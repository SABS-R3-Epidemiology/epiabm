#
# Infection due to contact within households
#

import random

from pyEpiabm.core import Parameters
from pyEpiabm.routine import HouseholdForces

from .abstract_sweep import AbstractSweep


class HouseholdSweep(AbstractSweep):
    """Class to run the intra-household infections
    as part of the sweep function. Takes an individual
    person as input and tests a infection event against each
    susceptible member of their household. The resulting
    exposed person is added to an infection queue.
    """

    def __call__(self, time: int):
        """Given a population structure, loops over infected members
        and considers whether they infected household members based
        on individual, and spatial infectiousness and susceptibility.

        : param time: Simulation time
        : type time: int
        """
        timestep = int(time * Parameters.instance().time_steps_per_day)

        # Double loop over the whole population, checking infectiousness
        # status, and whether they are absent from their household.
        for cell in self._population.cells:
            for infector in cell.persons:
                if not infector.is_infectious():
                    continue

                # Check to see whether a household member is susceptible.
                for infectee in infector.household.persons:
                    if not infectee.is_susceptible():
                        continue

                    # Calculate "force of infection" parameter which will
                    # determine the likelihood of an infection event.
                    force_of_infection = HouseholdForces.household_inf_force(
                        infector, infectee, timestep)

                    # Compare a uniform random number to the force of infection
                    # to see whether an infection event occurs in this timestep
                    # between the given persons.
                    r = random.uniform(0, 1)
                    if r < force_of_infection:
                        cell.enqueue_person(infectee)
