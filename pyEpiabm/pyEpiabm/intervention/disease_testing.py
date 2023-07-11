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
        self.name = 'disease_testing'

        population.test_count = [0, 0]

        super(DiseaseTesting, self).__init__(population=population, **kwargs)

    def __call__(self, time):
        """Run disease testing intervention.

        Parameters
        ----------
        time : float
            Current simulation time

        """
        for cell in self._population.cells:
            num_pcr = 0
            num_lft = 0
            while (num_pcr < self.testing_capacity[0] and not
                   cell.PCR_queue.empty()):
                person = cell.PCR_queue.get()
                num_pcr += 1
                self.do_testing(time, person, 0)
            while (num_lft < self.testing_capacity[1] and not
                   cell.LFT_queue.empty()):
                person = cell.LFT_queue.get()
                num_lft += 1
                self.do_testing(time, person, 1)

    def do_testing(self, time, person, index):
        """ Method to detemine whether an individual tests positive
        depending on the false positive and false negative rates for
        PCR tests (index = 0) or LFTs (index = 1).

        Parameters
        ----------
        time : float
            Current simulation time
        person : Person
            Instance of a Person class
        index : int
            To indicate whether test is PCR or LFT

        """
        r = random.random()
        if person.is_infectious():
            if r > self.false_negative[index]:
                person.date_positive = time
                self._population.test_count[0] += 1
        else:
            if r < self.false_positive[index]:
                person.date_positive = time
                self._population.test_count[1] += 1

    def turn_off(self):
        """Turn off intervention after intervention stops being active.

        """
        for cell in self._population.cells:
            for person in cell.persons:
                if person.date_positive is not None:
                    person.date_positive = None
