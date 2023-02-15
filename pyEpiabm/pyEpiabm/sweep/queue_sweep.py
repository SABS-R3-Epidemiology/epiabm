#
# Sweeps for enqueued persons to update infection status
#

from pyEpiabm.property import InfectionStatus

from .abstract_sweep import AbstractSweep


class QueueSweep(AbstractSweep):
    """Class to sweep through the enqueued persons
    in each cell and update their infection status.

    """
    @profile
    def __call__(self, time: float):
        """Function to run through the queue of people to be exposed.

        Parameters
        ----------
        time : float
            Simulation time

        """
        for cell in self._population.cells:
            while not cell.person_queue.empty():
                person = cell.person_queue.get()
                # Get takes person from the queue and removes them, so clears
                # the queue for the next timestep.
                # Update the infection status
                person.next_infection_status = InfectionStatus.Exposed
                person.time_of_status_change = time
