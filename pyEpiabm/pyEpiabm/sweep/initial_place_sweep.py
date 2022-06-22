#
# Sweep to initialise people present in a place
#

from pyEpiabm.core import Parameters

from .abstract_sweep import AbstractSweep
from .update_place_sweep import UpdatePlaceSweep


class InitialisePlaceSweep(AbstractSweep):
    """Class to initialise people in the "Place"
    class.
    """
    def __call__(self):
        """Given a population structure, updates the people
        present in each place at a specific timepoint. The
        explicit code handles the fixed population which are
        not changed later on in the simulation. To initialise
        the variable population (for example OutdoorSpace only
        has a variable population) one instance of
        UpdatePlaceSweep is called at the end to instantiate that.

        Parameters
        ----------
        time : float
            Current simulation time

        """

        # Double loop over the whole population, clearing places
        # of the variable population and refilling them.

        helper = UpdatePlaceSweep()
        helper.bind_population(self._population)
        params = Parameters.instance().place_params
        schools = ["PrimarySchool", "SecondarySchool", "SixthForm"]
        for cell in self._population.cells:
            for place in cell.places:
                param_ind = place.place_type.value - 1
                if param_ind < len(params["mean_size"]):
                    # Checks whether values are present, otherwise uses
                    # defaults
                    # nearest_places = params["nearest_places"][param_ind]
                    mean_cap = params["mean_size"][param_ind]
                    max_size = params["max_size"][param_ind]
                    offset = params["size_offset"][param_ind]
                    power = params["size_power"][param_ind]
                    ave_group_size = params["mean_group_size"][param_ind]
                    [person_list, weights] = self.create_age_weights(place,
                                                                     params)

                if place.place_type.name in schools:  # schools
                    # Initialise the fixed population
                    helper.update_place_group(place, group_size=ave_group_size,
                                              person_list=person_list,
                                              person_weights=weights,
                                              mean_capacity=mean_cap)

                elif place.place_type.name == "Workplace":  # WORKSPACE
                    # Fixed population is initialised on first run
                    power_list = [max_size, offset, power]
                    helper.update_place_group(place, group_size=ave_group_size,
                                              person_list=person_list,
                                              person_weights=weights,
                                              mean_capacity=mean_cap,
                                              power_law_params=power_list)

                elif place.place_type.name == "CareHome":  # CAREHOME
                    # Kit will add more detail for Carehomes
                    helper.update_place_group(place)

        # Instantiate the temporary population in each place using
        # the update sweep.
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
        typing.List[Person]
            List of people who may be in the place
        typing.List[float]
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
            if (place.place_type in person.place_types):
                # People can't have more than one place of each type.
                continue

            if not Parameters.instance().use_ages:
                person_list.append(person)
                weights.append(prop[2])  # Add everyone to adult group
            else:
                for i in range(3):
                    if (person.age > (min_age[i]-1)
                            and person.age < max_age[i]):
                        # Assumes age groups are distinct and integers.
                        person_list.append(person)
                        weights.append(prop[i])
                        break

        return person_list, weights
