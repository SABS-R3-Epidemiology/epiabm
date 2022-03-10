#
# Sweep to initialise people present in a place
#

import numpy as np

from .abstract_sweep import AbstractSweep
from .update_place_sweep import UpdatePlaceSweep
from pyEpiabm.core import Parameters
from pyEpiabm.property import PlaceType


class InitialisePlaceSweep(AbstractSweep):
    """Class to update people in the "Place"
    class.
    """
    def __call__(self):
        """Given a population structure, updates the people
        present in each place at a specific timepoint.

        :param time: Current simulation time
        :type time: int
        """

        # Double loop over the whole population, clearing places
        # of the variable population and refilling them.

        # May want a param dict to be called in from file etc.
        # place_params = Parameters.instance().place_params
        helper = UpdatePlaceSweep()
        helper.bind_population(self._population)
        params = Parameters.instance().place_params
        schools = [PlaceType.PrimarySchool, PlaceType.SecondarySchool,
                   PlaceType.SixthForm]
        for cell in self._population.cells:
            for place in cell.places:
                param_ind = place.place_type.value - 1
                if param_ind < len(params["mean_size"]):
                    # Checks whether values are present, otherwise uses
                    # defaults
                    # nearest_places = params["nearest_places"][param_ind]
                    mean_cap = params["mean_size"][param_ind]
                    max_cap = params["max_size"][param_ind]
                    ave_group_number = params["mean_num_groups"][param_ind]
                    group_num = np.random.poisson(ave_group_number) + 1
                    [person_list, weights] = self.create_age_weights(place,
                                                                     params)

                if place.place_type.name in schools:  # schools
                    # Initialise the fixed population

                    helper.update_place_group(place, person_list=person_list,
                                              person_weights=weights,
                                              mean_capacity=mean_cap,
                                              max_capacity=max_cap,
                                              group_index=0)

                elif place.place_type.name == PlaceType.Workplace:  # WORKSPACE
                    # Fixed population is initialised on first run
                    # thinking of making sure people don't have more than one
                    # workplace
                    for i in range(group_num):
                        helper.update_place_group(place,
                                                  person_list=person_list,
                                                  person_weights=weights,
                                                  mean_capacity=mean_cap,
                                                  max_capacity=max_cap,
                                                  group_index=0)
                        # Remove added people from list of possible addees.
                        # Only if there were sufficient people to add.
                        if i in place.person_groups.keys():
                            person_list = [person for person in person_list
                                           if person not in
                                           place.person_groups[i]]

                elif place.place_type.name == PlaceType.CareHome:  # CAREHOME
                    # Initialise the fixed population of workers
                    helper.update_place_group(place, group_index=0)
                    # Initialise a fixed population of residents
                    person_list = [person for person in cell.persons
                                   if person.age > 65]
                    helper.update_place_group(place, group_index=1,
                                              person_list=person_list)

        # Add temporary population via the update sweep
        add_temporary_population = UpdatePlaceSweep()
        add_temporary_population.bind_population(self._population)
        add_temporary_population(0)

    def create_age_weights(self, place, params):
        """Function to return a list of people in the correct
        age range to be added to a place, and the weights
        for the different age groups.

        Parameters
        ----------

        place : Place
            Place to add people to
        params : dict
            Dictionary of parameters with age structure data

        Returns
        -------

        person_list : list
            List of people who may be in the place
        weights : list
            Corresponding weights for the person list
        """
        param_ind = place.place_type.value - 1
        min_age = [params["age_group1_min_age"][param_ind],
                   params["age_group2_min_age"][param_ind],
                   params["age_group3_min_age"][param_ind]]
        max_age = [params["age_group1_max_age"][param_ind],
                   params["age_group2_max_age"][param_ind],
                   params["age_group3_max_age"][param_ind]]
        prop = [params["age_group1_prop"][param_ind],
                params["age_group2_prop"][param_ind],
                params["age_group3_prop"][param_ind]]

        person_list = []
        weights = []
        for person in place.cell.persons:
            if (place.place_type.value in person.place_types):
                # People can't have more than one place of each type.
                continue
            for i in range(3):
                if (person.age > (min_age[i]-1) and person.age < max_age[i]):
                    # Assumes age groups are distinct and integers.
                    person_list.append(person)
                    weights.append(prop[i])
        return person_list, weights
