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
        self.person_groups = {0: []}
        self.num_person_groups = 0
        self.place_type = place_type
        self.max_capacity = 50
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

        :param max_capacity: Maximum number of people
            allowed in place
        :type max_capacity: int
        """
        self.max_capacity = max_capacity

    def set_infectiousness(self, infectiousness: float):
        """Sets a baseline infectiousness for the place.

        :param infectiousness: Baseline infectiousness
        :type infectiousness: float
        """
        self.infectiousness = infectiousness

    def set_susceptibility(self, susceptibility: float):
        """Sets a baseline susceptibility for the place.

        :param susceptibility: Baseline susceptibility
        :type susceptibility: float
        """
        self.susceptibility = susceptibility

    def add_person(self, person: Person, person_group: int = 0):
        """Add a person into the place.

        :param person: Person to add
        :type person: Person
        :param person_group: key for the person group dictionary
        :type person_group: int
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

        :param person: Person to remove from place
        :type person: Person
        """
        if person not in self.persons:
            raise KeyError("Person not found in this place")
        else:
            group_index = self.get_group_index(person)
            self.person_groups[group_index].remove(person)
            # If anyone can think of a better way to remove
            # people from a dictionary without knowing the
            # key lmk.
            person.remove_place(self)
            self.persons.remove(person)

    def get_group_index(self, person):
        """Get the group of a person in the place.

        :param person: Person to remove from place
        :type person: Person
        """
        place_list = [i[0] for i in person.places]
        ind = place_list.index(self)
        return person.places[ind][1]

    def empty_place(self, person_groups: list = [0]):
        """Remove all people from place who are in a specific
        person group. For example
        a restaurant or park might regularly change
        all occupants each timestep, but workers at the
        restaurant will be present each timestep.

        :param person_groups: list of person_group
        indicies to be removed
        :type person_groups: list
        """
        for group in person_groups:
            for person in self.person_groups[group]:
                self.remove_person(person)
