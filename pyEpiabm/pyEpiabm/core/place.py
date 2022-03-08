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
        self.place_type = place_type
        self.max_capacity = 50
        self.susceptibility = 0
        self.infectiousness = 0

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

    def add_person(self, person: Person):
        """Add a person into the place.

        Parameters
        ----------
        person: Person
            Person to add

        """
        self.persons.append(person)
        person.add_place(self)

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
            person.remove_place(self)
            self.persons.remove(person)

    def empty_place(self):
        """Remove all people from place. For example
        a restaurant or park might regularly change
        all occupants each timestep.

        """
        while len(self.persons) > 0:
            self.remove_person(self.persons[0])
