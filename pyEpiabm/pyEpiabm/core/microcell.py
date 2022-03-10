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

    Parameters
    ----------
    cell : Cell
        An instance of :class:`Cell`

    """
    def __init__(self, cell):
        """Constructor Method.

        Parameters
        ----------
        cell: Cell
            Microcell's parent :class:`Cell` instance

        """
        self.id = hash(self)
        self.persons = []
        self.places = []
        self.cell = cell
        self.location = cell.location
        self.compartment_counter = _CompartmentCounter(
            f"Microcell {id(self)}")

    def __repr__(self):
        """Returns a string representation of Microcell.

        Returns
        -------
        str
            String representation of Microcell

        """
        return f"Microcell with {len(self.persons)} people" + \
            f" at location {self.location}."

    def set_id(self, id):
        """Updates ID of microcell (i.e. for input from file).

        Parameters
        ----------
        id : float
            Identity of microcell

        """
        self.id = id

    def add_people(self, n, status=InfectionStatus.Susceptible):
        """Adds n default :class:`Person` of given status to Microcell.

        Parameters
        ----------
        n : int
            Number of default :class:`Person` s to add
        status : InfectionStatus
            Status of persons to add to cell

        """
        self.compartment_counter._increment_compartment(n, status)
        self.cell.compartment_counter._increment_compartment(n, status)
        for _ in range(n):
            p = Person(self)
            self.cell.persons.append(p)
            self.persons.append(p)
            p.infection_status = status

    def add_place(self, n: int, loc: typing.Tuple[float, float],
                  place_type):
        """Adds n default :class:`Place` to Microcell.

        Parameters
        ----------
        n : int
            Number of default :class:`Place` s to add

        """
        for _ in range(n):
            p = Place(loc, place_type, self.cell, self)
            self.cell.places.append(p)
            self.places.append(p)

    def notify_person_status_change(
            self,
            old_status: InfectionStatus,
            new_status: InfectionStatus) -> None:
        """Notify Microcell that a person's status has changed.

        Parameters
        ----------
        old_status : InfectionStatus
            Person's old infection status
        new_status : InfectionStatus
            Person's new infection status

        """
        self.compartment_counter.report(old_status, new_status)
        self.cell.notify_person_status_change(old_status, new_status)

    def set_location(self, loc: typing.Tuple[float, float]):
        """Method to set or change the location of a microcell.

        Parameters
        ----------
        loc : Tuple[float, float]
            (x,y) coordinates of the microcell

        """
        if not (len(loc) == 2 and isinstance(loc[0], (float, int)) and
                isinstance(loc[1], (float, int))):
            raise ValueError("Location must be a tuple of float-type")
        self.location = loc
