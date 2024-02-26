#
# Factory for creation of a population based on an input file
#

import numpy as np
import pandas as pd
import random
import copy
import logging
from packaging import version

from pyEpiabm.core import Cell, Microcell, Person, Population, Parameters
from pyEpiabm.property import InfectionStatus, PlaceType
from pyEpiabm.sweep import HostProgressionSweep, InitialHouseholdSweep
from pyEpiabm.utility import log_exceptions


class FilePopulationFactory:
    """ Class that creates a population based on an input .csv file.
    """
    @staticmethod
    @log_exceptions()
    def make_pop(input_file: str, random_seed: int = None, time: float = 0):
        """Initialize a population object from an input csv file, with one
        row per microcell. A uniform multinomial distribution is
        used to distribute the number of people into the different households
        within each microcell. A random seed may be specified for reproducible
        populations.

        Input file contains columns:

            * `cell`: ID code for cell
            * `microcell`: ID code for microcell
            * `location_x`: The x coordinate of the parent cell location
            * `location_y`: The y coordinate of the parent cell location
            * `household_number`: Number of households in that microcell
            * `place_number`: Number of places in that microcell
            * Any number of columns with titles from the `InfectionStatus` \
              enum (such as `InfectionStatus.Susceptible`), giving the \
              number of people with that status in that cell


        Parameters
        ----------
        input_file : str
            Path to input file
        random_seed : int
            Seed for reproducible household and place distribution
        time : float
            Start time of simulation where this population is used (default 0)

        Returns
        -------
        Population
            Population object with individuals distributed into households

        """
        # If random seed is specified in parameters, set this
        if random_seed is not None:
            np.random.seed(random_seed)
            random.seed(random_seed)
            logging.info(f"Set population random seed to: {random_seed}")

        # Read file into pandas dataframe
        input = pd.read_csv(filepath_or_buffer=input_file, dtype={"cell": int,
                            "microcell": int})
        loc_given = ("location_x" and "location_y" in input.columns.values)
        # Sort csv on cell and microcell ID
        input = input.sort_values(by=["cell", "microcell"])

        # Validate all column names in input
        valid_names = ["cell", "microcell", "location_x",
                       "location_y", "household_number", "place_number"]
        for col in input.columns.values:  # Check all column headings
            if not ((col in valid_names) or hasattr(InfectionStatus, col)):
                raise ValueError(f"Unknown column heading '{col}'")

        # Initialise a population class
        new_pop = Population()

        # Initialise sweep to assign new people their next infection status
        host_sweep = HostProgressionSweep()

        # Store current cell
        current_cell = None
        # Iterate through lines (one per microcell)
        for line in input.itertuples():
            # Converting from float to string
            cell_id_csv = str(line.cell)
            microcell_id_csv = cell_id_csv + "." + str(line.microcell)

            # Check if cell exists, or create it
            cell = FilePopulationFactory.find_cell(new_pop, cell_id_csv,
                                                   current_cell)
            if current_cell != cell:
                current_cell = cell

            if loc_given:
                location = (line.location_x, line.location_y)
                cell.set_location(location)

            # Raise error if microcell exists, then create new one
            microcell_ids = [microcell.id for microcell in cell.microcells]
            if microcell_id_csv in microcell_ids:
                raise ValueError(f"Duplicate microcells: {microcell_id_csv}"
                                 + f" already exists in cell {cell.id}")

            new_microcell = Microcell(cell)
            new_microcell.set_id(microcell_id_csv)
            cell.microcells.append(new_microcell)

            for column in input.columns.values:
                if hasattr(InfectionStatus, column):
                    value = getattr(InfectionStatus, column)
                    for _ in range(int(getattr(line, column))):
                        person = Person(new_microcell)
                        person.set_random_age()
                        new_microcell.add_person(person)
                        person.update_status(InfectionStatus(value))
                        if (person.infection_status
                                == InfectionStatus.Susceptible):
                            continue  # Next status set upon infection
                        host_sweep.update_next_infection_status(person)
                        host_sweep.update_time_status_change(person, time)
                        if str(person.infection_status).startswith('Infect'):
                            HostProgressionSweep.set_infectiousness(person,
                                                                    time)
                            person.increment_num_times_infected()

            # Add households and places to microcell
            if len(Parameters.instance().household_size_distribution) == 0:
                if (hasattr(line, 'household_number') and
                        line.household_number > 0):
                    households = int(line.household_number)
                    FilePopulationFactory.add_households(new_microcell,
                                                         households)

            if hasattr(line, 'place_number') and line.place_number > 0:
                for _ in range(int(line.place_number)):
                    new_microcell.add_place(1, cell.location,
                                            random.choice(list(PlaceType)))

        # if household_size_distribution parameters are available use
        # appropriate function
        if len(Parameters.instance().household_size_distribution) != 0:
            InitialHouseholdSweep().household_allocation(new_pop)

        # Verify all people are logged in cell
        for cell in new_pop.cells:
            updated_persons = [person for mcell in cell.microcells
                               for person in mcell.persons]
            assert len(updated_persons) == len(cell.persons), \
                "Person gone missing in microcell allocation"

        logging.info(f"New Population from file {input_file} configured")
        return new_pop

    @staticmethod
    def find_cell(population: Population, cell_id: str, current_cell: Cell):
        """Returns cell with given ID in population, creates one if
        current cell has another ID. As input is sorted on cell no
        cell will exist with that ID.

        Parameters
        ----------
        population : Population
            Population containing target cell
        cell_id : str
            ID for target cell
        current_cell : Cell or None
            Cell object of current cell

        Returns
        -------
        Cell
            Cell with given ID in population

        """
        if (current_cell is not None) and (current_cell.id == cell_id):
            return current_cell
        new_cell = Cell()
        population.cells.append(new_cell)
        new_cell.set_id(cell_id, population.cells)
        return new_cell

    @staticmethod
    def add_households(microcell: Microcell, household_number: int):
        """Groups people in a microcell into households together.

        Parameters
        ----------
        microcell : Microcell
            Microcell containing all person objects to be considered
            for grouping
        household_number : int
            Number of households to form
        """
        # Initialises another multinomial distribution
        q = [1 / household_number] * household_number
        people_list = microcell.persons.copy()
        people_number = len(people_list)
        household_split = np.random.multinomial(people_number, q,
                                                size=1)[0]
        for j in range(household_number):
            people_in_household = household_split[j]
            household_people = []
            for i in range(people_in_household):
                person_choice = people_list[0]
                people_list.remove(person_choice)
                household_people.append(person_choice)
            microcell.add_household(household_people)

    @staticmethod
    @log_exceptions()
    def print_population(population: Population, output_file: str):
        """Outputs population as .csv file, in format usable by the make_pop()
        method. Used for verification, or saving current simulation state. Note
        the current household distribution is random, and so the seed for
        household allocation must also be recorded to precisely save the
        simulation state.

        WARNING: This function is only tested with versions of pandas > 1.4,
        and may not function correctly in older cases. This will include cases
        where the user is running python 3.7 or older versions.

        Parameters
        ----------
        population : Population
            Population object to output
        output_file: str
            Path to output file

        """
        if version.parse(pd.__version__) < version.parse("1.4.0"):
            logging.warning(f"Pandas version {pd.__version__} is outdated,"
                            + " only tests version 1.4 and above.")

        columns = ['cell', 'microcell', 'location_x', 'location_y',
                   'household_number', 'place_number']
        for status in InfectionStatus:
            columns.append(str(status.name))
        df = pd.DataFrame(columns=columns)

        for cell in population.cells:
            for microcell in cell.microcells:
                data_dict = {
                    "cell": cell.id,
                    "microcell": microcell.id,
                    "location_x": cell.location[0],
                    "location_y": cell.location[1],
                }

                inf_dict = {str(status.name): 0 for status in InfectionStatus}
                data_dict.update(inf_dict)

                for person in microcell.persons:
                    status = str(person.infection_status.name)
                    data_dict[status] += 1

                data_dict['household_number'] = len(microcell.households)
                data_dict['place_number'] = len(microcell.places)

                new_row = pd.DataFrame(data=data_dict, columns=columns,
                                       index=[0])
                df = pd.concat([df, new_row], ignore_index=True) \
                    if df.size else new_row

        df['household_number'] = df['household_number'].astype(int)
        df['place_number'] = df['place_number'].astype(int)
        for status in InfectionStatus:
            df[str(status.name)] = df[str(status.name)].fillna(0)\
                .astype(int)
            if (df[str(status.name)] == 0).all():  # Delete unused statuses
                df.drop(columns=str(status.name), inplace=True)
        output_df = copy.copy(df)  # To access dataframe in testing
        output_df.to_csv(output_file, header=True, index=False)
        logging.info(f"Population saved to location {output_file}")
