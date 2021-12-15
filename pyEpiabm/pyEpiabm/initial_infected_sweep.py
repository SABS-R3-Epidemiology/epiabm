from .abstract_sweep import AbstractSweep
import random
import pyEpiabm as pe


class InitialInfectedSweep(AbstractSweep):
    """Class for sweeping through population at start
    of simulation and setting an initial number of infecetd people.
    """

    def __call__(self, pop_params: dict):
        """Method that randomly chooses a number of people
        in the population and changes their infection status to InfectedMild
        and sets their time of next status change.

        :param pop_params: Dictionary of population parameters
        :type pop_params: dict
        """

        if pop_params["population_size"] < \
                pop_params["initial_infected_number"]:
            raise AssertionError('Initial number of infecetd people needs to be \
                                            less than the total population')

        for _ in range(pop_params["initial_infected_number"]):
            # Choose randomly which cell the person is in.
            cell_no = random.randint(0, len(self._population.cells)-1)
            cell = self._population.cells[cell_no]

            # Randomly asigns infective to any person in that cell.
            i = random.randint(0, len(cell.persons)-1)
            cell.persons[i].update_status(pe.InfectionStatus.InfectMild)
            cell.persons[i].update_time_to_status_change()
