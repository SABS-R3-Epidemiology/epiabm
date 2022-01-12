#
# Population Class
#

from pyEpiabm.core import Cell


class Population:
    """Class representing a Population.
    Collection of :class:`Cell` s.
    """
    def __init__(self):
        """Constructor Method.
        """
        self.cells = []

    def __repr__(self):
        """Returns a string representation of a Population.

        :return: String representation of the Population
        :rtype: str
        """
        return "Population with {} cells.".format(len(self.cells))

    def add_cells(self, n):
        """Adds n default :class:`Cell` s to the population.

        :param n: Number of empty :class:`Cell` s to add
        :type n: int
        """
        for i in range(n):
            self.cells.append(Cell())

    def setup(self) -> None:
        """Setup method. Should be called once Population has been setup.
        """
        for cell in self.cells:
            cell._setup()

    def total_people(self):
        """Returns the total number of people in the population.
        Will obviously match the configuration parameter, but useful
        in various sweeps to have this attached.
        """
        count = 0
        for cell in self.cells:
            count += len(cell.persons)
        return count
