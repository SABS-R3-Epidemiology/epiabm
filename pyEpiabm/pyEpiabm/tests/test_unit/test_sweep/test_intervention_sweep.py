import unittest

import pyEpiabm as pe
from pyEpiabm.sweep import InterventionSweep
from pyEpiabm.property import InfectionStatus
from pyEpiabm.tests.test_unit.parameter_config_tests import TestPyEpiabm


class TestInterventionSweep(TestPyEpiabm):
    """Test the 'InterventionSweep' class.
    """

    @classmethod
    def setUpClass(cls) -> None:
        super(TestInterventionSweep, cls).setUpClass()
        cls.interventionsweep = InterventionSweep()

        # Construct a population with 8 persons
        cls._population = pe.Population()
        cls._population.add_cells(1)
        cls._population.cells[0].add_microcells(1)
        cls._population.cells[0].microcells[0].add_people(8)
        for i in range(8):
            person = cls._population.cells[0].microcells[0].persons[i]
            person.update_status(InfectionStatus(i + 1))
        cls.interventionsweep.bind_population(cls._population)

    def test_bind_population(self):
        self.assertEqual(len(self.interventionsweep.
                             intervention_params['case_isolation']), 8)
        self.assertEqual(len(self.interventionsweep.
                             intervention_params['household_quarantine']), 10)
        self.assertEqual(len(self.interventionsweep.interventions), 3)

    def test___call__(self):
        self.interventionsweep(time=100)
        self.assertIsNone(self.interventionsweep._population.cells[0].
                          persons[0].isolation_start_time)
        self.assertIsNone(self.interventionsweep._population.cells[0].
                          persons[0].quarantine_start_time)


if __name__ == '__main__':
    unittest.main()
