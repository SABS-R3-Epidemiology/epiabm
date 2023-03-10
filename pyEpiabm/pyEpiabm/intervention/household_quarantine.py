#
# Household quarantine Class
#

import random

from pyEpiabm.intervention import AbstractIntervention


class HouseholdQuarantine(AbstractIntervention):
    """Household/Home quarantine intervention.
    People who share household with a symptomatic case (who case isolates)
    stay home based on the household and individual compliance, if
    intervention is active. Quarantine stops after the quarantine period
    or after the end of the policy.
    Detailed description of the implementation can be found in github wiki:
    https://github.com/SABS-R3-Epidemiology/epiabm/wiki/Interventions.
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
                if (hasattr(person, 'quarantine_start_time')) and (
                        person.quarantine_start_time is not None):
                    if time > person.quarantine_start_time + self.\
                              quarantine_duration:
                        # Stop quarantine after quarantine period
                        person.quarantine_start_time = None

                if (hasattr(person, 'isolation_start_time')) and (
                        person.isolation_start_time == time):
                    # Require household of symptomatic/isolating individuals to
                    # quarantine with given household compliance and individual
                    # compliance. Only check when infector starts its isolation
                    # in order to prevent resetting. Start time is reset when
                    # new person in household becomes an infector.
                    r_house = random.random()
                    if r_house < self.quarantine_house_compliant:
                        for household_person in person.household.persons:
                            if household_person != person:
                                r_indiv = random.random()
                                if r_indiv < \
                                        self.quarantine_individual_compliant:
                                    household_person.\
                                        quarantine_start_time = \
                                        time + self.quarantine_delay

    def turn_off(self):
        for cell in self._population.cells:
            for person in cell.persons:
                if (hasattr(person, 'quarantine_start_time')) and (
                        person.quarantine_start_time is not None):
                    person.quarantine_start_time = None
