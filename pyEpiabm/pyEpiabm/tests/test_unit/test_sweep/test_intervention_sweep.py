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

        # Construct a population with 2 persons, one infector and one infectee
        cls._population = pe.Population()
        cls._population.add_cells(1)
        cls._population.cells[0].add_microcells(1)
        cls._microcell = cls._population.cells[0].microcells[0]
        cls._microcell.add_people(2)
        cls._microcell.add_household(cls._microcell.persons)
        cls.person_susc = cls._population.cells[0].microcells[0].persons[0]
        cls.person_susc.update_status(InfectionStatus(1))
        cls.person_symp = cls._population.cells[0].microcells[0].persons[1]
        cls.person_symp.update_status(InfectionStatus(4))

        cls.interventionsweep.bind_population(cls._population)

    def test_bind_population(self):
        self.assertEqual(len(self.interventionsweep.
                             intervention_params['case_isolation']), 8)
        self.assertEqual(len(self.interventionsweep.
                             intervention_params['place_closure']), 9)
        self.assertEqual(len(self.interventionsweep.
                             intervention_params['household_quarantine']), 10)
        self.assertEqual(len(self.interventionsweep.interventions), 3)

    def test___call__(self):
        self.interventionsweep(time=100)
        self.assertIsNotNone(self.interventionsweep._population.cells[0].
                             microcells[0].closure_start_time)

        # infector in case isolation, infectee in quarantine as
        # 100% probability and compliance
        self.interventionsweep(time=10)
        self.assertIsNotNone(self.person_symp.isolation_start_time)
        self.assertIsNotNone(self.person_susc.quarantine_start_time)

    def test__turn_of__(self):
        # Isolate the InfectMild individual
        self.person_symp.isolation_start_time = 370
        self.assertIsNotNone(self.person_symp.isolation_start_time)

        # stop isolating after start_time + policy_duration
        self.interventionsweep(time=372)
        self.assertIsNone(self.person_symp.isolation_start_time)


if __name__ == '__main__':
    unittest.main()
