#
# Person Class
#

import random

from pyEpiabm.property import InfectionStatus


class Person:
    """Class to represent each person in a population.

    Parameters
    ----------
    microcell : Microcell
        An instance of an :class:`Microcell`

    Attributes
    ----------
    infection_status : InfectionStatus
        Person's current infection status
    next_infection_status : InfectionStatus
        Person's next infection status after current one
    time_of_status_change: int
        Time when person's infection status is updated

    """

    def __init__(self, microcell,
                 age=0, infectiousness=0):
        """Constructor Method.

        Parameters
        ----------
        microcell : Microcell
            Person's parent :class:`Microcell` instance
        age : float
            Person's age
        infectiousness : float
            Person's infectiousness

        """
        self.age = age
        self.initial_infectiousness = infectiousness
        self.infectiousness = 0
        self.microcell = microcell
        self.infection_status = InfectionStatus.Susceptible
        self.household = None
        self.places = []
        self.place_types = []
        self.next_infection_status = None
        self.time_of_status_change = None
        self.infection_start_time = None

    def is_infectious(self):
        """Query if the person is currently infectious.

        Returns
        -------
        bool
            Whether person is currently infectious

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

        Returns
        -------
        bool
            Whether person is currently susceptible

        """
        return self.infection_status == InfectionStatus.\
            Susceptible

    def __repr__(self):
        """Returns a string representation of Person.

        Returns
        -------
        str
            String representation of person

        """
        return f"Person, Age = {self.age}."

    def update_status(self,
                      new_status: InfectionStatus) -> None:
        """Update Person's Infection Status.

        Parameters
        ----------
        new_status : InfectionStatus
            Person's new status

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

    def add_place(self, place, person_group: int = 0):
        """Method adds a place to the place list if the person visits
        or is associated with this place. Places are saved as a tuple
        with the place as the first entry and the group the person is
        associated with as the second.

        Parameters
        ----------
        place: Place
            Place person should be added to
        person_group : int
            Key for the person group dictionary

        """
        if place.cell != self.microcell.cell:
            raise AttributeError("Place and person are not in the same\
                                 cell")
        self.places.append((place, person_group))
        self.place_types.append(place.place_type)

    def remove_place(self, place):
        """Method to remove person for each associated place, to be
        used when updating places.

        Parameters
        ----------
        place: Place
            Place person should be removed from

        """
        place_list = [i[0] for i in self.places]
        if place not in place_list:
            raise KeyError("Person not found in this place")
        else:
            ind = place_list.index(place)
            self.places.pop(ind)
            self.place_types.remove(place.place_type)
