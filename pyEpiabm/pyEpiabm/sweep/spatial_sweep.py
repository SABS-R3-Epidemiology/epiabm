#
# Infection due to contact in between people in different cells
#

import random
import numpy as np

from pyEpiabm.core import Parameters
from pyEpiabm.property import InfectionStatus
from pyEpiabm.routine import SpatialInfection
from pyEpiabm.utility import DistanceFunctions

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

        # As this tracks intercell infections need to check number of
        # cells is more than one (edge case but worth having)
        if len(self._population.cells) == 1:
            return
        # Double loop over the whole population, checking infectiousness
        # status, and whether they are absent from their household.
        for cell in self._population.cells:
            # Check to ensure there is an infector in the cell
            total_infectors = cell.number_infectious()
            if total_infectors == 0:
                continue
            # Creates a list of posible infectee cells which excludes the
            # infector cell.
            possible_infectee_cells = self._population.cells.copy()
            possible_infectee_cells.remove(cell)
            possible_infectee_num = sum([cell2.compartment_counter.retrieve()
                                        [InfectionStatus.Susceptible]
                                        for cell2 in possible_infectee_cells])
            if possible_infectee_num == 0:
                # Break the loop if no people outside the cell are susceptible.
                continue
            # If there are any infectors calculate number of infection events
            # given out in total by the cell
            ave_num_of_infections = SpatialInfection.cell_inf(cell, timestep)
            number_to_infect = np.random.poisson(ave_num_of_infections)

            # Sample at random from the cell to find an infector. Have
            # checked to ensure there is an infector present.
            possible_infectors = [person for person in cell.persons
                                  if person.is_infectious()]
            infector = random.choice(possible_infectors)

            if Parameters.instance().do_CovidSim:
                # Chooses cells based on a cumulative transmission array
                # one and a time a tests each infection event.
                while number_to_infect > 0:
                    # Weighting for cell choice in Covidsim uses cum_trans and
                    # invCDF arrays, but really can't see how these are
                    # initialised. Have used the number of susceptible for now.
                    weights = [cell2.compartment_counter.retrieve()
                               [InfectionStatus.Susceptible]
                               for cell2 in possible_infectee_cells]
                    infectee_cell = random.choices(possible_infectee_cells,
                                                   weights=weights, k=1)[0]
                    # Sample at random from the infectee cell to find
                    # an infectee
                    infectee = random.sample(infectee_cell.persons, 1)[0]
                    infection_distance = DistanceFunctions.dist(
                     cell.location, infectee_cell.location) / Parameters.\
                        instance().infection_radius
                    if (infection_distance < random.random()):
                        # Covidsim rejects the infection event if the distance
                        # between infector/infectee is too large.
                        self.do_infection_event(infector, infectee, timestep)
                        number_to_infect -= 1

            else:
                # Chooses a list of cells (with replacement) for each infection
                # event to occur in. Specifically inter-cell infections
                # so can't be the same cell

                distance_weights = [1/DistanceFunctions.dist(
                                    cell.location, cell2.location)
                                    for cell2 in
                                    possible_infectee_cells]
                cell_list = random.choices(possible_infectee_cells,
                                           weights=distance_weights,
                                           k=number_to_infect)
                # Each infection event corresponds to a infectee cell
                # on the cell list
                for infectee_cell in cell_list:

                    # Sample at random from the infectee cell to find
                    # an infectee
                    infectee = random.sample(infectee_cell.persons, 1)[0]
                    self.do_infection_event(infector, infectee, timestep)

    def do_infection_event(self, infector, infectee,
                           timestep):
        """Helper function which takes an infector and infectee,
        in different cells and tests whether contact between
        them will lead to an infection event.

        :param infector: Infector
        :type infector: Person
        :param infectee: Infectee
        :type infectee: Person
        :param timestep: Current simulation timestep
        :type timestep: int
        """
        if not infectee.is_susceptible():
            return

        # force of infection specific to cells and people
        # involved in the infection event
        force_of_infection = SpatialInfection.\
            space_foi(infector.microcell.cell, infectee.microcell.cell,
                      infector, infectee, timestep)

        # Compare a uniform random number to the force of
        # infection to see whether an infection event
        # occurs in this timestep between the given
        # persons.
        r = random.random()
        if r < force_of_infection:
            infectee.microcell.cell.enqueue_person(infectee)
