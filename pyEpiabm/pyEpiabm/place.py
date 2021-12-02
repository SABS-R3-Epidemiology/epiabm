#
# Place Class
#
from .person import Person
from .cell import Cell
from .microcell import Microcell
import typing
from .place_type import PlaceType


class Place:
    '''Creates a place class which represents spaces such
    as cafes, restaurants and hotel where people may come
    into contact with others outside their household.'''
    def __init__(self, loc: typing.Tuple[float, float],
                 place_type: PlaceType, cell: Cell, microcell: Microcell):
        self._location = loc
        self.persons = []
        self.placetype = place_type
        self.susceptibility = place_type.susceptibility
        self.infectiveness = place_type.infectiveness

        self.cell = cell
        self.microcell = microcell
        if not (self.microcell.cell == self.cell):
            raise KeyError('Microcell is not contained in cell')

    def add_person(self, person: Person):
        '''Add people into the place'''
        self.persons.append(person)

    def remove_person(self, person: Person):
        '''Remove people from place'''
        if person not in self.persons:
            raise KeyError('Person not found in this place')
        else:
            self.persons.remove(person)
