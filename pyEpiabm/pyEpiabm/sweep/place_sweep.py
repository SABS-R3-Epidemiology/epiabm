#
# Infection due to contact in social spaces outside of households
#

import random
import numpy as np

from pyEpiabm.property import PlaceInfection

from .abstract_sweep import AbstractSweep


class PlaceSweep(AbstractSweep):
    """Class to run the place infections
    as part of the sweep function. Runs through infectious
    people within a cell and tests a infection event against each
    susceptible member of the place. The resulting
    exposed person is added to an infection queue.

    """
    def __call__(self, time: float):
        """
        Given a population structure with places, loops over infected
        members of the place and considers whether they infected other
        people present, based on individual and place infectiousness
        and susceptibility.

        Parameters
        ----------
        time : float
            Current simulation time

        """
        # Double loop over the whole population, checking infectiousness
        # status, and whether they are absent from their household.
        for cell in self._population.cells:
            for infector in cell.persons:
                if not infector.is_infectious():
                    continue
                place_list = [i[0] for i in infector.places]
                for place in place_list:
                    infector_group = place.get_group_index(infector)
                    infectiousness = PlaceInfection.place_inf(place, infector,
                                                              time)
                    # Covidsim only considers infectees in
                    # the group with the infector. I suggest we use this line
                    # to easily change the list of possible infectees.
                    possible_infectees = place.person_groups[infector_group]

                    # High infectiousness (>= 1) means all susceptible
                    # occupants become infected.
                    if infectiousness > 1:
                        for infectee in possible_infectees:
                            if not infectee.is_susceptible():
                                continue
                            cell.enqueue_person(infectee)

                    # Otherwise number of infectees is binomially
                    # distributed. Not sure if covidsim considers only
                    # susceptible place members. Makes sense to consider
                    # all possible occupants, and leave it to chance whether
                    # they are susceptible.
                    else:
                        num_infectees = np.random.binomial(
                            len(possible_infectees), infectiousness)

                        # Pick that number of potential infectees from place
                        # members.
                        potential_infectees = random.sample(
                            possible_infectees, num_infectees)

                        # Check to see whether a place member is susceptible.
                        for infectee in potential_infectees:

                            if not infectee.is_susceptible():
                                continue
                            # Calculate "force of infection" parameter which
                            # determines the likelihood of an infection event
                            # between the infector and infectee given that they
                            # meet in this place.

                            force_of_infection = PlaceInfection.\
                                place_foi(place, infector, infectee,
                                          time)

                            # Compare a uniform random number to the force of
                            # infection to see whether an infection event
                            # occurs in this timestep between the given
                            # persons.
                            r = random.uniform(0, 1)

                            if r < force_of_infection:
                                cell.enqueue_person(infectee)
