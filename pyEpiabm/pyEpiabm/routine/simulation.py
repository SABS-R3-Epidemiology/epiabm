#
# Simulates a complete pandemic
#

import random
import os
import logging
import typing
import numpy as np
from tqdm import tqdm

from pyEpiabm.core import Parameters, Population
from pyEpiabm.output import _CsvDictWriter
from pyEpiabm.output import AbstractReporter
from pyEpiabm.property import InfectionStatus
from pyEpiabm.sweep import AbstractSweep
from pyEpiabm.utility import log_exceptions


class Simulation:
    """Class to run a full simulation.

    """

    def __init__(self):
        """ Constructor
        """
        self.writers = []

    @log_exceptions()
    def configure(self,
                  population: Population,
                  initial_sweeps: typing.List[AbstractSweep],
                  sweeps: typing.List[AbstractSweep],
                  sim_params: typing.Dict,
                  file_params: typing.Dict,
                  ih_file_params: typing.Dict = None):
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
            * `age_stratified`: Boolean to determine whether the output will \
                be age stratified

        ih_file_params Contains:
            * `output_dir`: String for the location for the output files, \
               as a relative path
            * `status_output`: Boolean to determine whether we need \
               a csv file containing infection status values
            * `infectiousness_output`: Boolean to determine whether we need \
               a csv file containing infectiousness (viral load) values

        Parameters
        ----------
        population : Population
            Population structure for the model
        pop_params : dict
            Dictionary of parameter specific to the population
        initial_sweeps : typing.List
            List of sweeps used to initialise the simulation
        sweeps : typing.List
            List of sweeps used in the simulation. Queue sweep and host
            progression sweep should appear at the end of the list
        sim_params : dict
            Dictionary of parameters specific to the simulation used and used
            as input for call method of initial sweeps
        file_params : dict
            Dictionary of parameters specific to the output file
        ih_file_params : dict
            Dictionary of parameters specific to the output infection history
            file. If both `status_output` and `infectiousness_output` are
            False, then no infection history csv files are produced (or if
            the dictionary is None)
        """
        self.sim_params = sim_params
        self.population = population
        self.initial_sweeps = initial_sweeps
        self.sweeps = sweeps

        self.spatial_output = file_params["spatial_output"] \
            if "spatial_output" in file_params else False

        self.age_stratified = file_params["age_stratified"] \
            if "age_stratified" in file_params else False

        Parameters.instance().use_ages = self.age_stratified

        # If random seed is specified in parameters, set this in numpy
        if "simulation_seed" in self.sim_params:
            Simulation.set_random_seed(self.sim_params["simulation_seed"])

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

        filename = file_params["output_file"]
        logging.info(
            f"Set output location to {os.path.join(folder, filename)}")

        # Setting up writer for infection status distribution for each cell
        output_titles = ["time"] + [s for s in InfectionStatus]
        if self.spatial_output:
            output_titles.insert(1, "cell")
            output_titles.insert(2, "location_x")
            output_titles.insert(3, "location_y")

        if self.age_stratified:
            output_titles.insert(1, "age_group")

        self.writer = _CsvDictWriter(
            folder, filename,
            output_titles)

        self.status_output = False
        self.infectiousness_output = False
        self.ih_status_writer = None
        self.ih_infectiousness_writer = None

        if ih_file_params:
            # Setting up writer for infection history for each person. If the
            # ih_file_params dict is empty, then we do not need to record this
            self.status_output = ih_file_params["status_output"] \
                if "status_output" in ih_file_params else False

            self.infectiousness_output = ih_file_params["infectiousness_output"] \
                if "infectiousness_output" in ih_file_params else False
            person_ids = []
            for cell in population.cells:
                person_ids += [person.id for person in cell.persons]
            self.ih_output_titles = ["time"] + person_ids
            ih_folder = os.path.join(os.getcwd(),
                                     ih_file_params["output_dir"])

            if self.status_output:

                ih_file_name = "ih_status_output.csv"
                logging.info(
                    f"Set infection history infection status location to "
                    f"{os.path.join(ih_folder, ih_file_name)}")

                self.ih_status_writer = _CsvDictWriter(
                    ih_folder, ih_file_name,
                    self.ih_output_titles
                )

            if self.infectiousness_output:

                ih_file_name = "ih_infectiousness_output.csv"
                logging.info(
                    f"Set infection history infectiousness location to "
                    f"{os.path.join(ih_folder, ih_file_name)}")

                self.ih_infectiousness_writer = _CsvDictWriter(
                    ih_folder, ih_file_name,
                    self.ih_output_titles
                )

    @log_exceptions()
    def run_sweeps(self):
        """Iteration step of the simulation. First the initialisation sweeps
        configure the population on the first timestep. Then at each
        subsequent timestep the sweeps run, updating the population. At each
        timepoint, a count of each infection status is written to file. Note
        that the elements of initial sweeps take the sim_params dict as an
        argument for their call method but the elements of sweeps take time
        as an argument for their call method.

        """
        # Define time step between sweeps
        ts = 1 / Parameters.instance().time_steps_per_day
        # Initialise on the time step before starting.
        for sweep in self.initial_sweeps:
            sweep(self.sim_params)
        logging.info("Initial Sweeps Completed at time "
                     + f"{self.sim_params['simulation_start_time']} days")
        # First entry of the data file is the initial state
        self.write_to_file(self.sim_params["simulation_start_time"])

        for t in tqdm(np.arange(self.sim_params["simulation_start_time"] + ts,
                                self.sim_params["simulation_end_time"] + ts,
                                ts)):
            for sweep in self.sweeps:
                sweep(t)
            self.write_to_file(t)
            if self.ih_status_writer:
                self.write_to_ih_file(t, output_option="status")
            if self.ih_infectiousness_writer:
                self.write_to_ih_file(t, output_option="infectiousness")
            for writer in self.writers:
                writer.write(t, self.population)
            logging.debug(f'Iteration at time {t} days completed')

        logging.info(f"Final time {t} days reached")

    def write_to_file(self, time):
        """Records the count number of a given list of infection statuses
        and writes these to file.

        Parameters
        ----------
        time : float
            Time of output data

        """
        if Parameters.instance().use_ages:
            nb_age_groups = len(Parameters.instance().age_proportions)
        else:
            nb_age_groups = 1
        if Parameters.instance().use_ages:
            if self.spatial_output:  # Separate output line for each cell
                for cell in self.population.cells:
                    for age_i in range(0, nb_age_groups):
                        data = {s: 0 for s in list(InfectionStatus)}
                        for inf_status in data:
                            data_per_inf_status = \
                                cell.compartment_counter.retrieve()[inf_status]
                            data[inf_status] += data_per_inf_status[age_i]
                        # Age groups are numbered from 1 to the total number
                        # of age groups (thus the +1):
                        data["age_group"] = age_i + 1
                        data["time"] = time
                        data["cell"] = cell.id
                        data["location_x"] = cell.location[0]
                        data["location_y"] = cell.location[1]
                        self.writer.write(data)
            else:  # Summed output across all cells in population
                data = {s: 0 for s in list(InfectionStatus)}
                for cell in self.population.cells:
                    for age_i in range(0, nb_age_groups):
                        for inf_status in list(InfectionStatus):
                            data_per_inf_status = \
                                cell.compartment_counter.retrieve()[inf_status]
                            data[inf_status] += data_per_inf_status[age_i]
                        data["age_group"] = age_i + 1
                        data["time"] = time
                        self.writer.write(data)
        else:  # If age not considered, age_group not written in csv
            if self.spatial_output:  # Separate output line for each cell
                for cell in self.population.cells:
                    data = {s: 0 for s in list(InfectionStatus)}
                    for k in data:
                        data[k] += sum(cell.compartment_counter.retrieve()[k])
                    data["time"] = time
                    data["cell"] = cell.id
                    data["location_x"] = cell.location[0]
                    data["location_y"] = cell.location[1]
                    self.writer.write(data)
            else:  # Summed output across all cells in population
                data = {s: 0 for s in list(InfectionStatus)}
                for cell in self.population.cells:
                    for k in data:
                        # Sum across age compartments
                        data[k] += sum(cell.compartment_counter.retrieve()[k])
                data["time"] = time
                self.writer.write(data)

    def write_to_ih_file(self, time, output_option: str):
        """Records the infection history of the individual people
        and writes these to file.

        Parameters
        ----------
        time : float
            Time of output data
        output_options : str
            Determines if you write data of infection status where \
            output_option="status" and/or infectiousness where \
            output_option="infectiousness"

        """
        if self.status_output:
            ih_data = {column: 0 for column in
                       self.ih_status_writer.writer.fieldnames}
            infect_data = {column: 0 for column in
                       self.ih_status_writer.writer.fieldnames}
            if self.infectiousness_output:
                for cell in self.population.cells:
                    for person in cell.persons:
                        if output_option == "status":
                            ih_data[person.id] = person.infection_status.value
                        elif output_option == "infectiousness":
                            infect_data[person.id] = person.infectiousness
                ih_data["time"] = time
                infect_data["time"] = time
                self.ih_status_writer.write(ih_data)
                self.ih_infectiousness_writer.write(infect_data)
            else:
                for cell in self.population.cells:
                    for person in cell.persons:
                        ih_data[person.id] = person.infection_status.value
                ih_data["time"] = time
                self.ih_status_writer.write(ih_data)
        else:
            if self.infectiousness_output:
                data = {column: 0 for column in
                        self.ih_infectiousness_writer.writer.fieldnames}
                for cell in self.population.cells:
                    for person in cell.persons:
                        data[person.id] = person.infectiousness
                data["time"] = time
                self.ih_infectiousness_writer.write(data)

    def add_writer(self, writer: AbstractReporter):
        self.writers.append(writer)

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
