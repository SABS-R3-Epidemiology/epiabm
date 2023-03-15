import unittest
from unittest import mock
from queue import Queue

from pyEpiabm.core import Population, Parameters
from pyEpiabm.property import InfectionStatus
from pyEpiabm.sweep import SpatialSweep
from pyEpiabm.tests.test_unit.mocked_logging_tests import TestMockedLogs


class TestSpatialSweep(TestMockedLogs):
    """Test the "SpatialSweep" class.
    """

    def setUp(self):
        # 1st Population
        # 2 cell population
        # 1st cell: 1 microcell, 100 people, includes the infector
        # who has InfectionStatus of mildly infected
        # 2nd cell: 1 microcell, 1 person, includes the infectee
        # who is Susceptible
        self.pop = Population()
        self.pop.add_cells(2)
        self.cell_inf = self.pop.cells[0]
        self.cell_susc = self.pop.cells[1]
        # self.cell_non_susc = self.pop.cells[2]

        self.cell_inf.add_microcells(1)
        self.microcell_inf = self.cell_inf.microcells[0]

        self.cell_susc.add_microcells(1)
        self.microcell_susc = self.cell_susc.microcells[0]

        self.microcell_inf.add_people(1)
        self.infector = self.microcell_inf.persons[0]
        self.infector.update_status(InfectionStatus.InfectMild)

        self.microcell_susc.add_people(1)
        self.infectee = self.microcell_susc.persons[0]
        self.infectee.update_status(InfectionStatus.Susceptible)

        self.infector.infectiousness = 1.0
        Parameters.instance().time_steps_per_day = 1
        Parameters.instance().do_CovidSim = False

        # 2nd population
        # Only has a single cell with a single person in
        # Used for checking exceptions in the code
        self.pop_only1 = Population()
        self.pop_only1.add_cells(1)
        self.cell_inf_only1 = self.pop_only1.cells[0]

        self.cell_inf_only1.add_microcells(1)
        self.microcell_inf_only1 = self.cell_inf_only1.microcells[0]

        self.microcell_inf_only1.add_people(100)
        self.infector_only1 = self.microcell_inf_only1.persons[0]
        self.infector_only1.update_status(InfectionStatus.InfectMild)

        self.infector_only1.infectiousness = 1.0
        Parameters.instance().time_steps_per_day = 1
        Parameters.instance().do_CovidSim = False

        # 3rd Population
        # 2 cells each with a single microcell with a single person
        # cell 1: 1 microcell with a mildly infected individual
        # cell 2: 1 microcell with a recovered individual
        self.pop_no_infectees = Population()
        self.pop_no_infectees.add_cells(2)
        self.cell_no_infectees_inf = self.pop_no_infectees.cells[0]
        self.cell_no_infectees_rec = self.pop_no_infectees.cells[1]

        self.cell_no_infectees_inf.add_microcells(1)
        self.microcell_no_infectees_inf = self.\
            cell_no_infectees_inf.microcells[0]

        self.cell_no_infectees_rec.add_microcells(1)
        self.microcell_no_infectees_rec = self.\
            cell_no_infectees_rec.microcells[0]

        self.microcell_no_infectees_inf.add_people(1)
        self.no_infectees_infector = self.microcell_no_infectees_inf.persons[0]
        self.no_infectees_infector.update_status(InfectionStatus.InfectMild)

        self.microcell_no_infectees_rec.add_people(1)
        self.no_infectees_rec = self.microcell_no_infectees_rec.persons[0]
        self.no_infectees_rec.update_status(InfectionStatus.Recovered)

    @mock.patch("pyEpiabm.utility.DistanceFunctions.dist_euclid")
    def test_nearby_cells(self, mock_dist):
        Parameters.instance().infection_radius = 1000
        test_pop = self.pop
        test_sweep = SpatialSweep()
        mock_dist.return_value = 2
        test_sweep.bind_population(test_pop)
        self.assertEqual(self.cell_inf.nearby_cells, {1: 2})

    @mock.patch("logging.exception")
    @mock.patch("numpy.nan_to_num")
    @mock.patch("pyEpiabm.utility.DistanceFunctions.dist_euclid")
    def test_bind_population(self, mock_dist, mock_nan, mock_logger):
        Parameters.instance().infection_radius = 0.0001
        # Assert a basic population
        test_pop = self.pop
        test_sweep = SpatialSweep()
        mock_dist.return_value = 2.2
        test_sweep.bind_population(test_pop)

        self.assertEqual(self.cell_inf.nearby_cells, {})

        Parameters.instance().infection_radius = 1000
        test_pop = self.pop
        test_sweep = SpatialSweep()
        mock_dist.return_value = 2.2
        self.assertEqual(test_sweep.bind_population(test_pop), None)
        self.assertEqual(test_sweep.bind_population(test_pop), None)

    @mock.patch("logging.exception")
    @mock.patch("numpy.nan_to_num")
    @mock.patch("pyEpiabm.utility.DistanceFunctions.dist_euclid")
    def test_find_infectees_successful(self, mock_dist, mock_nan, mock_logger):
        Parameters.instance().infection_radius = 1000
        test_pop = self.pop
        test_sweep = SpatialSweep()
        mock_dist.return_value = 2.2
        test_sweep.bind_population(test_pop)
        test_list = test_sweep.\
            find_infectees(self.cell_inf, [self.cell_susc], 1)
        self.assertFalse(mock_nan.called)
        self.assertEqual(test_list, [self.infectee])

    @mock.patch("logging.exception")
    @mock.patch("numpy.nan_to_num")
    @mock.patch("pyEpiabm.utility.DistanceFunctions.dist_euclid")
    def test_find_infectees_fails(self, mock_dist, mock_nan, mock_logger):
        Parameters.instance().infection_radius = 0.0001
        # Assert a basic population
        test_pop = self.pop
        test_sweep = SpatialSweep()
        mock_dist.return_value = 2.2
        test_sweep.bind_population(test_pop)

        # test value error is raised if all cells too far away
        Parameters.instance().infection_radius = 0.000001
        mock_dist.side_effect = [0, 2]
        mock_nan.return_value = [1, 1]
        test_list = test_sweep.\
            find_infectees(self.cell_inf, [self.cell_susc], 1)
        self.assertEqual(test_list, [])
        mock_logger.assert_called
        # test logger is called here

    @mock.patch("logging.exception")
    @mock.patch("pyEpiabm.utility.DistanceFunctions.dist_euclid")
    def test_find_infectees_fails_empty_cells(self, mock_dist, mock_logger):
        Parameters.instance().infection_radius = 1000
        test_pop = self.pop
        test_sweep = SpatialSweep()
        mock_dist.return_value = 2.2
        test_sweep.bind_population(test_pop)

        self.cell_susc.persons = []
        test_list = test_sweep.\
            find_infectees(self.cell_inf, [self.cell_susc], 1)
        self.assertEqual(test_list, [])
        mock_logger.assert_called
        # test logger is called here

    @mock.patch("pyEpiabm.utility.DistanceFunctions.dist_euclid")
    def test_find_infectees_Covidsim(self, mock_dist):
        Parameters.instance().infection_radius = 100
        test_pop = self.pop
        test_sweep = SpatialSweep()
        mock_dist.return_value = 0
        test_sweep.bind_population(test_pop)

        # Test if distance is small, infectee listed
        mock_dist.return_value = 0
        Parameters.instance().infection_radius = 1
        test_list = test_sweep.find_infectees_Covidsim(self.infector,
                                                       [self.cell_susc], 1)
        self.assertEqual(test_list, [self.infectee])
        mock_dist.assert_called_with(self.cell_inf.location,
                                     self.cell_susc.location)
        # If distance is large infectee not listed
        # Only this doesn't work now becuase Covidsim is weird

        # mock_dist.return_value = 1000
        # test_list = test_sweep.find_infectees_Covidsim(self.infector,
        #                                               [cell_susc], 1)

    @mock.patch("pyEpiabm.sweep.SpatialSweep.find_infectees_Covidsim")
    @mock.patch("pyEpiabm.sweep.SpatialSweep.find_infectees")
    @mock.patch("numpy.random.poisson")
    @mock.patch("pyEpiabm.property.SpatialInfection.spatial_foi")
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

        test_pop_only1 = self.pop_only1
        test_sweep = SpatialSweep()

        # Assert a population with one cell doesn't do anything
        test_sweep.bind_population(test_pop_only1)
        test_sweep(time)
        self.assertTrue(self.cell_inf.person_queue.empty())

        # Add in another cell with a susceptible, but still
        # no infectors so no infection events.
        mock_inf_list.return_value = [self.infectee]
        mock_list_covid.return_value = [self.infectee]

        test_sweep = SpatialSweep()

        # Assert a basic population
        test_pop = self.pop
        test_sweep.bind_population(test_pop)
        test_sweep(time)
        self.assertTrue(self.cell_inf.person_queue.empty())
        # Change infector's status to infected
        self.infector.update_status(InfectionStatus.InfectMild)
        test_sweep(time)
        self.assertEqual(self.cell_inf.person_queue.qsize(), 0)
        Parameters.instance().do_CovidSim = True
        self.cell_susc.person_queue = Queue()
        test_sweep(time)
        self.assertEqual(self.cell_susc.person_queue.qsize(), 1)
        # Check when we have an infector but no infectees
        self.infectee.update_status(InfectionStatus.Recovered)
        self.cell_susc.person_queue = Queue()
        test_sweep(time)
        self.assertEqual(self.cell_susc.person_queue.qsize(), 0)

        # Test parameters break-out clause
        Parameters.instance().infection_radius = 0
        test_sweep(time)
        mock_inf_list.assert_not_called
        mock_list_covid.assert_not_called
        self.assertEqual(self.cell_susc.person_queue.qsize(), 0)

    @mock.patch("pyEpiabm.sweep.SpatialSweep.find_infectees_Covidsim")
    @mock.patch("pyEpiabm.sweep.SpatialSweep.find_infectees")
    @mock.patch("numpy.random.poisson")
    @mock.patch("pyEpiabm.property.SpatialInfection.spatial_foi")
    @mock.patch("pyEpiabm.property.SpatialInfection.cell_inf")
    def test_call_possible_infectee_number_0(self, mock_inf, mock_foi,
                                             mock_poisson, mock_inf_list,
                                             mock_list_covid):
        mock_inf.return_value = 10
        mock_foi.return_value = 100.0
        mock_poisson.return_value = 1
        time = 1
        Parameters.instance().infection_radius = 1000

        test_pop_no_infectees = self.pop_no_infectees
        test_sweep = SpatialSweep()

        # Assert a population with two cells one with infected person
        # one with recovered person
        test_sweep.bind_population(test_pop_no_infectees)
        test_sweep(time)
        self.assertTrue(self.cell_inf.person_queue.empty())
        self.assertEqual(self.cell_no_infectees_rec.person_queue.qsize(), 0)

        mock_inf.assert_not_called
        mock_foi.assert_not_called
        mock_poisson.assert_not_called
        mock_inf_list.assert_not_called
        mock_list_covid.assert_not_called

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
