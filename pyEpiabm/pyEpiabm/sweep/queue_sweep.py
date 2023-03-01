#
# Sweeps for enqueued persons to update infection status
#
import random

from pyEpiabm.core import Parameters
from pyEpiabm.property import InfectionStatus

from .abstract_sweep import AbstractSweep


class QueueSweep(AbstractSweep):
    """Class to sweep through the enqueued persons
    in each cell and update their infection status.

    """
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
                if person.is_vaccinated:
                    vacc_params = Parameters.instance().\
                        intervention_params['vaccine_params']
                    if time > (person.date_vaccinated +
                               vacc_params['time_to_efficacy']):
                        r = random.random()
                        if r < vacc_params['vacc_protectiveness']:
                            person.next_infection_status = InfectionStatus.\
                                Vaccinated
                        else:
                            person.next_infection_status = InfectionStatus.\
                                Exposed
                    else:
                        person.next_infection_status = InfectionStatus.Exposed
                else:
                    person.next_infection_status = InfectionStatus.Exposed
                
                person.time_of_status_change = time
