#
# Sweep to update people present in a place
#

import random
import math
import numpy as np
import logging

from pyEpiabm.core import Parameters

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
        params = Parameters.instance().place_params
        for cell in self._population.cells:
            for place in cell.places:
                param_ind = place.place_type.value - 1
                if param_ind < len(params["mean_size"]):
                    # Checks whether values are present, otherwise uses
                    # defaults
                    mean_cap = params["mean_size"][param_ind]
                    max_cap = params["max_size"][param_ind]
                if place.place_type.name == "Workplace":
                    # Variable population is people not in the fixed pop.
                    # Held in the last group of the place.
                    # Changed at each timestep
                    place.empty_place(groups_to_empty=[-1])
                    candidate_list = [person for person in place.cell.persons
                                      if person not in place.persons]
                    self.update_place_group(place, group_index=-1,
                                            mean_capacity=mean_cap,
                                            max_capacity=max_cap,
                                            person_list=candidate_list)

                elif place.place_type.name == "OutdoorSpace":
                    place.empty_place()
                    self.update_place_group(place)

    def update_place_group(self, place, mean_capacity: float = 25,
                           max_capacity: int = 50,
                           group_size: int = 0, person_list: list = None,
                           person_weights: list = None):
        """Specific method to update people in a place or place group.

        Parameters
        ----------
        place : Place
            Place to change
        max_capacity : int
            Maximum people of in this place
        group_size: int
            Average size of the groups in each place
        person_list: list
            List of people that may be present in the place
        person_weights : list
            Weights for people in list
        """
        # If a specific list of people is not provided, use the whole cell
        if person_list is None:
            person_list = place.cell.persons

        # Ensure that the number of people put in the place
        # is at most its capacity or the total number of
        # people in the cell.
        new_capacity = np.random.lognormal(mean_capacity)
        if max_capacity > 0:
            # Covidsim data has some zeros for max capacity
            new_capacity = min(new_capacity, max_capacity, len(person_list))
        else:
            new_capacity = min(new_capacity, len(person_list))

        if len(person_list) <= 0:
            logging.warning("No people in the person list supplied.")
        count = 0

        try:
            num_groups = np.random.poisson(math.ceil(new_capacity/group_size))
        except ZeroDivisionError:
            num_groups = 1

        while count < new_capacity:
            if person_weights is not None:
                assert len(person_weights) == len(person_list),\
                    ('Weights given is a different size to the person list.')
                person = random.choices(person_list, person_weights, k=1)[0]
            else:
                i = random.randint(1, len(person_list))
                person = person_list[i-1]
            # Checks person is not already in the place, and that they
            # haven't already been assigned to this place type.
            if ((person not in place.persons) and
                    (place.place_type not in person.place_types)):

                place.add_person(person, random.randint(0, num_groups - 1))
                count += 1
