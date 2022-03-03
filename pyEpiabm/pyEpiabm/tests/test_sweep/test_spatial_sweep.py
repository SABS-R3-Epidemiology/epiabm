import unittest
from unittest import mock
from queue import Queue
import numpy as np

from pyEpiabm.core import Population, Parameters
from pyEpiabm.property import InfectionStatus
from pyEpiabm.sweep import SpatialSweep


class TestSpatialSweep(unittest.TestCase):
    """Test the "SpatialSweep" class.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """Initialises a population with one cell and one person in
        the cell.
        """
        cls.pop = Population()
        cls.pop.add_cells(1)
        cls.cell_inf = cls.pop.cells[0]

        cls.cell_inf.add_microcells(1)
        cls.microcell_inf = cls.cell_inf.microcells[0]

        cls.microcell_inf.add_people(100)
        cls.infector = cls.microcell_inf.persons[0]
        Parameters.instance().time_steps_per_day = 1

    @mock.patch("numpy.nan_to_num")
    @mock.patch("random.sample")
    @mock.patch("pyEpiabm.utility.DistanceFunctions.dist_euclid")
    @mock.patch("numpy.random.poisson")
    @mock.patch("pyEpiabm.routine.SpatialInfection.space_foi")
    @mock.patch("pyEpiabm.routine.SpatialInfection.cell_inf")
    def test__call__(self, mock_inf, mock_force, mock_poisson, mock_dist,
                     mock_infectee, mock_nan):
        """Test whether the spatial sweep function correctly
        adds persons to the queue, with each infection
        event certain to happen.
        """
        mock_dist.return_value = 2
        mock_poisson.return_value = 1
        mock_inf.return_value = 10.0
        mock_force.return_value = 100.0
        time = 1
        Parameters.instance().infection_radius = 5000

        test_sweep = SpatialSweep()

        # Assert a population with one cell doesn't do anything
        Parameters.instance().do_CovidSim = False
        test_sweep.bind_population(self.pop)
        test_sweep(time)
        self.assertTrue(self.cell_inf.person_queue.empty())

        # Add in another cell with a susceptible, but still
        # no infectors so no infection events.
        self.pop.add_cells(1)
        self.cell_susc = self.pop.cells[1]
        self.cell_susc.add_microcells(1)
        self.microcell_susc = self.cell_susc.microcells[0]
        self.microcell_susc.add_people(1)
        self.infectee = self.microcell_susc.persons[0]
        mock_infectee.return_value = [self.infectee]

        test_sweep.bind_population(self.pop)
        test_sweep(time)
        self.assertTrue(self.cell_susc.person_queue.empty())

        # Change infector's status to infected
        self.infector.update_status(InfectionStatus.InfectMild)
        test_sweep.bind_population(self.pop)
        test_sweep(time)
        self.assertEqual(self.cell_susc.person_queue.qsize(), 1)

        # Check when we have an infector but no infectees
        self.infectee.update_status(InfectionStatus.Recovered)
        self.cell_susc.person_queue = Queue()
        test_sweep.bind_population(self.pop)
        test_sweep(time)
        self.infectee.update_status(InfectionStatus.Susceptible)

        # Check when all (one) nan in distance, won't call nan_to_num
        mock_dist.return_value = 0

        self.cell_susc.person_queue = Queue()
        test_sweep.bind_population(self.pop)
        test_sweep(time)
        self.assertFalse(mock_nan.called)
        self.assertEqual(self.cell_susc.person_queue.qsize(), 1)

        # All (one) valid distances also won't call nan_to_num
        mock_dist.return_value = 2
        Parameters.instance().do_CovidSim = True
        self.cell_susc.person_queue = Queue()
        test_sweep.bind_population(self.pop)
        test_sweep(time)
        self.assertFalse(mock_nan.called)
        self.assertEqual(self.cell_susc.person_queue.qsize(), 1)

        # Three cells to test distance, one nan, one valid
        # distance will call nan_to_num
        Parameters.instance().do_CovidSim = False
        mock_nan.return_value = [2, 2]

        self.infectee.update_status(InfectionStatus.Susceptible)
        mock_dist.side_effect = [0, 2]
        self.pop.add_cells(1)
        self.third_cell = self.pop.cells[2]
        self.third_cell.add_microcells(1)
        self.third_cell.microcells[0].add_people(1)
        self.cell_susc.person_queue = Queue()
        test_sweep.bind_population(self.pop)
        test_sweep(time)
        mock_nan.assert_called_once_with([np.nan, 0.5], nan=0.5)
        self.assertEqual(self.cell_susc.person_queue.qsize(), 1)

    @mock.patch("random.random")
    def test_do_infection_event(self, mock_random):
        test_sweep = SpatialSweep()
        mock_random.return_value = 0  # Certain infection

        # Add in another cell, the subject of the infection,
        # initially with an recovered individual and no susceptibles

        cell_susc = self.pop.cells[1]
        cell_susc.person_queue = Queue()
        microcell_susc = cell_susc.microcells[0]
        microcell_susc.add_people(1)
        fake_infectee = microcell_susc.persons[1]
        fake_infectee.update_status(InfectionStatus.Recovered)
        actual_infectee = microcell_susc.persons[0]

        self.assertTrue(cell_susc.person_queue.empty())
        test_sweep.do_infection_event(self.infector, fake_infectee, 1)
        self.assertFalse(mock_random.called)  # Should have already returned
        self.assertTrue(cell_susc.person_queue.empty())

        test_sweep.do_infection_event(self.infector, actual_infectee, 1)
        mock_random.assert_called_once()
        self.assertEqual(cell_susc.person_queue.qsize(), 1)


if __name__ == '__main__':
    unittest.main()
