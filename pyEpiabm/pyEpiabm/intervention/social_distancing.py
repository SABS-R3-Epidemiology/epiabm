#
# Social Distancing Intervention
#

import random

from pyEpiabm.core import Parameters

from .abstract_intervention import AbstractIntervention


class SocialDistancing(AbstractIntervention):
    """Social distancing intervention
    Social distancing is based on the number of infectious persons in each
    microcell. The intensity of distancing for each individual is affected
    by the age group (with probability to take enhanced social distancing).
    Social distancing is stopped after the distancing period or
    after the end of the policy.
    Detailed description of the implementation can be found in github wiki:
    https://github.com/SABS-R3-Epidemiology/epiabm/wiki/Interventions.
    """

    def __init__(
        self,
        distancing_duration,
        distancing_delay,
        case_microcell_threshold,
        distancing_enhanced_prob,
        population,
        **kwargs
    ):
        self.distancing_duration = distancing_duration
        self.distancing_delay = distancing_delay
        self.case_microcell_threshold = case_microcell_threshold
        self.distancing_enhanced_prob = distancing_enhanced_prob
        super(SocialDistancing, self).__init__(population=population,
                                               **kwargs)

    def __call__(self, time):
        for cell in self._population.cells:
            for microcell in cell.microcells:
                if (hasattr(microcell, 'distancing_start_time')) and (
                        microcell.distancing_start_time is not None):
                    if time > microcell.distancing_start_time + self.\
                              distancing_duration:
                        # Stop social distancing after their distancing period
                        microcell.distancing_start_time = None
                else:
                    if microcell.count_infectious() >= self.\
                                case_microcell_threshold:
                        microcell.distancing_start_time = time + self.\
                                                        distancing_delay
                        for person in microcell.persons:
                            if Parameters.instance().use_ages:
                                r_age = random.random()
                                if r_age < self.distancing_enhanced_prob[
                                            person.age_group]:
                                    person.distancing_enhanced = True
                                else:
                                    person.distancing_enhanced = False
                            else:
                                person.distancing_enhanced = False

    def turn_off(self):
        for cell in self._population.cells:
            for microcell in cell.microcells:
                if (hasattr(microcell, 'distancing_start_time')) and (
                        microcell.distancing_start_time is not None):
                    microcell.distancing_start_time = None
