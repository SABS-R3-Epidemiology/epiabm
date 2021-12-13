from .host_progression_sweep import HostProgressionSweep
from .household_sweep import HouseholdSweep
from .toy_population_config import ToyPopulationFactory
from .csv_writer import CsvWriter
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
        self.population = ToyPopulationFactory().make_pop(
            pop_params["population_size"], pop_params["cell_number"],
            pop_params["microcell_number"], pop_params["household_number"],
            pop_params["if_households"])

        filename = os.path.join(os.getcwd(),
                                     file_params["output_dir"],
                                     file_params["output_file"])
        self.writer = CsvWriter(
            filename,
            ["time", "Susceptible", "Infected", "Recovered"])

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
        counts = {s: 0 for s in list(InfectionStatus)}
        for cell in self.population.cells:
            
        
        self.outfile.write("{},{},{}\n".format(time, "susceptible",
                                    count_susceptible))
        self.outfile.write("{},{},{}\n".format(time, "infectious", count_infectious))
        self.outfile.write("{},{},{}\n".format(time, "recovered", count_recovered))
