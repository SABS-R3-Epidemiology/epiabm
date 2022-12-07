#
# Case isolation Class
#

import random

from pyEpiabm.intervention import AbstractIntervention


class CaseIsolation(AbstractIntervention):
    """Case isolation intervention
    """

    def __init__(
        self,
        isolation_duration,
        isolation_delay,
        isolation_probability,
        isolation_effectiveness,
        isolation_house_effectiveness,
        *args,
        **kwargs
    ):
        self.isolation_duration = isolation_duration
        self.isolation_delay = isolation_delay
        self.isolation_probability = isolation_probability
        # self.isolation_effectiveness = isolation_effectiveness
        # self.isolation_house_effectiveness = isolation_house_effectiveness
        self._population.isolation_effectiveness = isolation_effectiveness
        self._population.isolation_house_effectiveness = isolation_house_effectiveness
        super(CaseIsolation, self).__init__(*args, **kwargs)

    def __call__(self, time):
        for cell in self._population.cells:
            for person in cell.persons:
                if person.isolation_start_time is not None:
                    if time > person.isolation_start_time + self.isolation_duration:
                        # Stop isolating people after their isolation period
                        person.isolation_start_time = None
                else:
                    if person.is_symptomatic():
                        r = random.random()
                        # Require symptomatic individuals to self-isolate
                        if r < self.isolation_probability:
                            person.isolation_start_time = time + self.isolation_delay


