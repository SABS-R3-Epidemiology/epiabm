from .abstract_sweep import AbstractSweep
from .infection_status import InfectionStatus
from .csv_dict_writer import CsvDictWriter
from .population import Population
import os
import typing


class Simulation:
    """Class to run a full simulation.
    """
    def configure(self,
                  population: Population,
                  initial_sweeps: typing.List[AbstractSweep],
                  sweeps: typing.List[AbstractSweep],
                  sim_params: typing.Dict,
                  file_params: typing.Dict):
        """Initialise a population structure for use in the simulation.

        :param pop_params: dictionary of parameter specific to the population.
        :type pop_params: dict
        :param initial_sweeps: list of abstract sweep used to initialise the
            simulation.
        :type initial_sweeps: list
        :param sweeps: list of abstract sweeps used in the simulation. Queue
            sweep and host progression sweep must appear at the
        :type sweeps: list
        :param sim_params: dictionay of parameters specific to the simulation
            used.
        :type sim_params: dict
        :param file_params: dictionay of parameters specific to the output
            file.
        :type file_params: dict
        """
        self.sim_params = sim_params
        self.population = population
        self.sweeps = sweeps
        # Initial sweeps configure the population by changing the type,
        # infection status, infectiveness or susceptibility of people
        # or places. Only implemented once.
        for s in initial_sweeps:
            assert isinstance(s, AbstractSweep)
            s.bind_population(self.population)
            s()

        # General sweeps run through the population on every timestep, and
        # include host progression and spatial infections.
        for s in sweeps:
            assert isinstance(s, AbstractSweep)
            s.bind_population(self.population)

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
            for sweep in self.sweeps:
                sweep(t)
            self.write_to_file(t)
            t += 1

    def write_to_file(self, time):
        data = {s: 0 for s in list(InfectionStatus)}
        for cell in self.population.cells:
            for k in data:
                data[k] += cell.compartment_counter.retrieve()[k]
        data["time"] = time

        self.writer.write(data)
