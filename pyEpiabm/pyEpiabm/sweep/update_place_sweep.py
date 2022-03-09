#
# Sweep to update people present in a place
#

import random
import numpy as np
import logging

from .abstract_sweep import AbstractSweep


class UpdatePlaceSweep(AbstractSweep):
    """Class to update people in the "Place"
    class.

    """
    def __call__(self, time: float):
        """Given a population structure, updates the people
        present in each place at a specific timepoint.

        Parameters
        ----------
        time : float
            Current simulation time

        """
        # Double loop over the whole population, clearing places
        # of the variable population and refilling them.

        # Can call a this line if being called in from file etc.
        # place_params = Parameters.instance().place_params
        for cell in self._population.cells:
            for place in cell.places:
                if place.place_type.value == 1:  # HOTEL
                    place.empty_place()
                    self.update_place_group(place)
                    # not sure how to handle this yet so
                    # just going to completely update each time
                    # as in the previous code

                elif place.place_type.value == 3:  # RESTAURANT
                    # Variable population is people not in the fixed pop.
                    # Changed at each timestep
                    print('here')
                    place.empty_place(groups_to_empty=[1])
                    candidate_list = [person for person in place.cell.persons
                                      if person not in place.person_groups[1]]
                    self.update_place_group(place, group_index=1,
                                            person_list=candidate_list)

                elif place.place_type.value == 4:  # OUTDOORS
                    place.empty_place()
                    self.update_place_group(place)

    def update_place_group(self, place, mean_capacity: float = 25,
                           max_capacity: int = 50,
                           group_index: int = 0, person_list: list = None):
        """Specific method to update people in a place or place group.

        :param place: Place to change
        :type place: Place
        :param max_capacity: Maximum people of this group in this place
        :type max_capacity: int
        :param group_index: Key for the person group dictionary
        :type group_index: int
        :param person_list: List of people that may be present in the cell
        :type person_list: list
        """
        # If a specific list of people is not provided, use the whole cell
        if person_list is None:
            person_list = place.cell.persons

        # Ensure that the number of people put in the place
        # is at most its capacity or the total number of
        # people in the cell.
        new_capacity = np.random.lognormal(mean_capacity)
        new_capacity = min(new_capacity, max_capacity, len(person_list))
        if len(person_list) <= 0:
            logging.warning("No people in the person list supplied.")
        count = 0
        while count < new_capacity:
            i = random.randint(1, len(person_list))
            person = person_list[i-1]
            # Checks person is not already in the place, and that they
            # haven't already been assigned to this place type.
            if ((person not in place.persons) and
                    (place.place_type not in person.place_types)):

                place.add_person(person_list[i-1], group_index)
                count += 1
