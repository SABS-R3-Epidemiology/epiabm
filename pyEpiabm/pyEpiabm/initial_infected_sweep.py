#
# Initialises infected members of the population
#
from .abstract_sweep import AbstractSweep
import random
import pyEpiabm as pe


class InitialInfectedSweep(AbstractSweep):
    """Class for sweeping through population at start
    of simulation and setting an initial number of infecetd people.
    """

    def __call__(self, sim_params: dict):
        """Method that randomly chooses a number of people
        in the population and changes their infection status to InfectedMild
        and sets their time of next status change.

        :param sim_params: Dictionary of simulation parameters
        :type sim_params: dict
        """
        pop_size = self._population.total_people()
        if pop_size < \
                sim_params["initial_infected_number"]:
            raise AssertionError('Initial number of infected people needs to be \
                                            less than the total population')

        # Checks whether there are enough susceptible people to infect.
        status = pe.InfectionStatus.Susceptible
        num_susceptible = 0
        for cell in self._population.cells:
            num_susceptible = num_susceptible + \
                                cell.compartment_counter.retrieve()[status]

        if num_susceptible < sim_params["initial_infected_number"]:
            raise AssertionError('There are not enough susceptible people in the \
                                        population to infect')

        num_people = 0
        while num_people < (sim_params["initial_infected_number"]):
            # Choose randomly which cell the person is in.
            cell_no = random.randint(0, len(self._population.cells)-1)
            cell = self._population.cells[cell_no]

            # Randomly asigns infective to any person in that cell.
            i = random.randint(0, len(cell.persons)-1)
            # Checks person has not already been assigned.
            if cell.persons[i].infection_status == \
                    pe.InfectionStatus.Susceptible:
                cell.persons[i].update_status(pe.InfectionStatus.InfectMild)
                cell.persons[i].update_time_to_status_change()
                num_people += 1
