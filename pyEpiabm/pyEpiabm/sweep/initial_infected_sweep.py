#
# Seed infected individuals in population
#
import random

from pyEpiabm.property import InfectionStatus
from pyEpiabm.sweep import AbstractSweep


class InitialInfectedSweep(AbstractSweep):
    """Class for sweeping through population at start
    of simulation and setting an initial number of infected people.
    """

    def __call__(self, sim_params: dict):
        """Method that randomly chooses a user-supplied number of people
        in the population, changes their infection status to InfectMild
        and sets their time of next status change.

        :param sim_params: Dictionary of simulation parameters
        :type sim_params: dict
        """
        pop_size = self._population.total_people()
        if pop_size < \
                sim_params["initial_infected_number"]:
            raise ValueError('Initial number of infected people needs to be \
                                            less than the total population')

        # Checks whether there are enough susceptible people to infect.
        status = InfectionStatus.Susceptible
        num_susceptible = 0
        for cell in self._population.cells:
            num_susceptible = num_susceptible + \
                                cell.compartment_counter.retrieve()[status]

        if num_susceptible < sim_params["initial_infected_number"]:
            raise ValueError('There are not enough susceptible people in the \
                                        population to infect')

        all_persons = [pers for cell in self._population.cells
                       for pers in cell.persons
                       if pers.infection_status == InfectionStatus.Susceptible]
        pers_to_infect = random.sample(all_persons,
                                       sim_params["initial_infected_number"])
        for person in pers_to_infect:
            person.update_status(InfectionStatus.InfectMild)
            person.update_time_to_status_change()
