#
# Cell Class
#
from .microcell import Microcell
from .person import Person
from queue import Queue


class Cell:
    """Class representing a Cell (Subset of Population).
    Collection of :class:`Microcell` s and :class:`Person` s.
    """
    def __init__(self):
        """Constructor Method.
        """
        self.microcells = []
        self.persons = []
        self.person_queue = Queue()

    def __repr__(self):
        """String representation of Cell.

        :return: String representation of Cell.
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
        """Add person to queue for processing at end of iteration

        :param person: Person to enqueue
        :type person: Person
        """
        self.person_queue.put(person)
