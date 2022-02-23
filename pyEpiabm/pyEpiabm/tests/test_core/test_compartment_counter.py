import unittest
import random

import pyEpiabm as pe
from pyEpiabm.property.infection_status import InfectionStatus


class TestCompartmentCounter(unittest.TestCase):
    """Test the _CompartmentCounter class
    """
    @classmethod
    def setUpClass(cls) -> None:
        """Initialises a population with one cell and one person in
        the cell.
        """
        cls.cell = pe.Cell()
        cls.cell.add_microcells(1)
        cls.microcell = cls.cell.microcells[0]
        cls.microcell.add_people(1000)

    def test_construct(self):
        subject = pe._CompartmentCounter("Cell 1")
        self.assertEqual(subject.identifier, "Cell 1")
        for k in subject.retrieve():
            self.assertEqual(subject.retrieve()[k], 0)

    def test_reportRetrieve(self):
        subject = pe._CompartmentCounter("")
        self.assertRaises(ValueError, subject.report,
                          InfectionStatus.Susceptible,
                          InfectionStatus.InfectMild)
        subject.initialize(self.cell)
        statuses = {s: 0 for s in pe.property.InfectionStatus}
        statuses[pe.property.InfectionStatus.Susceptible] = 1000
        self.assertDictEqual(subject.retrieve(), statuses)
        for i in range(100):
            statuses[pe.property.InfectionStatus.Susceptible] -= 1
            newStatus = random.choice(list(pe.property.InfectionStatus))
            statuses[newStatus] += 1
            subject.report(pe.property.InfectionStatus.Susceptible, newStatus)
        self.assertDictEqual(subject.retrieve(), statuses)
        statuses[pe.property.InfectionStatus.Susceptible] += 1
        subject.report_new_person()
        self.assertDictEqual(subject.retrieve(), statuses)

    def test_reportRetrieveLarge(self):
        # Would note this takes a while to run so slows down unittests
        subject = pe._CompartmentCounter("")
        large_num = 1000000
        self.microcell.add_people(large_num - len(self.microcell.persons))
        subject.initialize(self.microcell)
        statuses = {s: 0 for s in pe.property.InfectionStatus}
        statuses[pe.property.InfectionStatus.Susceptible] = large_num
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
