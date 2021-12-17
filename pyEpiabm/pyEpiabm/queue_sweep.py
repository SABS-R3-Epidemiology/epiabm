#
# Sweeps for enqueued persons to update infection status
#
from .abstract_sweep import AbstractSweep
from .infection_status import InfectionStatus


class QueueSweep(AbstractSweep):
    """Class to sweep through the enqueued persons
    in each cell and update their infection status.

    : param time: Simulation time, in days
    : type time: int
    """
    def __call__(self, time):
        """Function to run through the queue of exposed people.
        """
        for cell in self._population.cells:
            while not cell.person_queue.empty():
                person = cell.person_queue.get()
                # Get takes person from the queue and removes them, so clears
                # the queue for the next timestep.
                # Update the infection status
                person.update_status(InfectionStatus.Exposed)
                person.next_infection_status = InfectionStatus.InfectMild
                person.time_of_status_change = time
