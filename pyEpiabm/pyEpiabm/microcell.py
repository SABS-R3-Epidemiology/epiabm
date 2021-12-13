#
# Mirocell Class
#
from .person import Person
from .infection_status import InfectionStatus
from .compartment_counter import CompartmentCounter


class Microcell:
    """Class representing a Microcell (Group of people and places).
    Collection of :class:`Person` s

    :param cell: An instance of :class:`Cell`
    :type cell: Cell
    """
    def __init__(self, cell):
        """Constructor Method.

        :param cell: Microcell's parent :class:`Cell` instance.
        :type cell: Cell
        """
        self.persons = []
        self.cell = cell
        self.compartment_counter = CompartmentCounter(
            f"Microcell {hash(self)}")

    def __repr__(self):
        """String representation of Microcell.

        :return: String representation of Microcell
        :rtype: str
        """
        return f"Microcell with {len(self.persons)} people"

    def add_people(self, n):
        """Adds n default :class:`Person` to Microcell.

        :param n: Number of default :class:`Person` s to add
        :type n: int
        """
        for i in range(n):
            p = Person(self)
            self.cell.persons.append(p)
            self.persons.append(p)

    def _setup(self) -> None:
        """Setup method. Should be called once Population has been setup.
        Called by population (DOESN'T NEED TO BE CALLED MANUALLY)
        """
        self.compartment_counter.initialize(len(self.persons))

    def notify_person_status_change(
            self,
            old_status: InfectionStatus,
            new_status: InfectionStatus) -> None:
        """Notify Microcell that a person's status has changed.

        :param old_status: Person's old infection status.
        :type old_status: :class:`InfectionStatus`
        :param new_status: Person's new infection status.
        :type new_status: :class:`InfectionStatus`
        """
        self.compartment_counter.report(old_status, new_status)
        self.cell.notify_person_status_change(old_status, new_status)
