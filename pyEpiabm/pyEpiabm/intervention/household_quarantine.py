#
# Household quarantine Class
#

import random

from pyEpiabm.intervention import AbstractIntervention


class HouseholdQuarantine(AbstractIntervention):
    """Household/Home quarantine intervention
    People who share household with a symptomatic case stay home based on
    the household and individual compliance, if intervention is active.
    Quarantine stops after the quarantine period.
    """

    def __init__(
        self,
        quarantine_duration,
        quarantine_delay,
        quarantine_house_compliant,
        quarantine_individual_compliant,
        population,
        **kwargs
    ):
        self.quarantine_duration = quarantine_duration
        self.quarantine_delay = quarantine_delay
        self.quarantine_house_compliant = quarantine_house_compliant
        self.quarantine_individual_compliant = quarantine_individual_compliant

        # start_time, policy_duration, threshold, population
        super(HouseholdQuarantine, self).__init__(population=population,
                                                  **kwargs)

    def __call__(self, time):
        for cell in self._population.cells:
            for person in cell.persons:
                if person.quarantine_start_time is not None:
                    if time > person.quarantine_start_time + self.\
                              quarantine_duration:
                        # Stop quarantine after quarantine period
                        person.quarantine_start_time = None
                else:
                    if person.is_symptomatic():
                        # Require household of symptomatic individuals to
                        # quarantine with given household compliance and
                        # individual compliance.
                        r_house = random.random()
                        if r_house < self.quarantine_house_compliant:
                            for household_person in person.household.persons:
                                r_indiv = random.random()
                                if r_indiv < self.\
                                   quarantine_individual_compliant:
                                    household_person.quarantine_start_time = \
                                        time + self.quarantine_delay

    def __turn_off__(self, time: float):
        for cell in self._population.cells:
            for person in cell.persons:
                if person.quarantine_start_time is not None:
                    person.quarantine_start_time = None
