#
# Initial Vaccination Sweep
#

import random
import logging
from itertools import count

from pyEpiabm.core import Parameters
from .abstract_sweep import AbstractSweep


class InitialVaccineQueue(AbstractSweep):
    """Runs through the eligible population and adds people to a priority
    queue for vaccination, prioritised by age and added according to the
    uptake in each age group.
    For a description of how the method functions in the context of vaccination
    see
    https://github.com/SABS-R3-Epidemiology/epiabm/wiki/Interventions#vaccination

    """
    def __init__(self):
        """Call in age group and uptake parameters if vaccination parameters
        are given.

        """
        if 'vaccine_params' in Parameters.instance().intervention_params:
            vaccine_params = Parameters.instance()\
                .intervention_params['vaccine_params']
            self.age_thresholds = vaccine_params["min_ages"]
            self.prob_by_age = vaccine_params["prob_vaccinated"]

        else:
            logging.error("InitialVaccineQueue is being run but no " +
                          "vaccination parameters are provided")

    def assign_priority_group(self, person, age_thresholds):
        """Assigns priority group to each person based on age and whether
        they are a carehome resident.
        Lower numbers denote higher priority

        Parameters
        ----------
        person : Person
            Person in population
        age_thresholds : list
            List of the minimum age in each priority group

        Returns
        ----------
        level : int
            Priority level of 1, 2, 3, or 4

        """

        level = None
        if (person.care_home_resident or person.age >= age_thresholds[0]):
            level = 1
        elif (person.age < age_thresholds[0]
              and person.age >= age_thresholds[1]):
            level = 2
        elif (person.age < age_thresholds[1]
              and person.age >= age_thresholds[2]):
            level = 3
        elif (person.age < age_thresholds[2]
              and person.age >= age_thresholds[3]):
            level = 4

        return level

    def __call__(self, sim_params):
        """If vaccinations are to be performed, runs through the population
        and adds people to a priority queue if elligible for vaccination
        based on their priority level and the vaccination uptake in their
        age group.

        """
        if 'vaccine_params' in Parameters.instance().intervention_params:
            all_persons = [pers for cell in self._population.cells
                           for pers in cell.persons]
            random.shuffle(all_persons)
            unique = count()  # returns a count object. each time next() is
            # called returns consecutive value. used to generate secondary
            # priority index to order within each priority group.
            for person in all_persons:
                level = self.assign_priority_group(person,
                                                   self.age_thresholds)
                if (level is not None
                        and random.random() <= self.prob_by_age[int(level)-1]):
                    self._population.enqueue_vaccine(level,
                                                     next(unique),
                                                     person)
