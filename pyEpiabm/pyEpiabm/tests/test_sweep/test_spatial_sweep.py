import unittest
from unittest import mock
from queue import Queue
import numpy as np

from pyEpiabm.core import Population, Parameters
from pyEpiabm.property import InfectionStatus
from pyEpiabm.sweep import SpatialSweep
from pyEpiabm.tests.mocked_logging_tests import TestMockedLogs


class TestSpatialSweep(TestMockedLogs):
    """Test the "SpatialSweep" class.
    """

    def setUp(self):
        self.pop = Population()
        self.pop.add_cells(1)
        self.cell_inf = self.pop.cells[0]

        self.cell_inf.add_microcells(1)
        self.microcell_inf = self.cell_inf.microcells[0]

        self.microcell_inf.add_people(100)
        self.infector = self.microcell_inf.persons[0]
        self.infector.infectiousness = 1.0
        Parameters.instance().time_steps_per_day = 1
        Parameters.instance().do_CovidSim = False

    @mock.patch("logging.exception")
    @mock.patch("numpy.nan_to_num")
    @mock.patch("pyEpiabm.utility.DistanceFunctions.dist_euclid")
    def test_find_infectees(self, mock_dist, mock_nan, mock_logger):
        Parameters.instance().infection_radius = 1000
        test_pop = self.pop
        test_sweep = SpatialSweep()
        test_sweep.bind_population(test_pop)
        test_pop.add_cells(1)
        cell_susc = test_pop.cells[1]
        cell_susc.add_microcells(1)
        microcell_susc = cell_susc.microcells[0]
        microcell_susc.add_people(1)
        infectee = microcell_susc.persons[0]

        # Check when all (one) nan in distance, won't call nan_to_num
        mock_dist.return_value = 0
        test_list = test_sweep.find_infectees(self.cell_inf, [cell_susc], 1)
        self.assertFalse(mock_nan.called)
        self.assertEqual(test_list, [infectee])

        mock_dist.return_value = 2
        test_list = test_sweep.find_infectees(self.cell_inf, [cell_susc], 1)
        self.assertFalse(mock_nan.called)
        self.assertEqual(test_list, [infectee])

        mock_nan.return_value = [2, 0.0000001]
        mock_dist.side_effect = [0, 2]
        test_pop.add_cells(1)
        third_cell = test_pop.cells[2]
        third_cell.add_microcells(1)
        third_cell.microcells[0].add_people(1)

        test_list = test_sweep.find_infectees(self.cell_inf, [cell_susc,
                                                              third_cell], 1)
        mock_nan.assert_called_once_with([np.nan, 0.5], nan=0.5)
        self.assertEqual(test_list, [infectee])

        # test the assert that the distance weights has correct length
        mock_dist.side_effect = [0, 2]
        mock_nan.return_value = [1]
        self.assertRaises(AssertionError, test_sweep.find_infectees,
                          self.cell_inf, [cell_susc, third_cell], 1)

        # test value error is raised if all cells too far away
        Parameters.instance().infection_radius = 0.000001
        mock_dist.side_effect = [0, 2]
        mock_nan.return_value = [1, 1]
        test_list = test_sweep.find_infectees(self.cell_inf, [cell_susc,
                                              third_cell], 1)
        mock_logger.assert_called
        # test logger is called here

    @mock.patch("pyEpiabm.utility.DistanceFunctions.dist_euclid")
    def test_find_infectees_Covidsim(self, mock_dist):
        Parameters.instance().infection_radius = 100
        test_pop = self.pop
        test_sweep = SpatialSweep()
        test_sweep.bind_population(test_pop)
        test_pop.add_cells(1)
        cell_susc = test_pop.cells[1]
        cell_susc.add_microcells(1)
        microcell_susc = cell_susc.microcells[0]
        microcell_susc.add_people(1)
        infectee = microcell_susc.persons[0]

        # Test if distance is small, infectee listed
        mock_dist.return_value = 0
        Parameters.instance().infection_radius = 1
        test_list = test_sweep.find_infectees_Covidsim(self.infector,
                                                       [cell_susc], 1)
        self.assertEqual(test_list, [infectee])
        mock_dist.assert_called_with(self.cell_inf.location,
                                     cell_susc.location)
        # If distance is large infectee not listed
        # Only this doesn't work now becuase Covidsim is weird

        # mock_dist.return_value = 1000
        # test_list = test_sweep.find_infectees_Covidsim(self.infector,
        #                                               [cell_susc], 1)
        # self.assertEqual(test_list, [])

    @mock.patch("pyEpiabm.sweep.SpatialSweep.find_infectees_Covidsim")
    @mock.patch("pyEpiabm.sweep.SpatialSweep.find_infectees")
    @mock.patch("numpy.random.poisson")
    @mock.patch("pyEpiabm.property.SpatialInfection.space_foi")
    @mock.patch("pyEpiabm.property.SpatialInfection.cell_inf")
    def test__call__(self, mock_inf, mock_foi, mock_poisson, mock_inf_list,
                     mock_list_covid):
        """Test whether the spatial sweep function correctly
        adds persons to the queue, with each infection
        event certain to happen.
        """
        mock_inf.return_value = 10
        mock_foi.return_value = 100.0
        mock_poisson.return_value = 1
        time = 1
        Parameters.instance().infection_radius = 1000

        test_pop = self.pop
        test_sweep = SpatialSweep()

        # Assert a population with one cell doesn't do anything
        test_sweep.bind_population(test_pop)
        test_sweep(time)
        self.assertTrue(self.cell_inf.person_queue.empty())

        # Add in another cell with a susceptible, but still
        # no infectors so no infection events.
        test_pop.add_cells(1)
        cell_susc = test_pop.cells[1]
        cell_susc.add_microcells(1)
        microcell_susc = cell_susc.microcells[0]
        microcell_susc.add_people(1)
        infectee = microcell_susc.persons[0]
        mock_inf_list.return_value = [infectee]
        mock_list_covid.return_value = [infectee]

        test_sweep(time)
        self.assertTrue(cell_susc.person_queue.empty())

        # Change infector's status to infected
        self.infector.update_status(InfectionStatus.InfectMild)
        test_sweep(time)
        self.assertEqual(cell_susc.person_queue.qsize(), 1)
        Parameters.instance().do_CovidSim = True
        cell_susc.person_queue = Queue()
        test_sweep(time)
        self.assertEqual(cell_susc.person_queue.qsize(), 1)

        # Check when we have an infector but no infectees
        infectee.update_status(InfectionStatus.Recovered)
        cell_susc.person_queue = Queue()
        test_sweep(time)
        self.assertEqual(cell_susc.person_queue.qsize(), 0)

        # Test parameters break-out clause
        Parameters.instance().infection_radius = 0
        test_sweep(time)
        mock_inf_list.assert_not_called
        mock_list_covid.assert_not_called
        self.assertEqual(cell_susc.person_queue.qsize(), 0)

    @mock.patch("random.random")
    def test_do_infection_event(self, mock_random):
        test_sweep = SpatialSweep()
        mock_random.return_value = 0  # Certain infection

        # Add in another cell, the subject of the infection,
        # initially with an recovered individual and no susceptibles

        test_pop = self.pop
        test_pop.add_cells(1)
        cell_susc = test_pop.cells[1]
        cell_susc.add_microcells(1)
        microcell_susc = cell_susc.microcells[0]
        microcell_susc.add_people(2)
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
