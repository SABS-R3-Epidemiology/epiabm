#
# Cell Class
#

import typing
from queue import Queue

from pyEpiabm.property import InfectionStatus

from .microcell import Microcell
from .person import Person
from ._compartment_counter import _CompartmentCounter


class Cell:
    """Class representing a Cell (Subset of Population).
    Collection of :class:`Microcell` s and :class:`Person` s.

    """
    def __init__(self, loc: typing.Tuple[float, float] = (0, 0)):
        """Constructor Method.

        Parameters
        ----------
        loc : Tuple(float, float)
            Location of the cell, as an (x,y) tuple

        """
        self.location = loc
        self.id = hash(self)
        self.microcells = []
        self.persons = []
        self.places = []
        self.person_queue = Queue()
        self.compartment_counter = _CompartmentCounter(f"Cell {id(self)}")

        if not (len(loc) == 2 and isinstance(loc[0], (float, int)) and
                isinstance(loc[1], (float, int))):
            raise ValueError("Location must be a tuple of float-type")

    def __repr__(self):
        """Returns a string representation of the Cell.

        Returns
        -------
        str
            String representation of the Cell

        """
        return f"Cell with {len(self.microcells)} microcells " + \
            f"and {len(self.persons)} people at location {self.location}."

    def add_microcells(self, n):
        """Add n empty :class:`Microcell` s to Cell.

        Parameters
        ----------
        n : int
            Number of empty :class:`Microcell` s to add

        """
        for _ in range(n):
            self.microcells.append(Microcell(self))

    def set_id(self, id: float):
        """Updates ID of cell (i.e. for input from file).

        Parameters
        ----------
        id : float
            Identity of cell

        """
        self.id = id

    def enqueue_person(self, person: Person):
        """Add person to queue for processing at end of iteration.

        Parameters
        ----------
        person : Person
            Person to enqueue

        """
        self.person_queue.put(person)

    def notify_person_status_change(
            self,
            old_status: InfectionStatus,
            new_status: InfectionStatus) -> None:
        """Notify Cell that a person's status has changed.

        Parameters
        ----------
        old_status : InfectionStatus
            Person's old infection status
        new_status : InfectionStatus
            Person's new infection status

        """
        self.compartment_counter.report(old_status, new_status)

    def number_infectious(self):
        """Returns the total number of infectious people in each
        cell.

        Returns
        -------
        int
            Total infectors in cell

        """
        cell_data = self.compartment_counter.retrieve()
        total_infectors = (cell_data[InfectionStatus.InfectASympt]
                           + cell_data[InfectionStatus.InfectMild]
                           + cell_data[InfectionStatus.InfectGP])

        return total_infectors

    def set_location(self, loc: typing.Tuple[float, float]):
        """Method to set or change the location of a cell.

        Parameters
        ----------
        loc : Tuple[float, float]
            (x,y) coordinates of the place

        """
        self.location = loc
