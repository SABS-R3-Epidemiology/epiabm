#
# Sweep to update people present in a place
#

import random
import numpy as np

from .abstract_sweep import AbstractSweep


class UpdatePlaceSweep(AbstractSweep):
    """Class to update people in the "Place"
    class.
    """
    def __call__(self, time: int):
        """Given a population structure, updates the people
        present in each place at a specific timepoint.

        :param time: Current simulation time
        :type time: int
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
                elif place.place_type.value == 1:  # CAREHOME
                    if not place.initialised:
                        # Initialise the fixed population of workers
                        max_cap = 10  # for example, would actually come in
                        # from a dictionary
                        self.update_place_group(place, group_index=0)
                        max_residents = 100
                        self.update_place_group(place,
                                                max_capacity=max_residents,
                                                group_index=1)
                        place.initialised = True

                elif place.place_type.value == 3:  # RESTAURANT
                    if not place.initialised:
                        # Initialise the fixed population
                        max_cap = 10
                        self.update_place_group(place, max_capacity=max_cap,
                                                group_index=0)
                        place.initialised = True
                    # Variable population is people not in the fixed pop.
                    # Changed at each timestep
                    place.empty_place(1)
                    person_list = [person for person in place.cell.persons if
                                   person not in place.person_groups[1]]
                    self.update_place_group(place, group_index=1,
                                            person_list=person_list)

                elif place.place_type.value == 4:  # OUTDOORS
                    place.empty_place()
                    self.update_place_group(place)

                elif place.place_type.value == 5:  # WORKSPACE
                    # Fixed population is initialised on first run
                    if place.initialised:
                        continue
                    group_num = 5  # again would be an exterior param
                    group_size = 20
                    # thinking of making sure people don't have more than one
                    # workplace
                    person_list = place.cell.persons
                    for i in range(group_num):
                        self.update_place_group(place, group_index=i,
                                                person_list=person_list,
                                                max_capacity=group_size)
                    place.initialised = True

    def update_place_group(place, max_capacity: int = 50, group_index: int = 0,
                           person_list: list = None):
        """Specific method to update people in a place or place group.

        :param place: Place to change
        :type place: Place
        :param max_capacity: maximum people of this group in this place
        :type max_capacity: int
        :param group_index: key for the person group dictionary
        :type group_index: int
        :param person_list: list of people that may be present in the cell
        :type person_list: list
        """
        # If a specific list of people is not provided, use the whole cell
        if person_list is None:
            person_list = place.cell.persons

        # Ensure that the number of people put in the place
        # is at most its capacity or the total number of
        # people in the cell.
        max_capacity = np.minimum(max_capacity, len(person_list))
        new_capacity = random.randint(1, max_capacity)
        count = 0
        while count < new_capacity:
            i = random.randint(1, len(person_list))
            # Checks person is not already in the place.
            if person_list[i-1] not in place.persons:
                place.add_person(person_list[i-1], group_index)
                count += 1
