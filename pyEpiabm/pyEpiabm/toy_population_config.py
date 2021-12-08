import numpy as np
from .population import Population


class ToyPopulation:
    """ Class that creates a toy population for use in the simple python model
    """
    def __init__(self, pop_size: int, cell_number: int,
                 microcell_per_cell: int):
        """Method that initializes a population class with a given population size,
        number of cells and number of microcells. A multinomial distribution is
        used to distribute the number of people into the different microcells.

        : param pop_size: Total number of people in population
        : type pop_size: int
        : param cell_number: Number of cell objects the population will be
          split in to
        : type cell_number: int
        : param microcell_per_cell: Number of microcell objects per cell
        : type microcell_per_cell: int
        """

        self.pop_size = pop_size
        self.population = Population()
        self.population.add_cells(cell_number)
        self.total_number_microcells = cell_number*microcell_per_cell

        p = [1/self.total_number_microcells]*self.total_number_microcells
        cell_split = np.random.multinomial(pop_size, p, size=1)[0]
        i = 0
        for cell in self.population.cells:
            cell.add_microcells(microcell_per_cell)
            for microcell in cell.microcells:
                people_in_microcell = cell_split[i]
                microcell.add_people(people_in_microcell)
                i += 1
