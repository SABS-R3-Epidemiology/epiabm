#
# Mirocell Class
#

import typing

from pyEpiabm.property import InfectionStatus

from .person import Person
from .place import Place
from ._compartment_counter import _CompartmentCounter


class Microcell:
    """Class representing a Microcell (Group of people and places).
    Collection of :class:`Person` s.

    :param cell: An instance of :class:`Cell`
    :type cell: Cell
    """
    def __init__(self, cell):
        """Constructor Method.

        :param cell: Microcell's parent :class:`Cell` instance
        :type cell: Cell
        """
        self.id = hash(self)
        self.persons = []
        self.places = []
        self.cell = cell
        self.compartment_counter = _CompartmentCounter(
            f"Microcell {id(self)}")

    def __repr__(self):
        """Returns a string representation of Microcell.

        :return: String representation of Microcell
        :rtype: str
        """
        return f"Microcell with {len(self.persons)} people."

    def set_id(self, id):
        """Updates ID of microcell (i.e. for input from file).

        :param id: Identity of microcell
        :type id: float
        """
        self.id = id

    def add_people(self, n):
        """Adds n default :class:`Person` to Microcell.

        :param n: Number of default :class:`Person` s to add
        :type n: int
        """
        for i in range(n):
            p = Person(self)
            self.cell.persons.append(p)
            self.persons.append(p)

    def add_place(self, n: int, loc: typing.Tuple[float, float],
                  place_type):
        """Adds n default :class:`Place` to Microcell.

        :param n: Number of default :class:`Place` s to add
        :type n: int
        """
        for _ in range(n):
            p = Place(loc, place_type, self.cell, self)
            self.cell.places.append(p)
            self.places.append(p)

    def _setup(self) -> None:
        """Setup method. Should be called once Population has been setup.
        Called by population (doesn't need to be called manually).
        """
        self.compartment_counter.initialize(len(self.persons))

    def notify_person_status_change(
            self,
            old_status: InfectionStatus,
            new_status: InfectionStatus) -> None:
        """Notify Microcell that a person's status has changed.

        :param old_status: Person's old infection status
        :type old_status: InfectionStatus
        :param new_status: Person's new infection status
        :type new_status: InfectionStatus
        """
        self.compartment_counter.report(old_status, new_status)
        self.cell.notify_person_status_change(old_status, new_status)
