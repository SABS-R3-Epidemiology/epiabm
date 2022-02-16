import unittest
from unittest import mock
from queue import Queue

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
        cls.pop.setup()

    @mock.patch("pyEpiabm.utility.DistanceFunctions.dist_euclid")
    @mock.patch("numpy.random.poisson")
    @mock.patch("pyEpiabm.routine.SpatialInfection.space_foi")
    @mock.patch("pyEpiabm.routine.SpatialInfection.cell_inf")
    def test__call__(self, mock_inf, mock_force, mock_poisson, mock_dist):
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

        Parameters.instance().do_CovidSim = True
        test_sweep.bind_population(self.pop)
        test_sweep(time)
        self.assertTrue(self.cell_inf.person_queue.empty())

        # Add in another cell with a susceptible
        self.pop.add_cells(1)
        self.cell_susc = self.pop.cells[1]
        self.cell_susc.add_microcells(1)
        self.microcell_susc = self.cell_susc.microcells[0]
        self.microcell_susc.add_people(1)
        self.infectee = self.microcell_susc.persons[0]
        self.pop.setup()

        Parameters.instance().do_CovidSim = False
        test_sweep.bind_population(self.pop)
        test_sweep(time)
        self.assertTrue(self.cell_susc.person_queue.empty())

        Parameters.instance().do_CovidSim = True
        test_sweep.bind_population(self.pop)
        test_sweep(time)
        self.assertTrue(self.cell_susc.person_queue.empty())

        # Change person's status to infected
        Parameters.instance().do_CovidSim = False
        self.infector.update_status(InfectionStatus.InfectMild)
        test_sweep.bind_population(self.pop)
        test_sweep(time)
        self.assertEqual(self.cell_susc.person_queue.qsize(), 1)

        Parameters.instance().do_CovidSim = True
        self.cell_susc.person_queue = Queue()
        test_sweep.bind_population(self.pop)
        test_sweep(time)
        self.assertEqual(self.cell_susc.person_queue.qsize(), 1)

        # Change infectee's status to recovered so no susceptibles
        Parameters.instance().do_CovidSim = False
        self.infectee.update_status(InfectionStatus.Recovered)
        self.cell_susc.person_queue = Queue()
        test_sweep.bind_population(self.pop)
        test_sweep(time)
        self.assertTrue(self.cell_susc.person_queue.empty())

        Parameters.instance().do_CovidSim = True
        self.infectee.update_status(InfectionStatus.Recovered)
        self.cell_susc.person_queue = Queue()
        test_sweep.bind_population(self.pop)
        test_sweep(time)
        self.assertTrue(self.cell_susc.person_queue.empty())

    @mock.patch("random.random")
    def test_do_infection_event(self, mock_random):
        test_sweep = SpatialSweep()
        mock_random.return_value = 0  # Certain infection

        # Add in another cell, the subject of the infection,
        # initially with an recovered individual and no susceptibles
        pop = self.pop
        pop.add_cells(1)
        cell_sub = pop.cells[1]
        cell_sub.add_microcells(1)
        microcell_sub = cell_sub.microcells[0]
        microcell_sub.add_people(1)
        fake_infectee = microcell_sub.persons[0]
        pop.setup()
        fake_infectee.update_status(InfectionStatus.Recovered)

        self.assertTrue(cell_sub.person_queue.empty())
        test_sweep.do_infection_event(self.infector, fake_infectee, 1)
        self.assertFalse(mock_random.called)  # Should have already returned
        self.assertTrue(cell_sub.person_queue.empty())

        microcell_sub.add_people(1)
        real_infectee = microcell_sub.persons[1]  # Susceptible individual
        pop.setup()

        test_sweep.do_infection_event(self.infector, real_infectee, 1)
        mock_random.assert_called_once()
        self.assertEqual(cell_sub.person_queue.qsize(), 1)


if __name__ == '__main__':
    unittest.main()
