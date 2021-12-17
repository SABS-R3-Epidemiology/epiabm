#
# Infection due to contact in social spaces outside of households
#

import random
from .abstract_sweep import AbstractSweep
from .covidsim_helpers import CovidsimHelpers as c
from .parameters import Parameters


class PlaceSweep(AbstractSweep):
    """Class to run the place infections
    as part of the sweep function. Takes an individual
    person as input and tests a infection event against each
    susceptible member of the place. The resulting
    exposed person is added to an infection queue.
    """

    def __call__(self, time: float):
        """
        Given a population structure with places, loops over infected
        members of the place and considers whether they infected other
        people present, based on individual and place infectiousness
        and susceptibility.

        :param time: Current simulation time
        :type time: int
        """
        timestep = int(time * Parameters.instance().time_steps_per_day)

        # Double loop over the whole population, checking infectiousness
        # status, and whether they are absent from their household.
        for cell in self._population.cells:
            for place in cell.places:
                for infector in place.persons:
                    if not infector.is_infectious():
                        continue
                    # Check to see whether a place member is susceptible.

                    for infectee in place.persons:
                        if not infectee.is_susceptible():
                            continue

                        # Calculate "force of infection" parameter which will
                        # determine the likelihood of an infection event
                        # between the infector and infectee given that they
                        # meet in this place.
                        infectiousness = c.calc_place_inf(place, infector,
                                                          infectee, timestep)
                        susceptibility = c.calc_place_susc(place, infector,
                                                           infectee, timestep)
                        force_of_infection = infectiousness * susceptibility

                        # Compare a uniform random number to the force of
                        # infection to see whether an infection event occurs
                        # in this timestep between the given persons.
                        r = random.uniform(0, 1)
                        if r < force_of_infection:
                            cell.enqueue_person(infectee)
