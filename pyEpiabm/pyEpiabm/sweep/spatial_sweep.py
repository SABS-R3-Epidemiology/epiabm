#
# Infection due to contact in between people in different cells
#

import random
import numpy as np

from pyEpiabm.core import Parameters
from pyEpiabm.routine import SpatialInfection

from .abstract_sweep import AbstractSweep


class SpatialSweep(AbstractSweep):
    """Class to run the inter-cell space infections
    as part of the sweep function. Runs through cells
    and calculates their infectiousness parameter and calculates
    a poisson variable of how many people each cell should
    infect. Then chooses other cells, and persons within that
    cell to assign as infectee. Then tests a infection event
    against each susceptible member of the place. The resulting
    exposed person is added to an infection queue.
    """

    def __call__(self, time: float):
        """
        Given a population structure, loops over cells and generates
        a random number of people to infect. Then decides which cells
        the infectees should be found in and considers whether an
        infection event occurs on individual and cell infectiousness
        and susceptibility.

        :param time: Current simulation time
        :type time: int
        """
        timestep = int(time * Parameters.instance().time_steps_per_day)
        # Double loop over the whole population, checking infectiousness
        # status, and whether they are absent from their household.
        for cell in self._population.cells:

            # As this tracks intercell infections need to check number of
            # cells is more than one (edge case but worth having)
            if len(self._population.cells) == 1:
                break

            # Check to ensure there is an infector in the cell
            total_infectors = cell.infectious_number()
            if total_infectors == 0:
                continue

            # If there is an infector calculate number of infection events
            # given out in total by the cell
            ave_num_of_infections = SpatialInfection.cell_inf(cell, timestep)
            number_to_infect = np.random.poisson(ave_num_of_infections)

            # Chooses a list of cells (with replacement) for each infection
            # event to occur in. Specifically inter-cell infections
            # so can't be the same cell
            possible_infectee_cells = self._population.cells.copy()
            possible_infectee_cells.remove(cell)
            cell_list = random.choices(possible_infectee_cells,
                                       k=number_to_infect)

            # Sample at random from the cell to find an infector. Have
            # checked to ensure there is an infector present.
            # THIS COULD BE V SLOW IF SMALL PROPORTION OF INFECTORS
            possible_infectors = [person for person in cell.persons
                                  if person.is_infectious()]
            infector = random.choice(possible_infectors)

            # Each infection event corresponds to a infectee cell
            # on the cell list
            for infectee_cell in cell_list:

                # Sample at random from the infectee cell to find
                # an infectee
                infectee = random.sample(infectee_cell.persons, 1)[0]
                if not infectee.is_susceptible():
                    continue

                # force of infection specific to cells and people
                # involved in the infection event
                force_of_infection = SpatialInfection.\
                    space_foi(cell, infectee_cell, infector, infectee)

                # Compare a uniform random number to the force of
                # infection to see whether an infection event
                # occurs in this timestep between the given
                # persons.
                r = random.random()

                if r < force_of_infection:
                    infectee_cell.enqueue_person(infectee)
