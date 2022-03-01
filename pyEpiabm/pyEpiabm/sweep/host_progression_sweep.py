#
# Progression of infection within individuals
#
import random
import numpy as np
import pyEpiabm as pe
from pyEpiabm.property import InfectionStatus
from pyEpiabm.utility import InverseCdf

from .abstract_sweep import AbstractSweep


class HostProgressionSweep(AbstractSweep):
    """Class for sweeping through population and updating host infection status
    and time to next infection status change.
    """

    def _update_time_to_status_change(self, person, time):
        """Assigns time until next infection status update,
         given as a random integer between 1 and 10.

        :param Person: Person class with infection status attributes
        :type Person: Person
        :param time: Current simulation time
        :type time: float
        """
        # This is left as a random integer for now but will be made more
        # complex later.
        new_time = random.randint(1, 10)
        new_time = float(new_time)
        person.time_of_status_change = time + new_time

    def _set_latent_time(self, person, time):
        """Calculates and returns latency period as calculated in
        CovidSim, given as the time until next infection status
        for a person who has been set as exposed.

        :param Person: Person class with infection status attributes
        :type Person: Person
        :param time: Current simulation time
        :type time: float
        """
        latent_period = pe.Parameters.instance().latent_period
        latent_period_iCDF = pe.Parameters.instance().latent_period_iCDF
        latent_icdf_object = InverseCdf(latent_period, latent_period_iCDF)
        latent_time = latent_icdf_object.icdf_choose_exp()

        if latent_time < 0.0:
            raise AssertionError('Negative latent time')

        person.time_of_status_change = time + latent_time

    def _update_next_infection_status(self, person):
        """Assigns next infection status based on
        current infection status.

        :param Person: Person class with infection status attributes
        :type Person: Person
        """
        # More infection statuses will be incorporated in future.
        if person.infection_status == InfectionStatus.InfectMild:
            person.next_infection_status = InfectionStatus.Recovered
        elif person.infection_status == InfectionStatus.Exposed:
            person.next_infection_status = InfectionStatus.InfectMild
        else:
            raise TypeError('update_next_infection_status should only ' +
                            'be applied to individuals with mild ' +
                            'infection status, or exposed')

    def __call__(self, time: float):
        """Sweeps through all people in the population and updates
        their infection status if it is time and assigns them their
        next infection status and a new time of next status change.

        :param time: Current simulation time
        :type time: float
        """

        for cell in self._population.cells:
            for person in cell.persons:
                if person.time_of_status_change is None:
                    assert person.infection_status \
                                    in [InfectionStatus.Susceptible]
                    continue
                while person.time_of_status_change <= time:
                    print(person.time_of_status_change)
                    person.update_status(person.next_infection_status)
                    if person.infection_status == InfectionStatus.Recovered:
                        person.next_infection_status = None
                        person.time_of_status_change = np.inf
                    if person.infection_status != InfectionStatus.Recovered:
                        self._update_next_infection_status(person)
                        if person.infection_status == InfectionStatus.Exposed:
                            self._set_latent_time(person, time)
                        else:
                            self._update_time_to_status_change(person, time)
