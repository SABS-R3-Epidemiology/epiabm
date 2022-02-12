#
# Factory for creation of a population based on an input file
#

import typing
import numpy as np
import pandas as pd
import random

from pyEpiabm.core import Household, Population
from pyEpiabm.property import PlaceType


class FilePopulationFactory:
    """ Class that creates a population  based on an input .csv file.
    """
    @staticmethod
    def make_pop(input_file: str, random_seed: int = None):
        """Initialize a population object from an input csv file, with one
        row per microcell. A uniform multinomial distribution is
        used to distribute the number of people into the different households
        within each microcell.

        Input file contains columns:
            * `cell`: ID code for cell (Uses hash if unspecified)
            * `microcell`: ID code for microcell (Uses hash if unspecified)
            * `household_number`: Number of households in that microcell
            * `place_number`: Number of places in each microcell
            * `population_seed`: Random seed for reproducible populations (*)

        :param input_file: Path to input file
        :type file_params: str
        :param random_seed: Seed for reproducible household distribution
        :type seed: int
        :return: Population object with individuals distributed into
            households
        :rtype: Population
        """
        # Unpack variables from input dictionary
        population_size = pop_params["population_size"]
        cell_number = pop_params["cell_number"]
        microcell_number = pop_params["microcell_number"]

        household_number = pop_params["household_number"] \
            if "household_number" in pop_params else 0
        place_number = pop_params["place_number"] \
            if "place_number" in pop_params else 0

        # If random seed is specified in parameters, set this in numpy
        if "population_seed" in pop_params:
            np.random.seed(pop_params["population_seed"])
            random.seed(pop_params["population_seed"])

        # Initialise a population class
        new_pop = Population()

        # Checks parameter type and stores as class objects.
        total_number_microcells = cell_number * microcell_number

        new_pop.add_cells(cell_number)
        # Sets up a probability array for the multinomial.
        p = [1 / total_number_microcells] * total_number_microcells
        # Multinomially distributes people into microcells.
        cell_split = np.random.multinomial(population_size, p, size=1)[0]
        i = 0
        for cell in new_pop.cells:
            cell.add_microcells(microcell_number)
            for microcell in cell.microcells:
                people_in_microcell = cell_split[i]
                microcell.add_people(people_in_microcell)
                i += 1

        # If a household number is given then that number of households
        # are initialised. If the household number defaults to zero
        # then no households are initialised.
        if household_number > 0:
            ToyPopulationFactory.add_households(new_pop, household_number)
        if place_number > 0:
            ToyPopulationFactory.add_places(new_pop, place_number)

        new_pop.setup()
        return new_pop

    @staticmethod
    def add_households(population: Population, household_number: int):
        """Groups people in a microcell into households together.

        :param population: Population containing all person objects to be
            considered for grouping
        :type population: Population
        :param household_number: Number of households to form
        :type household_number: int
        """
        # Initialises another multinomial distribution
        q = [1 / household_number] * household_number
        for cell in population.cells:
            for microcell in cell.microcells:
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
