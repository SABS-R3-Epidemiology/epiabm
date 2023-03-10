#
# Travel isolation Class
#

import random

from pyEpiabm.intervention import AbstractIntervention
from pyEpiabm.core import Parameters


class TravelIsolation(AbstractIntervention):
    """Travel isolation intervention.
    Isolate symptomatic travelling individual based on the
    isolation_probability and stop isolating isolated individuals after their
    isolation period or after the end of the policy.
    Detailed description of the implementation can be found in github wiki:
    https://github.com/SABS-R3-Epidemiology/epiabm/wiki/Interventions.

    """

    def __init__(
        self,
        isolation_duration,
        isolation_probability,
        isolation_delay,
        use_testing,
        hotel_isolate,
        population,
        **kwargs
    ):
        self.isolation_duration = isolation_duration
        self.isolation_delay = isolation_delay
        self.isolation_probability = isolation_probability
        self.use_testing = use_testing
        self.hotel_isolate = hotel_isolate

        super(TravelIsolation, self).__init__(population=population, **kwargs)

    def __call__(self, time):
        for cell in self._population.cells:
            for person in cell.persons:
                if (hasattr(person, 'travel_isolation_start_time')) and (
                        person.travel_isolation_start_time is not None):
                    if time > person.travel_isolation_start_time + self.\
                              isolation_duration:
                        # Stop isolating people after their isolation period
                        person.travel_isolation_start_time = None
                        # Check if need to assign to new household
                        r = random.random()
                        if r < Parameters.instance().travel_params[
                                'prob_existing_household']:
                            # Remove from current household and microcell
                            # counter
                            person.microcell.compartment_counter.\
                                _increment_compartment(
                                    -1, person.infection_status,
                                    person.age_group)
                            person.household.persons.remove(self)
                            # Assign to existing household (and implicit add
                            # to microcell counter)
                            selected_household = random.choice(
                                person.microcell.households)
                            selected_household.add_person(person)
                else:
                    if self.person_selection_method(person):

                        r = random.random()
                        # Require travelling symptomatic individuals to self-
                        # isolate with given probability
                        if r < self.isolation_probability:
                            # Check if they need to isolate outside household
                            if self.hotel_isolate == 1:
                                if len(person.household.persons) > 1:
                                    # Remove from old household and counter
                                    self.microcell.compartment_counter.\
                                        _increment_compartment(
                                            -1, person.infection_status,
                                            person.age_group)
                                    person.household.persons.remove(person)
                                    # Put in new household (implicitly added
                                    # to counter)
                                    person.microcell.add_household([person])

                            person.travel_isolation_start_time = time + self.\
                                isolation_delay
                            if person.date_positive is not None:
                                self._population.test_isolate_count = [0, 0]
                                if person.is_symptomatic():
                                    self._population.test_isolate_count[0] += 1
                                else:
                                    self._population.test_isolate_count[1] += 1

    def person_selection_method(self, person):
        """ Method to determine whether a person is eligible for isolation
        based on whether they are symptomatic or have tested positive depending
        on the value of the use_testing parameter.

        Parameters
        ----------
        person : Person

        Returns
        -------
        bool
            True if the individual is eligible for travel isolation (either
            symptomatic or has tested positive)

        """
        if self.use_testing == 0:
            return person.is_symptomatic()
        else:
            if person.date_positive is not None:
                return True

    def turn_off(self):
        # To do: loop over travellers list in TravelSweep
        for cell in self._population.cells:
            for person in cell.persons:
                if (hasattr(person, 'travel_isolation_start_time')) and (
                        person.travel_isolation_start_time is not None):
                    person.travel_isolation_start_time = None
