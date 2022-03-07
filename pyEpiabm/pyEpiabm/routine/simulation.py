#
# Simulates a complete pandemic
#

import random
import os
import logging
import typing
import numpy as np
from tqdm import tqdm

from pyEpiabm.core import Population
from pyEpiabm.output import _CsvDictWriter
from pyEpiabm.property import InfectionStatus
from pyEpiabm.sweep import AbstractSweep
from pyEpiabm.utility import log_exceptions


class Simulation:
    """Class to run a full simulation.

    """
    @log_exceptions()
    def configure(self,
                  population: Population,
                  initial_sweeps: typing.List[AbstractSweep],
                  sweeps: typing.List[AbstractSweep],
                  sim_params: typing.Dict,
                  file_params: typing.Dict):
        """Initialise a population structure for use in the simulation.

        sim_params Contains:
            * `simulation_start_time`: The initial time for the simulation
            * `simulation_end_time`: The final time to stop the simulation
            * `initial_infected_number`: The initial number of infected \
               individuals in the population
            * `simulation_seed`:  Random seed for reproducible simulations

        file_params Contains:
            * `output_file`: String for the name of the output .csv file
            * `output_dir`: String for the location of the output file, \
               as a relative path
            * `spatial_output`: Boolean to determine whether a spatial output \
               should be used

        Parameters
        ----------
        population : Population
            Population structure for the model
        pop_params : dict
            Dictionary of parameter specific to the population
        initial_sweeps : list
            List of sweeps used to initialise the simulation
        sweeps : list
            List of sweeps used in the simulation. Queue sweep and host
            progression sweep should appear at the end of the list
        sim_params : dict
            Dictionary of parameters specific to the simulation used and used
            as input for call method of initial sweeps
        file_params : dict
            Dictionary of parameters specific to the output file

        """
        self.sim_params = sim_params
        self.population = population
        self.initial_sweeps = initial_sweeps
        self.sweeps = sweeps

        self.spatial_output = file_params["spatial_output"] \
            if "spatial_output" in file_params else False

        # If random seed is specified in parameters, set this in numpy
        if "simulation_seed" in self.sim_params:
            random.seed(self.sim_params["simulation_seed"])
            np.random.seed(self.sim_params["simulation_seed"])

        # Initial sweeps configure the population by changing the type,
        # infection status, infectiousness or susceptibility of people
        # or places. Only runs on the first timestep.
        for s in initial_sweeps + sweeps:
            s.bind_population(self.population)
            logging.info(f"Bound sweep {s.__class__.__name__} to"
                         + " population")

        # General sweeps run through the population on every timestep, and
        # include host progression and spatial infections.

        folder = os.path.join(os.getcwd(),
                              file_params["output_dir"])

        filename = os.path.join(folder, file_params["output_file"])
        logging.info(f"Set output location to {filename}")

        output_titles = ["time"] + [s for s in InfectionStatus]
        if self.spatial_output:
            output_titles.insert(1, "cell")
            output_titles.insert(2, "location_x")
            output_titles.insert(3, "location_y")

        self.writer = _CsvDictWriter(
            folder, filename,
            output_titles)

    @log_exceptions()
    def run_sweeps(self):
        """Iteration step of the simulation. First the initialisation sweeps
        configure the population on the first timestep. Then at each
        subsequent timestep the sweeps run, updating the population. At each
        timepoint, a count of each infection status is written to file. Note
        that the elements of intial sweeps take the sim_params dict as an
        argument for their call method but the elements of sweeps take time
        as an argument for their call method.

        """
        # Initialise on the time step before starting.
        for sweep in self.initial_sweeps:
            sweep(self.sim_params)

        logging.info("Initial Sweeps Completed")

        # First entry of the data file is the initial state
        self.write_to_file(self.sim_params["simulation_start_time"])

        for t in tqdm(range(self.sim_params["simulation_start_time"] + 1,
                            self.sim_params["simulation_end_time"])):
            for sweep in self.sweeps:
                sweep(t)
            self.write_to_file(t)
            logging.debug(f'Iteration {t} completed')

        logging.info(f"Final time {t} reached")

    def write_to_file(self, time):
        """Records the count number of a given list of infection statuses
        and writes these to file.

        Parameters
        ----------
        time : float
            Time of output data

        """

        if self.spatial_output:  # Separate output line for each cell
            for cell in self.population.cells:
                data = {s: 0 for s in list(InfectionStatus)}
                for k in data:
                    data[k] += cell.compartment_counter.retrieve()[k]
                data["time"] = time
                data["cell"] = cell.id
                data["location_x"] = cell.location[0]
                data["location_y"] = cell.location[1]
                self.writer.write(data)
        else:  # Summed output across all cells in population
            data = {s: 0 for s in list(InfectionStatus)}
            for cell in self.population.cells:
                for k in data:
                    data[k] += cell.compartment_counter.retrieve()[k]
            data["time"] = time
            self.writer.write(data)

    @staticmethod
    def set_random_seed(seed):
        """ Set random seed for all subsequent operations. Should be used
        before population configuration to control this process as well.

        Parameters
        ----------
        seed : int
            Seed for RandomState

        """
        random.seed(seed)
        np.random.seed(seed)
        logging.info(f"Set simulation random seed to: {seed}")
