#
# Initial Vaccination Sweep
#

import random

from .abstract_sweep import AbstractSweep

class InitialVaccineQueue(AbstractSweep):
    def __call__(self, vaccine_params, time):
        if time >= vaccine_params["vaccine_start_time"]:
            all_persons = [pers for cell in self._population.cells for pers
                           in cell.persons]
            age_thresholds = vaccine_params["min_ages"]
            prob_by_age = vaccine_params["probability_vaccinated"]

            for person in all_persons:
                assign_priority_group(person, age_thresholds)
                if random.random() < prob_by_age[person.priority_level-1]:
                    self._population.enque_vaccine(person.priority_level, person)


    def assign_priority_group(person, age_thresholds):
        # lower numbers denote higher priority
        if person.care_home_resident or person.age >= age_thresholds[0]:
            person.priority_level = 1
        elif person.age < age_thresholds[0] and person.age >= age_thresholds[1]:
            person.priority_level = 2
        elif person.age <age_thresholds[1] and person.age >= age_thresholds[2]:
            person.priority_level = 3
        elif person.age <age_thresholds[2] and person.age >= age_thresholds[3]:
            person.priority_level = 4
