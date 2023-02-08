#
# Person Class
#

import random

from pyEpiabm.property import InfectionStatus

from .parameters import Parameters


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

    def __init__(self, microcell):
        """Constructor Method.

        Parameters
        ----------
        microcell : Microcell
            Person's parent :class:`Microcell` instance

        """
        self.initial_infectiousness = 0
        self.infectiousness = 0
        self.microcell = microcell
        self.infection_status = InfectionStatus.Susceptible
        self.household = None
        self.places = []
        self.place_types = []
        self.next_infection_status = None
        self.time_of_status_change = None
        self.infection_start_time = None
        self.care_home_resident = False
        self.key_worker = False
        self.isolation_start_time = None
        self.is_vaccinated = False

        self.set_random_age()

    def set_random_age(self):
        """Set random age of person, and save index of their age group.
        Note that the max age in the 80+ group is 84 here, however the precise
        age of 80+ people is never used (exact ages are only used to assign
        school/workplaces) so this does not cause any issues.

        """
        if Parameters.instance().use_ages:
            group_probs = Parameters.instance().age_proportions
            self.age_group = random.choices(range(len(group_probs)),
                                            weights=group_probs)[0]
            self.age = random.randint(0, 4) + 5 * self.age_group
        else:
            self.age = None
            # If age is not used in the model, then every person is in the
            # same age group (to conserve same output structure)
            self.age_group = 0

    def is_symptomatic(self):
        """Query if the person is currently symptomatic.

        Returns
        -------
        bool
            Whether person is currently symptomatic

        """
        return Person.is_infectious(self) and self.infection_status != \
            InfectionStatus.InfectASympt

    def is_infectious(self):
        """Query if the person is currently infectious.

        Returns
        -------
        bool
            Whether person is currently infectious

        """
        return str(self.infection_status).startswith('InfectionStatus.Infect')

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
        return f"Person, Age = {self.age}, Status = {self.infection_status}."

    def update_status(self,
                      new_status: InfectionStatus) -> None:
        """Update Person's Infection Status.

        Parameters
        ----------
        new_status : InfectionStatus
            Person's new status

        """
        self.microcell.notify_person_status_change(
            self.infection_status, new_status, self.age_group)
        self.infection_status = new_status

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
