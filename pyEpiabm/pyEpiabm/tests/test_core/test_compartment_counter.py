import unittest
import pyEpiabm as pe

import random


class TestCompartmentCounter(unittest.TestCase):
    """Test the _CompartmentCounter class
    """

    def test_construct(self):
        subject = pe.core._CompartmentCounter("Cell 1")
        self.assertEqual(subject.identifier, "Cell 1")
        for k in subject.retrieve():
            self.assertEqual(subject.retrieve()[k], 0)

    def test_reportRetrieve(self):
        subject = pe.core._CompartmentCounter("")
        subject.initialize(1000)
        statuses = {s: 0 for s in pe.property.InfectionStatus}
        statuses[pe.property.InfectionStatus.Susceptible] = 1000
        self.assertDictEqual(subject.retrieve(), statuses)
        for i in range(100):
            statuses[pe.property.InfectionStatus.Susceptible] -= 1
            newStatus = random.choice(list(pe.property.InfectionStatus))
            statuses[newStatus] += 1
            subject.report(pe.property.InfectionStatus.Susceptible, newStatus)
        self.assertDictEqual(subject.retrieve(), statuses)

    def test_reportRetrieveLarge(self):
        subject = pe.core._CompartmentCounter("")
        subject.initialize(1000000)
        statuses = {s: 0 for s in pe.property.InfectionStatus}
        statuses[pe.property.InfectionStatus.Susceptible] = 1000000
        self.assertDictEqual(subject.retrieve(), statuses)

        for i in range(10000):
            old = random.choice(list(pe.property.InfectionStatus))
            if statuses[old] == 0:
                continue

            new = random.choice(list(pe.property.InfectionStatus))
            subject.report(old, new)
            statuses[old] -= 1
            statuses[new] += 1

            self.assertDictEqual(subject.retrieve(), statuses)


if __name__ == '__main__':
    unittest.main()
