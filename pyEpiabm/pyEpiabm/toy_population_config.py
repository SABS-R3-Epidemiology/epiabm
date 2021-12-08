import numpy as np
from .population import Population
from .household import Household


class ToyPopulation:
    """ Class that creates a toy population for use in the simple python model.
    """
    def __init__(self, pop_size: int, cell_number: int,
                 microcell_per_cell: int, household_number: int,
                 if_households=False):
        """Method that initializes a population class with a given population size,
        number of cells and number of microcells. A multinomial distribution is
        used to distribute the number of people into the different microcells.
        There is also an option to distribute people into households.

        : param pop_size: Total number of people in population.
        : type pop_size: int
        : param cell_number: Number of cell objects the population will be
          split in to.
        : type cell_number: int
        : param microcell_per_cell: Number of microcell objects per cell.
        : type microcell_per_cell: int
        : param household_number: Number of households per microcell.
        : type household_number: int
        : param if_households: decides whether to put people into households.
        : type if_households: bool
        """
        if not (type(if_households) == bool):
            raise TypeError('Include household input needs to be boolean')
        self.pop_size = pop_size
        self.population = Population()
        self.population.add_cells(cell_number)
        self.total_number_microcells = cell_number*microcell_per_cell
        self.if_households = if_households
        self.household_number = household_number

        p = [1/self.total_number_microcells]*self.total_number_microcells
        cell_split = np.random.multinomial(pop_size, p, size=1)[0]
        i = 0
        for cell in self.population.cells:
            cell.add_microcells(microcell_per_cell)
            for microcell in cell.microcells:
                people_in_microcell = cell_split[i]
                microcell.add_people(people_in_microcell)
                i += 1

        if self.if_households:
            self.add_households()
        else:
            for cells in self.population.cells:
                for person in cells.persons:
                    new_household = Household()
                    new_household.add_person(person)

    def add_households(self):
        """Method that groups people in microcell into households together.
        """
        q = [1/self.household_number]*self.household_number
        for cell in self.population.cells:
            for microcell in cell.microcells:
                people_number = len(microcell.persons)
                household_split = np.random.multinomial(people_number, q,
                                                        size=1)[0]
                person_index = 0
                for j in range(self.household_number):
                    people_in_household = household_split[j]
                    new_household = Household()
                    for k in range(people_in_household):
                        person = microcell.persons[person_index]
                        new_household.add_person(person)
                        person_index += 1
