#
# Factory for creation of a population based on an input file
#

import numpy as np
import pandas as pd
import random

from pyEpiabm.core import Household, Population, Cell
from pyEpiabm.core.microcell import Microcell
from pyEpiabm.property import InfectionStatus


class FilePopulationFactory:
    """ Class that creates a population  based on an input .csv file.
    """
    @staticmethod
    def make_pop(input_file: str, random_seed: int = None):
        """Initialize a population object from an input csv file, with one
        row per microcell. A uniform multinomial distribution is
        used to distribute the number of people into the different households
        within each microcell. A random seed may be specified for reproducible
        populations.

        Input file contains columns:
            * `cell`: ID code for cell (Uses hash if unspecified)
            * `microcell`: ID code for microcell (Uses hash if unspecified)
            * `location_x`: The x coordinate of the parent cell location
            * `location_y`: The y coordinate of the parent cell location
            * `household_number`: Number of households in that microcell
            * Any number of columns with titles from the `InfectionStatus`
                enum (such as `InfectionStatus.Susceptible`), giving the
                number of people with that status in that cell

        :param input_file: Path to input file
        :type file_params: str
        :param random_seed: Seed for reproducible household distribution
        :type seed: int
        :return: Population object with individuals distributed into
            households
        :rtype: Population
        """
        # If random seed is specified in parameters, set this
        if random_seed is not None:
            np.random.seed(random_seed)
            random.seed(random_seed)

        # Read file into pandas dataframe
        input = pd.read_csv(input_file)
        loc_given = ("location_x" and "location_y" in input.columns.values)

        # Validate all column names in input
        valid_names = ["cell", "microcell", "location_x",
                       "location_y", "household_num"]
        for column in input.columns.values:  # Check all column headings
            if not (hasattr(InfectionStatus, column) | column in valid_names):
                raise ValueError(f"Unknown column heading '{column}' in input")

        # Initialise a population class
        new_pop = Population()

        # Iterate through lines (one per microcell)
        for i, line in input.iterrows():
            # Check if cell exists, or create it
            cell = FilePopulationFactory.find_cell(new_pop, line["cell"])

            if loc_given:
                location = (line["location_x"], line["location_y"])
                cell.set_location(location)

            # Raise error if microcell exists, then create new one
            for microcell in cell.microcells:
                if microcell.id == line["microcell"]:
                    raise ValueError(f"Duplicate microcells {microcell.id}"
                                     + f"in cell {cell.id}")

            new_microcell = Microcell()
            cell.microcells.append(new_microcell)
            new_microcell.set_id(line["microcell"])

            # Add people of each infection status - need to move after setup?
            for column in input.columns.values:
                if hasattr(InfectionStatus, column):
                    value = getattr(InfectionStatus, column)
                    new_microcell.add_people(input[column],
                                             InfectionStatus(value))

            # Add households to microcell
            if line["household_num"] > 0:
                FilePopulationFactory.add_households(new_pop,
                                                     line["household_num"])

        new_pop.setup()
        return new_pop

    @staticmethod
    def find_cell(population: Population, cell_id: float):
        """Returns cell with given ID in population, creates one if
        no cell with that ID exists.

        :param population: Population containing target cell
        :type population: Population
        :param cell_id: ID for target cell
        :type cell_id: float
        :return: Cell with given ID in population
        :rtype: Cell
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

        :param microcell: Microcell containing all person objects to be
            considered for grouping
        :type microcell: Microcell
        :param household_number: Number of households to form
        :type household_number: int
        """
        # Initialises another multinomial distribution
        q = [1 / household_number] * household_number
        people_number = len(microcell.persons)
        household_split = np.random.multinomial(people_number, q,
                                                size=1)[0]
        person_index = 0
        for j in range(household_number):
            people_in_household = household_split[j]
            new_household = Household()
            for _ in range(people_in_household):
                person = microcell.persons[person_index]
                new_household.add_person(person)
                person_index += 1
