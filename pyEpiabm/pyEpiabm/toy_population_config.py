#
# Factory for creation of a toy population
#
import numpy as np
from .place_type import PlaceType
from .population import Population
from .household import Household


class ToyPopulationFactory:
    """ Class that creates a toy population for use in the simple
    python model.
    """
    def make_pop(self, population_size: int, cell_number: int,
                 microcell_number: int, household_number: int = 0,
                 place_number: int = 0):
        """Initialize a population object with a given population size,
        number of cells and microcells. A uniform multinomial distribution is
        used to distribute the number of people into the different microcells.
        There is also an option to distribute people into households or places.

        :param pop_size: Total number of people in population
        :type pop_size: int
        :param cell_number: Number of cell objects the population will be
            split into
        :type cell_number: int
        :param microcell_number: Number of microcell objects per cell
        :type microcell_number: int
        :param household_number: Number of households per microcell
        :type household_number: int
        :param place_number

        :return: Population object with individuals distributed into
            households
        :rtype: Population
        """
        # Initialise a population class
        new_pop = Population()

        # Checks parameter type and stores as class objects.

        total_number_microcells = cell_number * microcell_number

        new_pop.add_cells(cell_number)
        # Sets up a probability array for the multinomial.
        p = [1 / total_number_microcells] * total_number_microcells
        # Distributes multinomially people into microcells.
        cell_split = np.random.multinomial(population_size, p, size=1)[0]
        i = 0
        for cell in new_pop.cells:
            cell.add_microcells(microcell_number)
            for microcell in cell.microcells:
                people_in_microcell = cell_split[i]
                microcell.add_people(people_in_microcell)
                i += 1

        # If a household number is given then that number of households
        # are initialised. If the housrhold number defaults to zero
        # then no households are initialised.
        if household_number > 0:
            self.add_households(new_pop, household_number)
        if place_number > 0:
            self.add_places(new_pop, place_number)

        new_pop.setup()
        return new_pop

    def add_households(self, population: Population, household_number: int):
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

    def add_places(self, population: Population, place_number: int):
        """Groups people in a microcell into households together.

        :param population: Population containing all person objects to be
            considered for grouping
        :type population: Population
        :param place_number: Number of places to form
        :type place_number: int
        """
        # Further consideration of whether we initialise place types
        # at this step is needed.

        # As the population of a place is reconfigured in Update
        # Place Sweep, it is not necessary to initialise a population
        # in each place.
        for cell in population.cells:
            for microcell in cell.microcells:
                microcell.add_place(place_number, (1.0, 1.0),
                                    PlaceType.Hotel)
