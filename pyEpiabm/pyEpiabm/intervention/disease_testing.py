#
# Gives people a positive or negatie test status
#

import random

from pyEpiabm.intervention import AbstractIntervention


class DiseaseTesting(AbstractIntervention):
    """ Class to move through testing queue and assign
    positive test results depending on true/false positive rates.
    Detailed description of the implementation can be found in github wiki:
    https://github.com/SABS-R3-Epidemiology/epiabm/wiki/Interventions#testing

    """

    def __init__(self,
                 testing_capacity,
                 false_positive,
                 false_negative,
                 population,
                 **kwargs
                 ):
        self.testing_capacity = testing_capacity
        self.false_positive = false_positive
        self.false_negative = false_negative

        population.test_count = [0, 0]

        super(DiseaseTesting, self).__init__(population=population, **kwargs)

    def __call__(self, time):
        for cell in self._population.cells:
            num_pcr = 0
            num_lft = 0
            while (num_pcr < self.testing_capacity[0] and not
                   cell.PCR_queue.empty()):
                r = random.random()
                person = cell.PCR_queue.get()
                num_pcr += 1
                if person.is_infectious():
                    if r > self.false_negative[0]:
                        person.date_positive = time
                        self._population.test_count[0] += 1
                else:
                    if r < self.false_positive[0]:
                        person.date_positive = time
                        self._population.test_count[1] += 1
            while (num_lft < self.testing_capacity[1] and not
                   cell.LFT_queue.empty()):
                r = random.random()
                person = cell.LFT_queue.get()
                num_lft += 1
                if person.is_infectious():
                    if r > self.false_negative[1]:
                        person.date_positive = time
                        self._population.test_count[0] += 1
                else:
                    if r < self.false_positive[1]:
                        person.date_positive = time
                        self._population.test_count[1] += 1

    def turn_off(self):
        for cell in self._population.cells:
            for person in cell.persons:
                if person.date_positive is not None:
                    person.date_positive = None
