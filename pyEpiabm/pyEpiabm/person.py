#
# Person Class
#
import random
from .infection_status import InfectionStatus


class Person:
    """Class to represent each person in a population.

    :param microcell: An instance of an :class:`Microcell`
    :type microcell: Microcell

    Class attributes.

    :param infection_status: Person's current infection status
    :type infection_status: InfectionStatus
    :param next_infection_status: Person's next infection status after
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
        self.places = []
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
        return f"Person, Age = {self.age}."

    def update_status(self,
                      new_status: InfectionStatus) -> None:
        """Update Person's Infection Status.

        :param new_status: Person's new status
        :type new_status: InfectionStatus
        """
        self.microcell.notify_person_status_change(
            self.infection_status, new_status)
        self.infection_status = new_status

    def update_time_to_status_change(self) -> None:
        """Method that assigns time until next infection status update,
         given as a random integer between 1 and 10.
        """
        # This is left as a random integer for now but will be made more
        # complex later.
        new_time = random.randint(1, 10)
        self.time_of_status_change = new_time

    def add_place(self, place):
        """Method adds a place to the place list if the person visits
        or is associated with this place.
        """
        if place.microcell != self.microcell:
            raise AttributeError("Place and person are not in the same\
                                 microcell")
        self.places.append(place)
