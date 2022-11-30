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
                if place.place_type.name == "Workplace":
                    # Variable population is people not in the fixed pop.
                    # Held in the last group of the place.
                    # Changed at each timestep
                    group_ind = list(place.person_groups.keys())[-1]
                    place.empty_place(groups_to_empty=[group_ind])
                    person_list = [person for person in place.cell.persons
                                   if person not in place.persons]
                    self.update_place_group(place, group_index=group_ind,
                                            mean_capacity=mean_cap,
                                            person_list=person_list.copy())

                #elif place.place_type.name == "CareHome":
                #    group_ind = list(place.person_groups.keys())[0]
                #    place.empty_place(groups_to_empty=[group_ind])
                #    person_list = [person for person in place.cell.persons
                #                   if person not in place.persons]
                #    self.update_place_group(place, group_index=group_ind,
                #                            mean_capacity=mean_cap,
                #                            person_list=person_list.copy())

                elif place.place_type.name == "OutdoorSpace":
                    place.empty_place()
                    self.update_place_group(place)

    def update_place_group(self, place, mean_capacity: float = 25,
                           power_law_params: list = None,
                           group_index: int = None,
                           group_size: int = 0, person_list: list = None,
                           person_weights: list = None):
        """Specific method to update people in a place or place group.

        Parameters
        ----------
        place : Place
            Place to change
        mean_capacity : int
            Average number of people in this place
        power_law_params : list
            Should only be given for workplaces, contains the further
            parameters used to calculate place_size. List entries should
            take the order [Maximum size, Offset, Power]
        group_index : int
            If specified, the index of the group to be added to
        group_size: int
            Average size of the groups in each place
        person_list: list
            List of people that may be present in the place
        person_weights : list
            Weights for people in list
        """
        # If a specific list of people is not provided, use the whole cell
        if person_list is None:
            person_list = (place.cell.persons).copy()
        # Ensure that the number of people put in the place
        # is at most its capacity or the total number of
        # people in the cell. Will use a power law calculation if
        # parameters are provided, and a Poisson distribution is not.
        if power_law_params is None:
            new_capacity = np.random.poisson(mean_capacity)
        else:
            assert len(power_law_params) == 3, \
                ("Incorrect number of power law parameters given"
                 + " - should be of the form [maximum, offset, power]")
            [maximum, offset, power] = power_law_params
            s = (offset / (offset + maximum - 1)) ** power
            r = random.random()
            num = offset * ((1 - s) * r + s) ** (-1 / power) + 1 - offset
            new_capacity = math.floor(num)

        new_capacity = min(new_capacity, len(person_list))

        if len(person_list) <= 0:
            logging.info("No people in the person list supplied"
                         + " to update " + str(place))
            return
        if person_weights == [0 for _ in person_list]:
            logging.info("List of 0 weights given: no people"
                         + " of acceptable age for this place")
            return
        count = 0

        try:
            num_groups = np.random.poisson(math.ceil(new_capacity/group_size))
        except ZeroDivisionError:
            # Will occur when no group_size is set, if there are no groups
            # implemented in this place type
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
                if group_index is not None:
                    # If the index is specified
                    place.add_person(person, group_index)
                else:
                    # Add people randomly to any group within the place
                    place.add_person(person,
                                     random.randint(0, max(0, num_groups - 1)))
                count += 1

            # Prevent person being readded to list
            if person_weights is not None:
                person_weights.pop(person_list.index(person))
            person_list.remove(person)

            if len(person_list) <= 0:
                # logging.warning("Insufficient people in the person list"
                #                 + " supplied to update " + str(place))
                break

    def update_carehome_group(self, place, mean_capacity: float = 25,
                              power_law_params: list = None,
                              group_index: int = None,
                              group_size: int = 0, person_list: list = None,
                              person_weights: list = None):
        """Specific method to update people in a carehomes.

        Parameters
        ----------
        place : Place
            Place to change
        mean_capacity : int
            Average number of people in this place
        power_law_params : list
            Should only be given for workplaces, contains the further
            parameters used to calculate place_size. List entries should
            take the order [Maximum size, Offset, Power]
        group_index : int
            If specified, the index of the group to be added to
        group_size: int
            Average size of the groups in each place
        person_list: list
            List of people that may be present in the place
        person_weights : list
            Weights for people in list
        """
        carehome_params = Parameters.instance().carehome_params
        # If a specific list of people is not provided, use the whole cell
        if person_list is None:
            person_list = (place.cell.persons).copy()
        # Ensure that the number of people put in the place
        # is at most its capacity or the total number of
        # people in the cell. Will use a power law calculation if
        # parameters are provided, and a Poisson distribution is not.
        if power_law_params is None:
            new_capacity = np.random.poisson(mean_capacity)
        else:
            assert len(power_law_params) == 3, \
                ("Incorrect number of power law parameters given"
                 + " - should be of the form [maximum, offset, power]")
            [maximum, offset, power] = power_law_params
            s = (offset / (offset + maximum - 1)) ** power
            r = random.random()
            num = offset * ((1 - s) * r + s) ** (-1 / power) + 1 - offset
            new_capacity = math.floor(num)

        new_capacity = min(new_capacity, len(person_list))

        if len(person_list) <= 0:
            logging.info("No people in the person list supplied"
                         + " to update " + str(place))
            return
        if person_weights == [0 for _ in person_list]:
            logging.info("List of 0 weights given: no people"
                         + " of acceptable age for this place")
            return
        count = 0

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
            if person.age >= carehome_params["carehome_minimum_age"]:
                if ((person not in place.persons) and
                        (place.place_type not in person.place_types)):
                    place.add_person(person, 1)
                    person.care_home_resident = 1
                count += 1
            elif person.age < carehome_params["carehome_minimum_age"]:
                if ((person not in place.persons) and
                        (place.place_type not in person.place_types)):
                    place.add_person(person, 0)
                    person.key_worker = 1
                count += 1
            # Prevent person being readded to list
            if person_weights is not None:
                person_weights.pop(person_list.index(person))
            person_list.remove(person)

            if len(person_list) <= 0:
                # logging.warning("Insufficient people in the person list"
                #                 + " supplied to update " + str(place))
                break
