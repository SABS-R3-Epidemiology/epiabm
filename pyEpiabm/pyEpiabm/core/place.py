#
# Place Class
#

import typing

from pyEpiabm.property import PlaceType

from .person import Person


class Place:
    """Creates a place class which represents spaces such
    as cafes, restaurants and hotels where people may come
    into contact with others outside their household. People
    can be stratified in this place into different groups
    which may interact differently (ie workers and visitors).

    """
    def __init__(self, loc: typing.Tuple[float, float],
                 place_type: PlaceType, cell, microcell):
        """Constructor method.

        Parameters
        ----------
        loc : Tuple[float, float]
            (x,y) coordinates of the place
        place_type : 'PlaceType' enum
            Categorises the place
        cell : Cell
            An instance of :class:`Cell`
        microcell : Microcell
            An instance of :class:`Microcell`

        """
        self._location = loc
        self.persons = []
        self.person_groups = {0: []}
        self.num_person_groups = 1
        self.place_type = place_type
        self.max_capacity = 50
        self.mean_capacity = 25
        self.susceptibility = 0
        self.infectiousness = 0
        self.initialised = False

        self.cell = cell
        self.microcell = microcell
        # Assert the microcell and cell prescribes are related.
        if not (self.microcell.cell == self.cell):
            raise KeyError("Microcell is not contained in cell")

        if not (len(loc) == 2 and isinstance(loc[0], (float, int)) and
                isinstance(loc[1], (float, int))):
            raise ValueError("Location must be a tuple of float-type")

    def set_max_cap(self, max_capacity: int):
        """Sets the maximum capacity of a place.

        Parameters
        ----------
        max_capacity : int
            Maximum number of people allowed in place

        """
        self.max_capacity = max_capacity

    def set_mean_cap(self, mean_capacity: float):
        """Sets the mean capacity of a place.

        :param mean_capacity: Mean capacity of place type
        :type mean_capacity: float
        """
        self.mean_capacity = mean_capacity

    def set_infectiousness(self, infectiousness: float):
        """Sets a baseline infectiousness for the place.

        Parameters
        ----------
        infectiousness : float
            Baseline infectiousness

        """
        self.infectiousness = infectiousness

    def set_susceptibility(self, susceptibility: float):
        """Sets a baseline susceptibility for the place.

        Parameters
        ----------
        susceptibility : float
            Baseline susceptibility

        """
        self.susceptibility = susceptibility

    def add_person(self, person: Person, person_group: int = 0):
        """Add a person into the place.

        Parameters
        ----------
        person: Person
            Person to add
        person_group : int
            Key for the person group dictionary

        """
        self.persons.append(person)
        if person_group in self.person_groups.keys():
            self.person_groups[person_group].append(person)
        else:
            self.person_groups[person_group] = [person]
            self.num_person_groups += 1
        person.add_place(self, person_group)

    def remove_person(self, person: Person):
        """Remove a person from place.

        Parameters
        ----------
        person: Person
            Person to remove from place

        """
        if person not in self.persons:
            raise KeyError("Person not found in this place")
        else:
            group_index = self.get_group_index(person)
            self.person_groups[group_index].remove(person)
            person.remove_place(self)
            self.persons.remove(person)

    def get_group_index(self, person):
        """Get the group of a person in the place.

        :param person: Person associated with group
        :type person: Person
        """
        if person not in self.persons:
            raise KeyError("Person not found in this place")
        else:
            place_list = [i[0] for i in person.places]
            ind = place_list.index(self)
        return person.places[ind][1]

    def empty_place(self, groups_to_empty: list = []):
        """Remove all people from place who are in a specific
        person group. For example a restaurant or park might
        regularly change all occupants each timestep, but
        workers at the restaurant will be present each timestep.
        Defaults to emptying the whole place.

        :param person_groups: List of person_group
            indicies to be removed
        :type person_groups: list

        """
        if len(groups_to_empty) == 0:
            groups_to_empty = [key for key in self.person_groups.keys()]
        for group in groups_to_empty:
            if group not in self.person_groups.keys():
                continue
            for person in self.person_groups[group]:
                self.remove_person(person)
