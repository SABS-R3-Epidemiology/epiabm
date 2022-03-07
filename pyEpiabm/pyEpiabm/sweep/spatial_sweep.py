#
# Infection due to contact in between people in different cells
#


import random
import numpy as np
import logging

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

        Parameters
        ----------
        time : float
            Current simulation time

        """
        timestep = int(time * Parameters.instance().time_steps_per_day)

        # As this tracks intercell infections need to check number of
        # cells is more than one (edge case but worth having)
        if len(self._population.cells) == 1:
            return
        # If infection radius is set to zero no infections will occur so
        # break immediately to save time.
        if Parameters.instance().infection_radius == 0:
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
            poss_susc_cells = self._population.cells.copy()
            poss_susc_cells.remove(cell)
            possible_infectee_num = sum([cell2.compartment_counter.retrieve()
                                        [InfectionStatus.Susceptible]
                                        for cell2 in poss_susc_cells])
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
                infectee_list = self.find_infectees_Covidsim(infector,
                                                             poss_susc_cells,
                                                             number_to_infect)
            else:
                infectee_list = self.find_infectees(cell,
                                                    poss_susc_cells,
                                                    number_to_infect)

            for infectee in infectee_list:
                self.do_infection_event(infector, infectee, timestep)

    def find_infectees(self, infector_cell, possible_infectee_cells,
                       number_to_infect):
        """Given a specific infector, a list of possible infectee cells,
        and the number of people needed to infect, follows a distance based
        implementation to create a list of infectees.

        Parameters
        ----------
        infector_cell : Cell
            Infector cell instance of Cell
        possible_infectee_cells : List
            List of possible cells to infect
        number_to_infect : int
            maximum number of people to infect

        Returns
        ----------
        infectee_list : List
            List of exposed people to test an infection event
        """
        infectee_list = []
        # Chooses a list of cells (with replacement) for each infection
        # event to occur in. Specifically inter-cell infections
        # so can't be the same cell.
        distance_weights = []
        for cell2 in possible_infectee_cells:
            try:
                distance_weights.append(1/DistanceFunctions.dist(
                            infector_cell.location, cell2.location))
            except ZeroDivisionError:
                # If cells are on top of each other use nan placeholder
                distance_weights.append(np.nan)
        # Cells on top of each currently have a distance weight equal
        # to the maximum of all other weights.
        # Possibly want to do twice this.
        number_of_nans = sum(np.isnan(distance_weights))
        if number_of_nans == len(distance_weights):
            distance_weights = [1 for _ in distance_weights]
        elif number_of_nans > 0:
            max_weight = np.nanmax(distance_weights)
            distance_weights = np.nan_to_num(distance_weights,
                                             nan=max_weight)
        # Use of the cutoff distance idea from CovidSim.
        cutoff = Parameters.instance().infection_radius
        distance_weights = [weight if (cutoff > 1/weight) else 0
                            for weight in distance_weights]
        # Will catch the case if distance weights isn't configured
        # correctly and returns the wrong length.
        assert len(distance_weights) == len(possible_infectee_cells), (
            "Distance weights are not the same length as cell list")

        try:
            # Will catch a list of zeros
            if sum(distance_weights) == 0:
                raise(ValueError)
            cell_list = random.choices(possible_infectee_cells,
                                       weights=distance_weights,
                                       k=number_to_infect)
        except ValueError as e:
            logging.exception(f"{type(e).__name__}: no cells"
                              + f" within radius {cutoff} of"
                              + f" cell {infector_cell.id} at location"
                              + f" {infector_cell.location} - skipping cell.")
            # This returns an empty list so no infection events tested.
            return infectee_list

        # Each infection event corresponds to a infectee cell
        # on the cell list
        for infectee_cell in cell_list:
            # Sample at random from the infectee cell to find
            # an infectee
            infectee_list.append(random.sample(infectee_cell.persons, 1)[0])
        return infectee_list

    def find_infectees_Covidsim(self, infector, possible_infectee_cells,
                                number_to_infect):
        """Given a specific infector, a list of possible infectee cells,
        and the number of people needed to infect, follows Covidsim's
        implementation to create a list of infectees.

        Parameters
        ----------
        infector : Person
            Infector instance of person
        possible_infectee_cells : List
            List of possible cells to infect
        number_to_infect : int
            maximum number of people to infect
        """
        infectee_list = []
        count = 0
        while number_to_infect > 0 and count < self._population.total_people():
            count += 1
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
            infection_distance = (DistanceFunctions.dist(
                infector.microcell.cell.location, infectee_cell.location) /
                Parameters.instance().infection_radius)
            if (infection_distance < random.random()):
                # Covidsim rejects the infection event if the distance
                # between infector/infectee is too large.
                infectee_list.append(infectee)
                number_to_infect -= 1
                # I can see an infinte loop here if there are no suitable
                # infectees. Have put in a count so no more loops than
                # total population.
        return infectee_list

    def do_infection_event(self, infector, infectee,
                           timestep):
        """Helper function which takes an infector and infectee,
        in different cells and tests whether contact between
        them will lead to an infection event.

        Parameters
        ----------
        infector : Person
            Infector instance of Person
        infectee : Person
            Infectee instance of Person
        timestep : int
            Current simulation timestep

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
