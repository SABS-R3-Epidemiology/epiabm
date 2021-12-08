#
# Cell Class
#
from .microcell import Microcell


class Cell:
    """Class representing a Cell (Subset of Population).
    Collection of :class:`Microcell` s and :class:`Person` s.
    """
    def __init__(self):
        """Constructor Method.
        """
        self.microcells = []
        self.persons = []

    def untested_method(self, x):
        y = x + 1
        return y
    
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
