import unittest

import pyEpiabm as pe
from pyEpiabm.tests.test_unit.parameter_config_tests import TestPyEpiabm


class TestAbstractSweep(TestPyEpiabm):
    """Test the 'AbstractSweep' class.
    """

    def test_construct(self):
        pe.sweep.AbstractSweep()

    def test_bind_population(self):
        subject = pe.sweep.AbstractSweep()
        population = pe.Population()
        subject.bind_population(population)

    def test___call__(self):
        subject = pe.sweep.AbstractSweep()
        self.assertRaises(NotImplementedError, subject.__call__, 1)

    def test_store_infection_periods(self):
        pop = pe.Population()
        pop.add_cells(1)
        cell = pop.cells[0]
        microcell = pe.Microcell(cell)
        infector = pe.Person(microcell)
        infectee = pe.Person(microcell)
        time = 15.0
        infector.infection_start_times = [4.0, 10.0]
        infector.set_latent_period(3.0)
        pe.sweep.AbstractSweep.store_infection_periods(infector, infectee,
                                                       time)
        self.assertEqual(infectee.exposure_period, 5.0)
        self.assertEqual(infectee.infector_latent_period, 3.0)


if __name__ == '__main__':
    unittest.main()
