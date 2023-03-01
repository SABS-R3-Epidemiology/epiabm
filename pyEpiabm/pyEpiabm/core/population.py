#
# Population Class
#

from queue import PriorityQueue

from .cell import Cell
from .person import Person


class Population:
    """Class representing a Population.
    Collection of :class:`Cell` s.

    """
    def __init__(self):
        """Constructor Method.

        """
        self.cells = []
        self.vaccine_queue = PriorityQueue()

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

    def enqueue_vaccine(self, priority, counter, person: Person):
        """Add person to queue for processing when mass vaccination
        begins.

        Parameters
        ----------
        priority : int
            Priority level of 1, 2, 3, or 4 to prioritise by age and
            whether carehome resident. 1 being highest priority and
            4 being lowest.
        counter : int
            Counter to prioritise by order of addition within each
            priority group. Generated successively onn addition of
            individuals to the queue.
        person : Person
            Person to enqueue

        """
        priority_value = int(priority)
        self.vaccine_queue.put((priority_value, counter, person))
