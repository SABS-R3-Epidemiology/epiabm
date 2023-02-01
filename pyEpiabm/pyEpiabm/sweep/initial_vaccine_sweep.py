#
# Initial Vaccination Sweep
#

import random
from itertools import count

from pyEpiabm.core import Parameters
from .abstract_sweep import AbstractSweep

class InitialVaccineQueue(AbstractSweep):
    def __init__(self):
        if 'vaccine_params' in Parameters.instance().intervention_params:
            vaccine_params = Parameters.instance().intervention_params['vaccine_params']
            self.age_thresholds = vaccine_params["min_ages"]
            self.prob_by_age = vaccine_params["prob_vaccinated"]

    def assign_priority_group(self, person, age_thresholds):
        # lower numbers denote higher priority
        if person.care_home_resident or person.age >= age_thresholds[0]:
            person.priority_level = 1
        elif person.age < age_thresholds[0] and person.age >= age_thresholds[1]:
            person.priority_level = 2
        elif person.age <age_thresholds[1] and person.age >= age_thresholds[2]:
            person.priority_level = 3
        elif person.age <age_thresholds[2] and person.age >= age_thresholds[3]:
            person.priority_level = 4
   
    def __call__(self, sim_params):
        if 'vaccine_params' in Parameters.instance().intervention_params:
            all_persons = [pers for cell in self._population.cells for pers in cell.persons]
            random.shuffle(all_persons)
            unique = count()
            for person in all_persons:
                self.assign_priority_group(person, self.age_thresholds)
                if person.priority_level is not None and random.random() <= self.prob_by_age[int(person.priority_level)-1]:
                    self._population.enqueue_vaccine(person.priority_level, next(unique), person)


