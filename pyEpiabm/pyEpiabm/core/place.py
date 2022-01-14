#
# Place Class
#

import typing

from pyEpiabm.property import PlaceType

from .person import Person


class Place:
    """Creates a place class which represents spaces such
    as cafes, restaurants and hotels where people may come
    into contact with others outside their household.
    """
    def __init__(self, loc: typing.Tuple[float, float],
                 place_type: PlaceType, cell, microcell):
        """Constructor method.

        :param loc: (x,y) coordinates of the place
        :type loc: Tuple[float, float]
        :param place_type: Categorises the place
        :type place_type: 'PlaceType' enum
        :param cell: An instance of :class:`Cell`
        :type cell: Cell
        :param microcell: An instance of :class:`Microcell`
        :type microcell: Microcell
        """
        self._location = loc
        self.persons = []
        self.place_type = place_type
        self.max_capacity = 50
        self.susceptibility = 0
        self.infectiveness = 0

        self.cell = cell
        self.microcell = microcell
        # Assert the microcell and cell prescribes are related.
        if not (self.microcell.cell == self.cell):
            raise KeyError("Microcell is not contained in cell")

    def set_max_cap(self, max_capacity: int):
        """Sets the maximum capacity of a place.

        :param max_capacity: Maximum number of people
            allowed in place
        :type max_capacity: int
        """
        self.max_capacity = max_capacity

    def set_infectiveness(self, infectiveness: float):
        """Sets a baseline infectiveness for the place.

        :param infectiveness: Baseline infectiveness
        :type infectiveness: float
        """
        self.infectiveness = infectiveness

    def set_susceptibility(self, susceptibility: float):
        """Sets a baseline susceptibility for the place.

        :param susceptibility: Baseline susceptibility
        :type susceptibility: float
        """
        self.susceptibility = susceptibility

    def add_person(self, person: Person):
        """Add a person into the place.

        :param person: Person to add
        :type person: Person
        """
        self.persons.append(person)
        person.add_place(self)

    def remove_person(self, person: Person):
        """Remove a person from place.

        :param person: Person to remove from place
        :type person: Person
        """
        if person not in self.persons:
            raise KeyError("Person not found in this place")
        else:
            person.remove_place(self)
            self.persons.remove(person)

    def empty_place(self):
        """Remove all people from place. For example
        a restaurant or park might regularly change
        all occupants each timestep.
        """
        while len(self.persons) > 0:
            self.remove_person(self.persons[0])
