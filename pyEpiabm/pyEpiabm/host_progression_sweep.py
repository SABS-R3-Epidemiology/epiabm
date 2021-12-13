import random
from .abstract_sweep import AbstractSweep
from .infection_status import InfectionStatus


class HostProgressionSweep(AbstractSweep):
    """Class for sweeping through population and updating host infection status
    and time to next infection status change.
    """

    def _update_time_to_status_change(self):
        """Method that assigns time until next infection status update,
         given as a random integer between 1 and 10.

        :return: Time until next infection status update
        :rtype: int
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
            raise TypeError('update_next_infection_status should only' +
                            'be applied to individuals with mild' +
                            'infection status')

    def __call__(self, time: int):
        """Method that sweeps through all people in the population
        and updates their infection status if it is time and assigns
        them a next infection status and a new time of next status
        change.

        : param time: Current simulation time in days
        : type time: int
        """
        if not (type(time) == int):
            raise TypeError('Time needs to be type int')
        for cell in self._population.cells:
            for person in cell.persons:
                if person.time_of_status_change == time:
                    self._update_next_infection_status(person)
                    person.infection_status = person.next_infection_status
                    if not person.infection_status == \
                            InfectionStatus.Recovered:
                        person.time_of_status_change =\
                            time + self._update_time_to_status_change()
