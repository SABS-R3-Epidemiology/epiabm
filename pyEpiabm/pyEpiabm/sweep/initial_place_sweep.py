#
# Sweep to initialise people present in a place
#

from .abstract_sweep import AbstractSweep
from .update_place_sweep import UpdatePlaceSweep


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
        for cell in self._population.cells:
            for place in cell.places:
                if place.place_type.value == 2:  # CAREHOME
                    # Initialise the fixed population of workers
                    mean_size = 10  # for example, would actually come in
                    # from a dictionary
                    helper.update_place_group(place, group_index=0,
                                              mean_capacity=mean_size)
                    # Initialise a fixed population of residents
                    mean_size = 100
                    helper.update_place_group(place,
                                              mean_capacity=mean_size,
                                              group_index=1)

                elif place.place_type.value == 3:  # RESTAURANT
                    # Initialise the fixed population
                    mean_size = 10
                    helper.update_place_group(place, mean_capacity=mean_size,
                                              group_index=0)

                elif place.place_type.value == 5:  # WORKSPACE
                    # Fixed population is initialised on first run
                    group_num = 5  # again would be an exterior param
                    mean_size = 20
                    max_size = 50
                    # thinking of making sure people don't have more than one
                    # workplace
                    person_list = place.cell.persons
                    for i in range(group_num):
                        helper.update_place_group(place, group_index=i,
                                                  person_list=person_list,
                                                  mean_capacity=mean_size,
                                                  max_capacity=max_size)
                        # Remove added people from list of possible addees.
                        # Only if there were sufficient people to add.
                        if i in place.person_groups.keys():
                            person_list = [person for person in person_list
                                           if person not in
                                           place.person_groups[i]]

        # Add temporary population via the update sweep
        add_temporary_population = UpdatePlaceSweep()
        add_temporary_population.bind_population(self._population)
        add_temporary_population(0)
