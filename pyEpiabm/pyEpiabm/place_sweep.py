#
# Infection due to contact in social spaces outside of households
#

from .abstract_sweep import AbstractSweep
from .population import Population
from .covidsim_helpers import CovidsimHelpers
from .parameters import Parameters
import random


class PlaceSweep(AbstractSweep):
    '''Class to run the inter-household infections
    as part of the sweep function. Takes an individual
    person as input and tests a infection event against each
    susceptible member of the population. The resulting
    exposed person is added to an infection queue.
    '''

    def __call__(self, time: float, population: Population):
        '''
        Given a population structure, loops over infected members
        and considers whether they infected household members based
        on individual, and spatial infectiousness and susceptibility.

        : param infected: Person
        '''
        timestep = int(time * Parameters.instance().time_steps_per_day)

        # Double loop over the whole population, checking infectiousness
        # status, and whether they are absent from their household.
        for cell in population.cells:
            for place in cell.places:
                for infector in place.persons:
                    if not infector.is_infectious():
                        continue

                    # Check to see whether a place member is susceptible.
                    for infectee in place.persons:
                        if not infectee.is_susceptible():
                            continue

                        # Calculate "force of infection" parameter which will
                        # determine the likelihood of an infection event.
                        infectiousness = CovidsimHelpers.calc_place_inf(place,
                            infector, infectee, timestep)
                        susceptibility = CovidsimHelpers.calc_place_susc(place,
                            infector, infectee, timestep)
                        force_of_infection = infectiousness * susceptibility

                        # Compare a uniform random number to the force of
                        # infection to see whether an infection event occurs
                        # in this timestep between the given persons.
                        r = random.uniform(0, 1)
                        if r < force_of_infection:
                            cell.enqueue_person(infectee)
