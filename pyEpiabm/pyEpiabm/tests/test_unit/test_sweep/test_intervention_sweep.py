import unittest

import pyEpiabm as pe
from pyEpiabm.sweep import InterventionSweep
from pyEpiabm.property import InfectionStatus
from pyEpiabm.tests.test_unit.parameter_config_tests import TestPyEpiabm


class TestInterventionSweep(TestPyEpiabm):
    """Test the 'InterventionSweep' class.
    """

    def setUp(self) -> None:
        super(TestInterventionSweep, self).setUp()
        self.interventionsweep = InterventionSweep()

        # Construct a population with 2 persons, one infector and one infectee
        self._population = pe.Population()
        self._population.add_cells(1)
        self._population.cells[0].add_microcells(1)
        self._microcell = self._population.cells[0].microcells[0]
        self._microcell.add_people(2)
        self._microcell.add_household(self._microcell.persons)
        self.person_susc = self._population.cells[0].microcells[0].persons[0]
        self.person_susc.update_status(InfectionStatus(1))
        self.person_symp = self._population.cells[0].microcells[0].persons[1]
        self.person_symp.update_status(InfectionStatus(4))

        self.interventionsweep.bind_population(self._population)

    def test_bind_population(self):
        self.assertEqual(len(self.interventionsweep.
                             intervention_params['case_isolation']), 8)
        self.assertEqual(len(self.interventionsweep.
                             intervention_params['place_closure']), 9)
        self.assertEqual(len(self.interventionsweep.
                             intervention_params['household_quarantine']), 10)
        self.assertEqual(len(
            self.interventionsweep.intervention_active_status.keys()), 3)

    def test___call__(self):
        self.interventionsweep(time=100)
        self.assertIsNotNone(self.interventionsweep._population.cells[0].
                             microcells[0].closure_start_time)

        # infector in case isolation, infectee in quarantine as
        # 100% probability and compliance
        # isolation_start_time = 100 as evaluated at this time (see above)
        self.assertEqual(self.person_symp.isolation_start_time, 100)
        self.assertIsNotNone(self.person_susc.quarantine_start_time)

    def test_turn_of(self):
        # Isolate the InfectMild individual
        self.interventionsweep(time=370)
        self.assertEqual(self.person_symp.isolation_start_time, 370)

        # stop isolating after start_time + policy_duration
        self.interventionsweep(time=372)
        self.assertIsNone(self.person_symp.isolation_start_time)


if __name__ == '__main__':
    unittest.main()
