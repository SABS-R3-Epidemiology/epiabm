from .host_progression_sweep import HostProgressionSweep
from .household_sweep import HouseholdSweep
from .toy_population_config import ToyPopulationFactory
import os
import typing


class Simulation:
    """Class to run a full simulation.
    """
    def configure(self, pop_params: typing.Dict, sim_params: typing.Dict,
                  file_params: typing.Dict):
        """Initialise a population structure for use in the simulation.

        :param pop_params: dictionary of parameter specific to the population.
        :type pop_params: dict
        :param sim_params: dictionay of parameters specific to the simulation
            used.
        :type sim_params: dict
        """
        self.pop_params = pop_params
        self.sim_params = sim_params
        self.file_params = file_params
        self.population = ToyPopulationFactory().make_pop(
            pop_params["population_size"], pop_params["cell_number"],
            pop_params["microcell_number"], pop_params["household_number"],
            pop_params["if_households"])
        self.filename = os.path.join(os.path.dirname(__file__),
                                     file_params["output_dir"],
                                     file_params["output_file"])
        with open(self.filename, 'w'):
            pass

    def run_sweeps(self):
        """Iteration step of the simulation. For each timestep the required
        spatial sweeps are run, which enqueues people who have been in contact
        """

        t = self.sim_params["simulation_start_time"]
        while t < self.sim_params["simulation_end_time"]:
            householdsweep = HouseholdSweep()
            householdsweep.bind_population(self.population)
            householdsweep(t)
            # PlaceSweep(t, self.population)
            for cell in self.population.cells:
                cell.queue_sweep(t)
            hostprog = HostProgressionSweep()
            hostprog.bind_population(self.population)
            hostprog(t)
            self.write_to_file(t)
            t += 1

    def write_to_file(self, time):
        count_susceptible = 0
        count_infectious = 0
        count_recovered = 0
        for cell in self.population.cells:
            for person in cell.persons:
                if person.is_susceptible():
                    count_susceptible += 1
                elif person.is_infectious():
                    count_infectious += 1
                else:
                    count_recovered += 1
        with open(self.filename, "a") as w:
            w.write("{},{},{}\n".format(time, "susceptible",
                                        count_susceptible))
            w.write("{},{},{}\n".format(time, "infectious", count_infectious))
            w.write("{},{},{}\n".format(time, "recovered", count_recovered))
