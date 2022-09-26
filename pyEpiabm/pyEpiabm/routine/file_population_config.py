#
# Factory for creation of a population based on an input file
#

import numpy as np
import pandas as pd
import random
import copy
import logging
from packaging import version

from pyEpiabm.core import Cell, Household, Microcell, Person, Population
from pyEpiabm.property import InfectionStatus, PlaceType
from pyEpiabm.sweep import HostProgressionSweep
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
        input = pd.read_csv(input_file)
        loc_given = ("location_x" and "location_y" in input.columns.values)

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

        # Iterate through lines (one per microcell)
        for _, line in input.iterrows():
            # Check if cell exists, or create it
            cell = FilePopulationFactory.find_cell(new_pop, line["cell"])

            if loc_given:
                location = (line["location_x"], line["location_y"])
                cell.set_location(location)

            # Raise error if microcell exists, then create new one
            for microcell in cell.microcells:
                if microcell.id == line["microcell"]:
                    raise ValueError(f"Duplicate microcells {microcell.id}"
                                     + f" in cell {cell.id}")

            new_microcell = Microcell(cell)
            cell.microcells.append(new_microcell)
            new_microcell.set_id(line["microcell"])

            for column in input.columns.values:
                if hasattr(InfectionStatus, column):
                    value = getattr(InfectionStatus, column)
                    for i in range(int(line[column])):
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

            # Add households and places to microcell
            if ('household_number' in line) and (line["household_number"]) > 0:
                households = int(line["household_number"])
                FilePopulationFactory.add_households(new_microcell,
                                                     households)

            if ('place_number' in line) and (line["place_number"]) > 0:
                new_microcell.add_place(int(line["place_number"]),
                                        cell.location,
                                        random.choice(list(PlaceType)))

        # Verify all people are logged in cell
        for cell in new_pop.cells:
            mcell_persons = [person for mcell in cell.microcells
                             for person in mcell.persons]
            cell.persons = list(set(cell.persons) | set(mcell_persons))

        logging.info(f"New Population from file {input_file} configured")
        return new_pop

    @staticmethod
    def find_cell(population: Population, cell_id: float):
        """Returns cell with given ID in population, creates one if
        no cell with that ID exists.

        Parameters
        ----------
        population : Population
            Population containing target cell
        cell_id : float
            ID for target cell

        Returns
        -------
        Cell
            Cell with given ID in population

        """
        for cell in population.cells:
            if cell.id == cell_id:
                return cell
        new_cell = Cell()
        population.cells.append(new_cell)
        new_cell.set_id(cell_id)
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
        people_number = len(microcell.persons)
        household_split = np.random.multinomial(people_number, q,
                                                size=1)[0]
        person_index = 0
        for j in range(household_number):
            people_in_household = household_split[j]
            new_household = Household(loc=microcell.location)
            for _ in range(people_in_household):
                person = microcell.persons[person_index]
                new_household.add_person(person)
                person_index += 1

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

                households = []
                for person in microcell.persons:
                    status = str(person.infection_status.name)
                    if status in data_dict:
                        data_dict[status] += 1
                    else:  # New status
                        data_dict[status] = 1
                    if person.household not in households:
                        households.append(person.household)
                data_dict['household_number'] = len(households)
                data_dict['place_number'] = len(microcell.places)

                new_row = pd.DataFrame(data=data_dict, columns=columns,
                                       index=[0])
                df = pd.concat([df, new_row], ignore_index=True)

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
