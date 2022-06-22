import unittest
import random
import numpy as np
from unittest.mock import patch

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
        if pe.Parameters.instance().use_ages:
            nb_groups = len(pe.Parameters.instance().age_proportions)
        else:
            nb_groups = 1
        for status in self.subject.retrieve():
            for agegroup in range(nb_groups):
                with self.subTest(status=status):
                    self.assertEqual(self.subject.retrieve()[status][agegroup],
                                     0)

    @patch('pyEpiabm.core.Parameters.instance')
    def test_construct_no_age(self, mock_params):
        mock_params.return_value.use_ages = False
        self.subject = pe._CompartmentCounter("Cell 1")
        self.assertEqual(self.subject.identifier, "Cell 1")
        if pe.Parameters.instance().use_ages:
            nb_groups = len(pe.Parameters.instance().age_proportions)
        else:
            nb_groups = 1
        for status in self.subject.retrieve():
            for agegroup in range(nb_groups):
                with self.subTest(status=status):
                    self.assertEqual(self.subject.retrieve()[status][agegroup],
                                     0)

    def test_reportRetrieve(self):
        self.assertRaises(ValueError, self.subject.report,
                          InfectionStatus.InfectMild,
                          InfectionStatus.Recovered)
        if pe.Parameters.instance().use_ages:
            nb_groups = len(pe.Parameters.instance().age_proportions)
        else:
            nb_groups = 1
        statuses = {s: np.zeros(nb_groups) for s in InfectionStatus}
        statuses[InfectionStatus.Susceptible][0] = 1000
        self.assertTrue((self.subject.retrieve()[InfectionStatus.Susceptible]
                         == statuses[InfectionStatus.Susceptible]).all())
        for i in range(100):
            statuses[InfectionStatus.Susceptible][0] -= 1
            newStatus = random.choice(list(InfectionStatus))
            statuses[newStatus][0] += 1
            self.microcell.persons[i].update_status(newStatus)
        for inf_status in list(InfectionStatus):
            self.assertTrue((self.subject.retrieve()[inf_status] ==
                             statuses[inf_status]).all())
        statuses[InfectionStatus.Susceptible][0] += 1
        # Explicitly tests the incremenet compartment function.
        self.subject._increment_compartment(1, InfectionStatus.Susceptible)
        for inf_status in list(InfectionStatus):
            self.assertTrue((self.subject.retrieve()[inf_status] ==
                             statuses[inf_status]).all())
        # Now need to remove the false addition above.
        self.subject.retrieve()[InfectionStatus.Susceptible][0] -= 1

    def test_reportRetrieveLarge(self):
        self.maxDiff = None
        for person in self.microcell.persons:
            person.update_status(InfectionStatus.Susceptible)
        large_num = 10000
        self.microcell.add_people(large_num - len(self.microcell.persons))
        if pe.Parameters.instance().use_ages:
            nb_groups = len(pe.Parameters.instance().age_proportions)
        else:
            nb_groups = 1
        statuses = {s: np.zeros(nb_groups) for s in InfectionStatus}
        statuses[InfectionStatus.Susceptible][0] = large_num
        self.assertTrue((self.subject.retrieve()[InfectionStatus.Susceptible]
                         == statuses[InfectionStatus.Susceptible]).all())

        for _ in range(10000):
            old = random.choice(list(InfectionStatus))
            if statuses[old][0] == 0:
                continue

            new = random.choice(list(InfectionStatus))
            self.subject.report(old, new)
            statuses[old][0] -= 1
            statuses[new][0] += 1

            for inf_status in list(InfectionStatus):
                self.assertTrue((self.subject.retrieve()[inf_status] ==
                                 statuses[inf_status]).all())


if __name__ == '__main__':
    unittest.main()
