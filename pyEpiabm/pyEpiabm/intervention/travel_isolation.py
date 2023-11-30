#
# Travel isolation Class
#
import logging
import random

from pyEpiabm.core import Parameters

from .abstract_intervention import AbstractIntervention


class TravelIsolation(AbstractIntervention):
    """Travel isolation intervention.
    Isolate travelling individual based on the isolation_probability
    and stop isolating isolated individuals after their isolation period or
    after the end of the policy.
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
        self.name = 'travel_isolation'

        super(TravelIsolation, self).__init__(population=population, **kwargs)

    def __call__(self, time):
        """Run travel isolation intervention.

        Parameters
        ----------
        time : float
            Current simulation time

        """
        for person in self._population.travellers:
            # Apply only to travelling individuals
            if (hasattr(person, 'travel_end_time')):
                if hasattr(person, 'travel_isolation_start_time'):
                    if person.travel_isolation_start_time is not None:
                        if time > person.travel_isolation_start_time + \
                                self.isolation_duration:
                            # Stop isolating people after their isolation
                            # period
                            person.travel_isolation_start_time = None

                            # Check if need to assign to new household
                            if self.hotel_isolate == 1:
                                r = random.random()
                                if r < Parameters.instance().travel_params[
                                        'prob_existing_household']:
                                    # Remove the household
                                    person.household.remove_household()
                                    # Assign to existing household (not
                                    # to household containing isolating
                                    # individual)
                                    existing_households = \
                                        [h for h in person.microcell.
                                            households if not
                                            h.isolation_location]
                                    selected_household = random.choice(
                                        existing_households)
                                    selected_household.add_person(person)
                                    logging.info(f"Person {person.id} has "
                                                 f"finished isolating and "
                                                 f"has moved to household "
                                                 f"{selected_household.id}")

                                else:
                                    person.household.isolation_location = \
                                        False

                else:
                    if self.person_selection_method(person):
                        r = random.random()
                        # Require travelling symptomatic individuals to
                        # self-isolate with given probability
                        if r < self.isolation_probability:
                            # Check if they need to isolate outside
                            # household (if not already staying alone)
                            if self.hotel_isolate == 1:
                                if len(person.household.persons) > 1:
                                    # Remove from old household
                                    person.household.persons.remove(person)
                                    # Move to temporary household
                                    # N.B Person ID is not changed
                                    person.microcell.add_household([
                                        person], override_person_id=False)
                                    person.household.isolation_location = \
                                        True
                                else:
                                    # Current single household is my isolation
                                    # household
                                    person.household.isolation_location = \
                                        True

                            person.travel_isolation_start_time = time + \
                                self.isolation_delay

    def person_selection_method(self, person):
        """Method to determine whether a person is eligible for isolation.
        Depending on the value of the use_testing parameter person always
        isolates or isolates after testing positive.

        Parameters
        ----------
        person : Person
            Instance of the Person class

        Returns
        -------
        bool
            Whether the individual is eligible for travel isolation (either
            always or has tested positive)

        """
        if self.use_testing == 0:
            return True
        else:
            if person.date_positive is not None:
                return True

    def turn_off(self):
        """Turn off intervention after intervention stops being active.

        """
        for person in self._population.travellers:
            if (hasattr(person, 'travel_isolation_start_time')) and (
                    person.travel_isolation_start_time is not None):
                person.travel_isolation_start_time = None
