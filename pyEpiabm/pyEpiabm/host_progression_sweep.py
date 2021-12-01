import random
from .abstract_sweep import AbstractSweep
from .population import Population
from .infection_status import InfectionStatus


class HostProgressionSweep(AbstractSweep):
    '''Class for sweeping through population and updating host infection status
    and time to next infection status change.
    '''

    def _update_time_to_status_change(self):
        """Method that assigns time until next infection status update,
         given as a random integer between 1 and 10.
        """
        # This is left as a random integer for now but will be made more
        # complex later.
        new_time = random.randint(1, 10)
        return new_time

    def _update_next_infection_status(self, person):
        """Method that assigns next infection status based on
        current infection status.

        : param Person: Person class with infection status attributes
        : type Person: Person
        """
        # More infection statuses will be incorporated in future.
        if person.infection_status == InfectionStatus.InfectMild:
            person.next_infection_status = InfectionStatus.Recovered
        else:
            raise TypeError('Infection status of a person must be InfectMild.')

    def __call__(self, time: float):
        """Method that sweeps through all people in the population
        and updates their infection status if it is time and assigns
        them a next infection status and a new time of next status
        change.

        : param time: Current simulation time in days
        : type time: float
        """
        for cell in self._population.cells:
            for person in cell.persons:
                if person.time_of_status_change == time:
                    person.infection_status = person.next_infection_status
                    person.next_infection_status =\
                        self._update_next_infection_status(person)
                    person.time_of_status_change =\
                        time + self._update_time_to_status_change
