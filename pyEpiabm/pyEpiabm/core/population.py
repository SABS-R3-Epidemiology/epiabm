#
# Population Class
#

from .cell import Cell


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

        Returns
        -------
        str
            String representation of the Population

        """
        return "Population with {} cells.".format(len(self.cells))

    def add_cells(self, n):
        """Adds n default :class:`Cell` s to the population.

        Parameters
        ----------
        n : int
            Number of empty :class:`Cell` s to add

        """
        for i in range(n):
            self.cells.append(Cell())
            self.cells[i].set_id(i)

    def total_people(self):
        """Returns the total number of people in the population.
        Will obviously match the configuration parameter, but useful
        in various sweeps to have this attached.

        """
        count = 0
        for cell in self.cells:
            count += len(cell.persons)
        return count
