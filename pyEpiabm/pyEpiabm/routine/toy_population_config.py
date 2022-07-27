#
# Factory for creation of a toy population
#

import typing
import logging
import numpy as np
import random
import math

from pyEpiabm.core import Household, Population, Parameters
from pyEpiabm.property import PlaceType
from pyEpiabm.utility import DistanceFunctions, log_exceptions

from .abstract_population_config import AbstractPopulationFactory


class ToyPopulationFactory(AbstractPopulationFactory):
    """ Class that creates a toy population for use in the simple
    python model.

    """
    @staticmethod
    @log_exceptions()
    def make_pop(pop_params: typing.Dict):
        """Initialize a population object with a given population size,
        number of cells and microcells. A uniform multinomial distribution is
        used to distribute the number of people into the different microcells.
        There is also an option to distribute people into households or places.

        file_params contains (with optional args as (*)):
            * `population_size`: Number of people in population
            * `cell_number`: Number of cells in population
            * `microcell_number`: Number of microcells in each cell
            * `household_number`: Number of households in each microcell (*)
            * `place_number`: Number of places in each microcell (*)
            * `population_seed`: Random seed for reproducible populations (*)

        Parameters
        ----------
        file_params : dict
            Dictionary of parameters for generating a population

        Returns
        -------
        Population
            Population object with individuals distributed into households

        """
        # Unpack variables from input dictionary
        population_size = pop_params["population_size"]
        cell_number = pop_params["cell_number"]
        microcell_number = pop_params["microcell_number"]

        household_number = pop_params["household_number"] \
            if "household_number" in pop_params else 0
        place_number = pop_params["place_number"] \
            if "place_number" in pop_params else 0

        # If random seed is specified in parameters, set this
        if "population_seed" in pop_params:
            np.random.seed(pop_params["population_seed"])
            random.seed(pop_params["population_seed"])
            logging.info("Set population random seed to:"
                         + str(pop_params["population_seed"]))

        # Initialise a population class
        new_pop = Population()

        # Checks parameter type and stores as class objects.
        total_number_microcells = cell_number * microcell_number

        new_pop.add_cells(cell_number)
        # Sets up a probability array for the multinomial.
        p = [1 / total_number_microcells] * total_number_microcells
        # Multinomially distributes people into microcells.
        cell_split = np.random.multinomial(population_size, p, size=1)[0]
        age_prop = Parameters.instance().age_proportions
        w = age_prop/sum(age_prop)
        # Split microcell into age groups

        i = 0
        for cell in new_pop.cells:
            cell.add_microcells(microcell_number)
            for microcell in cell.microcells:
                people_in_microcell = cell_split[i]
                microcell_split = np.random.multinomial(people_in_microcell,
                                                        w, size=1)[0]
                for age in range(len(age_prop)):
                    microcell.add_people(microcell_split[age], age_group=age)
                i += 1

        # If a household number is given then that number of households
        # are initialised. If the household number defaults to zero
        # then no households are initialised.
        if household_number > 0:
            ToyPopulationFactory.add_households(new_pop, household_number)
        if place_number > 0:
            ToyPopulationFactory.add_places(new_pop, place_number)

        logging.info(f"Toy Population Configured with {cell_number} cells")
        return new_pop

    @staticmethod
    def add_households(population: Population, household_number: int):
        """Groups people in a microcell into households together.

        Parameters
        ----------
        population : Population
            Population containing all person objects to be considered for
            grouping
        household_number : int
            Number of households to form

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

    @staticmethod
    def add_places(population: Population, place_number: int):
        """Generates places within a Population.

        Parameters
        ----------
        population : Population
            Population where :class:`Place` s will be added
        place_number : int
            Number of places to generate per :class:`Microcell`

        """
        # Unable to replicate CovidSim schools as this uses data not
        # available for all countries. Random dist used instead.
        # Cf. SetupModel.cpp L1463. (https://github.com/mrc-ide/
        # covid-sim/blob/1ada407d4b9c56a259fb6923353b8e55097d5a7c/
        # src/SetupModel.cpp#L1463)

        # As the population of a place is reconfigured in Update
        # Place Sweep, it is not necessary to initialise a population
        # in each place.
        for cell in population.cells:
            for microcell in cell.microcells:
                microcell.add_place(place_number, cell.location,
                                    random.choice(list(PlaceType)))

    @staticmethod
    def assign_cell_locations(population: Population, method: str = 'random'):
        """Assigns cell locations based on method provided. Possible methods:

            * 'random': Assigns all locations randomly within unit square
            * 'uniform_x': Spreads points evenly along x axis in range (0, 1)
            * 'grid': Distributes points according to a square grid within a \
               unit square. There will be cells missing in the last row \
               if the input is not a square number

        Parameters
        ----------
        population : Population
            Population containing all cells to be assigned locations
        method : str
            Method of determining cell locations

        """
        try:
            if method == "random":
                for cell in population.cells:
                    cell.set_location(tuple(np.random.rand(2)))
                    for microcell in cell.microcells:
                        while True:
                            # Will keep random location only if microcell
                            # is closer to its cell's location than any other.
                            # Not very efficient.
                            microcell.set_location(tuple(np.random.rand(2)))
                            cell_dist = (DistanceFunctions.dist(microcell.
                                         location, cell.location))
                            inter_dist = [DistanceFunctions.dist(microcell.
                                          location, cell2.location) for cell2
                                          in population.cells]
                            if min(inter_dist) == cell_dist:
                                break

            elif method == "uniform_x":
                cell_number = len(population.cells)
                x_pos = np.linspace(0, 1, cell_number)
                for i, cell in enumerate(population.cells):
                    cell.set_location((x_pos[i], 0))
                    mcell_number = len(cell.microcells)
                    y_pos = np.linspace(0, 1, mcell_number)
                    for j, microcell in enumerate(cell.microcells):
                        microcell.set_location((x_pos[i], y_pos[j]))

            elif method == "grid":
                cell_number = len(population.cells)
                grid_len = math.ceil(math.sqrt(cell_number))
                pos = np.linspace(0, 1, grid_len)
                for i, cell in enumerate(population.cells):
                    cell.set_location((pos[i % grid_len],
                                       pos[i // grid_len]))
                    mcell_num = len(cell.microcells)
                    mcell_len = math.ceil(math.sqrt(mcell_num))
                    m_pos = np.linspace(0, 1, mcell_len)
                    for j, microcell in enumerate(cell.microcells):
                        x = pos[i % grid_len] + \
                            (m_pos[j % mcell_len] - 0.5) / grid_len
                        y = pos[i // grid_len] + \
                            (m_pos[j // mcell_len] - 0.5) / grid_len
                        microcell.set_location((x, y))

            else:
                raise ValueError(f"Unknown method: '{method}' not recognised")

        except Exception as e:
            logging.exception(f"{type(e).__name__} in ToyPopulationFactory"
                              + ".assign_cell_locations()")
