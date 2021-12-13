#
# Person Class
#
from .infection_status import InfectionStatus


class Person:
    """Class to represent each person in a population.

    :param microcell: An instance of an :class:`Microcell`
    :type microcell: Microcell

    Class attributes.

    :param infection_status: Person's current infection status
    :type infection_status: InfectionStatus
    :param next_infection_status: Person's next infection staus after
        current one
    :type next_infection_status: InfectionStatus
    :param time_of_status_change: Time when person's infection status
        is updated
    :type time_of_status_change: int
    """

    def __init__(self, microcell,
                 age=0, susceptibility=0, infectiveness=0):
        """Constructor Method.

        :param microcell: Person's parent :class:`Microcell` instance
        :type microcell: Microcell
        :param age: Person's age
        :type age: float
        :param susceptibility: Person's susceptibility
        :type susceptibility: float
        :param infectiveness: Person's infectiveness
        :type infectiveness: float
        """
        self.age = age
        self.susceptibility = susceptibility
        self.infectiveness = infectiveness
        self.microcell = microcell
        self.infection_status = InfectionStatus.Susceptible
        self.household = None
        self.next_infection_status = None
        self.time_of_status_change = None

    def is_infectious(self):
        """Query if the person is currently infectious.

        :return: Whether person is currently infectious
        :rtype: bool
        """
        return self.infection_status in [
            InfectionStatus.InfectASympt,
            InfectionStatus.InfectMild,
            InfectionStatus.InfectGP,
            InfectionStatus.InfectHosp,
            InfectionStatus.InfectICU,
            InfectionStatus.InfectICURecov]

    def is_susceptible(self):
        """Query if the person is currently susceptible.

        :return: Whether person is currently susceptible
        :rtype: bool
        """
        return self.infection_status == InfectionStatus.Susceptible

    def __repr__(self):
        """Returns a string representation of Person.

        :return: String representation of person
        :rtype: str
        """
        return f"Person, Age = {self.age}"
