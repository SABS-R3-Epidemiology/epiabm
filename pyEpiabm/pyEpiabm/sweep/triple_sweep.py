#
# Infection always causes three subsequent infections. Always.
#

import random

from pyEpiabm.core import Person

from .abstract_sweep import AbstractSweep


class TripleSweep(AbstractSweep):

    def __call__(self, time: float):
        """Given a population structure, loops over infected members
        and considers whether they infected household members based
        on individual, and spatial infectiousness and susceptibility.

        Parameters
        ----------
        time : float
            Simulation time

        """
        # Infects three people at first opportunity, then never again
        for cell in self._population.cells:
            infectious_persons = filter(Person.is_infectious, cell.persons)
            for infector in infectious_persons:
                while infector.secondary_infections_counts[-1] < 3:
                    infectee = random.choice(infector.household.susceptible_persons)
                    cell.enqueue_person(infectee)
                    infector.increment_secondary_infections()
                    inf_to_exposed = (time -
                                        infector.infection_start_times[-1])
                    infectee.set_exposure_period(inf_to_exposed)
