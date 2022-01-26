#
# Cell Class
#

from queue import Queue

from pyEpiabm.property import InfectionStatus

from .microcell import Microcell
from .person import Person
from ._compartment_counter import _CompartmentCounter


class Cell:
    """Class representing a Cell (Subset of Population).
    Collection of :class:`Microcell` s and :class:`Person` s.
    """
    def __init__(self):
        """Constructor Method.
        """
        self.microcells = []
        self.persons = []
        self.places = []
        self.person_queue = Queue()
        self.compartment_counter = _CompartmentCounter(f"Cell {id(self)}")

    def __repr__(self):
        """Returns a string representation of the Cell.

        :return: String representation of the Cell
        :rtype: str
        """
        return f"Cell with {len(self.microcells)} microcells " + \
            f"and {len(self.persons)} people."

    def add_microcells(self, n):
        """Add n empty :class:`Microcell` s to Cell.

        :param n: Number of empty :class:`Microcell` s to add
        :type n: int
        """
        for i in range(n):
            self.microcells.append(Microcell(self))

    def enqueue_person(self, person: Person):
        """Add person to queue for processing at end of iteration.

        :param person: Person to enqueue
        :type person: Person
        """
        self.person_queue.put(person)

    def _setup(self) -> None:
        """Setup method. Should be called once Population has been setup.
        Called by population (doesn't need to be called manually).
        """
        self.compartment_counter.initialize(len(self.persons))
        for mcell in self.microcells:
            mcell._setup()

    def notify_person_status_change(
            self,
            old_status: InfectionStatus,
            new_status: InfectionStatus) -> None:
        """Notify Cell that a person's status has changed.

        :param old_status: Person's old infection status
        :type old_status: InfectionStatus
        :param new_status: Person's new infection status
        :type new_status: InfectionStatus
        """
        self.compartment_counter.report(old_status, new_status)

    def infectious_number(self):
        """Returns the total number of infectious people in each
        cell.

        :return: Total infectors in cell
        :rtype: int
        """
        cell_data = self.compartment_counter.retrieve()
        total_infectors = (cell_data[InfectionStatus.InfectASympt]
                           + cell_data[InfectionStatus.InfectMild]
                           + cell_data[InfectionStatus.InfectGP])

        return total_infectors
