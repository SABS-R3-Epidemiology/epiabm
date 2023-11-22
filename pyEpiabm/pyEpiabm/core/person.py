#
# Person Class
#

import random
import re

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

    def __init__(self, microcell, age_group=None):
        """Constructor Method.

        Parameters
        ----------
        microcell : Microcell
            Person's parent :class:`Microcell` instance
        age_group : int or None
            Integer identifying persons age group or None if random age should
            be assigned

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
        self.date_positive = None
        self.is_vaccinated = False
        self.id = self.microcell.id + "." + "." + \
                  str(len(self.microcell.persons))

        self.set_random_age(age_group)

    def set_random_age(self, age_group=None):
        """Set random age of person, and save index of their age group.
        Note that the max age in the 80+ group is 84 here, however the precise
        age of 80+ people is never used (exact ages are only used to assign
        school/workplaces) so this does not cause any issues.

        """
        if Parameters.instance().use_ages:
            if age_group is None:
                group_probs = Parameters.instance().age_proportions
                self.age_group = random.choices(range(len(group_probs)),
                                                weights=group_probs)[0]
            else:
                self.age_group = age_group
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
        return self.infection_status == InfectionStatus. \
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

        if self.infection_status == InfectionStatus.Susceptible and \
            self.household is not None:
            self.household.add_susceptible_person(self)
        if self.infection_status == InfectionStatus.Exposed and \
            self.household is not None:
            self.household.remove_susceptible_person(self)

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
            self.place_types.pop(ind)

    def is_place_closed(self, closure_place_type):
        """Method to check if any of the place in the person's place list
        will be closed based on the place type, to be
        used when place closure intervention is active.

        Parameters
        ----------
        closure_place_type: a list of PlaceType
            PlaceType should be closed if in place closure intervention

        """
        if (hasattr(self.microcell, 'closure_start_time')) and (
            self.microcell.closure_start_time is not None):
            for place_type in self.place_types:
                if place_type.value in closure_place_type:
                    return True
        return False

    def vaccinate(self, time):
        """Used to set a persons vaccination status to vaccinated
        if they are drawn from the vaccine queue.

        """
        self.is_vaccinated = True
        self.date_vaccinated = time

    def remove_person(self):
        """Method to remove Person object from population.
        Used to remove travellers from the population.

        """
        self.microcell.cell.compartment_counter. \
            _increment_compartment(-1, self.infection_status,
                                   self.age_group)
        self.microcell.compartment_counter. \
            _increment_compartment(-1, self.infection_status,
                                   self.age_group)
        self.microcell.cell.persons.remove(self)
        self.microcell.persons.remove(self)
        self.household.persons.remove(self)

    def set_id(self, id: str):
        """Updates id of current person (i.e. for input from file).
        id format: 4.3.2.1 represents cell 4, microcell 3 within this cell,
        household 2 within this microcell, and person 1 within this
        household. The id will only be changed if there is a match.

        Parameters
        ----------
        id : str
            Identity of person

        """

        # Ensure id is a string
        if not isinstance(id, str):
            raise TypeError("Provided id must be a string")

        # This regex will match on any string which takes the form "i.j.k.l"
        # where i, j, k and l are integers (k can be empty)
        if not re.match("^\\d+\\.\\d+\\.\\d*\\.\\d+$", id):
            raise ValueError(f"Invalid id: {id}. id must be of the form "
                             f"'i.j.k.l' where i, j, k, l are integers (k"
                             f"can be empty)")

        # Finally, check for duplicates
        person_ids = [person.id for person in self.household.persons]
        if id in person_ids:
            raise ValueError(f"Duplicate id: {id}.")

        self.id = id
