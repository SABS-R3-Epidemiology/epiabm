#
# Population Class
#
from .cell import Cell


class Population:
    """Class representing a Population.
    Collection of :class:`Cell` s
    """
    def __init__(self):
        """Constructor Method.
        """
        self.cells = []

    def __repr__(self):
        """String Representation of Population.

        :return: String representation of the Population
        :rtype: str
        """
        return "Population with {} cells.".format(len(self.cells))

    def add_cells(self, n):
        """Adds n default :class:`Cell` s to the population.

        :param n: number of empty :class:`Cell` s to add
        :type n: int
        """
        for i in range(n):
            self.cells.append(Cell())

    def setup(self) -> None:
        """Setup method. Should be called once Population has been setup.
        """
        for cell in self.cells:
            cell._setup()
