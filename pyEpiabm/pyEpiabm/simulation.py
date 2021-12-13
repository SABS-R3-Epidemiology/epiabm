from .host_progression_sweep import HostProgressionSweep
from .household_sweep import HouseholdSweep
from .toy_population_config import ToyPopulationFactory
from .infection_status import InfectionStatus
from .csv_dict_writer import CsvDictWriter
from .population import Population
import os
import typing

class Simulation:
    """Class to run a full simulation.
    """
    def configure(self, population: Population, sim_params: typing.Dict,
                  file_params: typing.Dict):
        """Initialise a population structure for use in the simulation.

        :param pop_params: dictionary of parameter specific to the population.
        :type pop_params: dict
        :param sim_params: dictionay of parameters specific to the simulation
            used.
        :type sim_params: dict
        """
        self.sim_params = sim_params
        self.population = population

        filename = os.path.join(os.getcwd(),
                                     file_params["output_dir"],
                                     file_params["output_file"])
        self.writer = CsvDictWriter(
            filename,
            ["time"] + [s for s in InfectionStatus])

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
        data = {s: 0 for s in list(InfectionStatus)}
        for cell in self.population.cells:
            for k in data:
                data[k] += cell.compartment_counter.retrieve()[k]
        data["time"] = time
        
        self.writer.write(data)
