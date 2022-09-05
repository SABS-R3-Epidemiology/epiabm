import unittest
import random

import pyEpiabm as pe
from pyEpiabm.property.infection_status import InfectionStatus
from pyEpiabm.tests.test_unit.parameter_config_tests import TestPyEpiabm


class TestCompartmentCounter(TestPyEpiabm):
    """Test the _CompartmentCounter class
    """
    @classmethod
    def setUpClass(cls) -> None:
        """Initialises a population with one cell and one person in
        the cell.
        """
        super(TestCompartmentCounter, cls).setUpClass()  # Sets up parameters
        cls.cell = pe.Cell()
        cls.cell.add_microcells(1)
        cls.microcell = cls.cell.microcells[0]
        cls.microcell.add_people(1000)
        cls.subject = cls.microcell.compartment_counter

    def test_construct(self):
        self.subject = pe._CompartmentCounter("Cell 1")
        self.assertEqual(self.subject.identifier, "Cell 1")
        for status in self.subject.retrieve():
            with self.subTest(status=status):
                self.assertEqual(self.subject.retrieve()[status], 0)

    def test_reportRetrieve(self):
        self.assertRaises(ValueError, self.subject.report,
                          InfectionStatus.InfectMild,
                          InfectionStatus.Recovered)
        statuses = {s: 0 for s in InfectionStatus}
        statuses[InfectionStatus.Susceptible] = 1000
        self.assertDictEqual(self.subject.retrieve(), statuses)
        for i in range(100):
            statuses[InfectionStatus.Susceptible] -= 1
            newStatus = random.choice(list(InfectionStatus))
            statuses[newStatus] += 1
            self.microcell.persons[i].update_status(newStatus)
        self.assertDictEqual(self.subject.retrieve(), statuses)
        statuses[InfectionStatus.Susceptible] += 1
        # Explicitly tests the incremenet compartment function.
        self.subject._increment_compartment(1, InfectionStatus.Susceptible)
        self.assertDictEqual(self.subject.retrieve(), statuses)
        # Now need to remove the false addition above.
        self.subject.retrieve()[InfectionStatus.Susceptible] -= 1

    def test_reportRetrieveLarge(self):
        self.maxDiff = None
        for person in self.microcell.persons:
            person.update_status(InfectionStatus.Susceptible)
        large_num = 10000
        self.microcell.add_people(large_num - len(self.microcell.persons))
        statuses = {s: 0 for s in InfectionStatus}
        statuses[InfectionStatus.Susceptible] = large_num
        self.assertDictEqual(self.subject.retrieve(), statuses)

        for _ in range(10000):
            old = random.choice(list(InfectionStatus))
            if statuses[old] == 0:
                continue

            new = random.choice(list(InfectionStatus))
            self.subject.report(old, new)
            statuses[old] -= 1
            statuses[new] += 1

            self.assertDictEqual(self.subject.retrieve(), statuses)


if __name__ == '__main__':
    unittest.main()
