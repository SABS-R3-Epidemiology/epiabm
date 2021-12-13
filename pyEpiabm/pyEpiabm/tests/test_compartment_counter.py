
import pyEpiabm as pe
import unittest

import random


class TestCompartmentCounter(unittest.TestCase):
    """Test the CompartmentCounter class
    """

    def test_construct(self):
        subject = pe.CompartmentCounter("Cell 1")
        self.assertEqual(subject.identifier, "Cell 1")
        for k in subject.retrieve():
            self.assertEqual(subject.retrieve()[k], 0)

    def test_reportRetrieve(self):
        subject = pe.CompartmentCounter("")
        subject.initialize(1000)
        statuses = {s: 0 for s in pe.InfectionStatus}
        statuses[pe.InfectionStatus.Susceptible] = 1000
        self.assertDictEqual(subject.retrieve(), statuses)
        for i in range(100):
            statuses[pe.InfectionStatus.Susceptible] -= 1
            newStatus = random.choice(list(pe.InfectionStatus))
            statuses[newStatus] += 1
            subject.report(pe.InfectionStatus.Susceptible, newStatus)
        self.assertDictEqual(subject.retrieve(), statuses)

    def test_reportRetrieveLarge(self):
        subject = pe.CompartmentCounter("")
        subject.initialize(1000000)
        statuses = {s: 0 for s in pe.InfectionStatus}
        statuses[pe.InfectionStatus.Susceptible] = 1000000
        self.assertDictEqual(subject.retrieve(), statuses)

        for i in range(10000):
            old = random.choice(list(pe.InfectionStatus))
            if statuses[old] == 0:
                continue

            new = random.choice(list(pe.InfectionStatus))
            subject.report(old, new)
            statuses[old] -= 1
            statuses[new] += 1

            self.assertDictEqual(subject.retrieve(), statuses)


if __name__ == '__main__':
    unittest.main()
