import unittest
from unittest import mock
import pyEpiabm as pe


class TestHostProgressionSweep(unittest.TestCase):
    """Tests the 'HostProgressionSweep' class.
    """
    @classmethod
    def setUpClass(cls) -> None:
        """Sets up a population we can use throughout the test.
        2 people are located in one microcell.
        """
        cls.test_population = pe.Population()
        cls.test_population.add_cells(1)
        cls.test_population.cells[0].add_microcells(1)
        cls.test_population.cells[0].microcells[0].add_people(3)
        cls.person1 = cls.test_population.cells[0].microcells[0].persons[0]
        cls.person2 = cls.test_population.cells[0].microcells[0].persons[1]
        cls.person3 = cls.test_population.cells[0].microcells[0].persons[2]

    def test_construct(self):
        """Tests that the host progression sweep initialises correctly.
        """
        pe.sweep.HostProgressionSweep()

    def test_update_status(self):
        """Tests the update status function on the test population. Person 2
        is set to infected and we check that their status changes to Recovered
        on the next time step.
        """
        self.person2.infection_status = pe.property.InfectionStatus.InfectMild
        test_sweep = pe.sweep.HostProgressionSweep()
        test_sweep.bind_population(self.test_population)
        test_sweep._update_next_infection_status(self.person2)
        self.assertEqual(self.person2.next_infection_status,
                         pe.property.InfectionStatus.Recovered)
        self.person2.infection_status = pe.property.InfectionStatus.Recovered
        self.assertRaises(TypeError, test_sweep._update_next_infection_status,
                          self.person2)

    def test_set_latent_time(self):
        """Test the set latent time returns a float greater than 0.0.
        """
        current_time = 5.0
        test_sweep = pe.sweep.HostProgressionSweep()
        test_sweep._calc_latent_time(self.person1, current_time)
        self.assertIsInstance(self.person1.time_of_status_change, float)
        self.assertTrue(5.0 <= self.person1.time_of_status_change)

    @mock.patch('pyEpiabm.utility.InverseCdf.icdf_choose_exp')
    def test_neg_latent_time(self, mock_choose):
        """Tests that an Assertion Error is raised if the set latent time
        is negative.
        """
        mock_choose.return_value = -1
        with self.assertRaises(AssertionError):
            test_sweep = pe.sweep.HostProgressionSweep()
            latency_time = test_sweep._set_latent_time()
            self.assertTrue(latency_time < 0)

    def test_update_time(self):
        """Test the update time function on the test population. This generates
        a random float (uniformly) between 1.0 and 10.0.
        """
        current_time = 5.0
        test_sweep = pe.sweep.HostProgressionSweep()
        test_sweep._update_time_to_status_change(self.person1, current_time)
        self.assertIsInstance(self.person1.time_of_status_change, float)
        self.assertTrue(6.0 <= self.person1.time_of_status_change <= 15.0)

    def test_call(self):
        """Tests the main function of the Host Progression Sweep.
        Person 3 is set to susceptible and becoming exposed. Person 2 is set to
        exposed and becoming infectious in one time step. Checks the
        population updates as expected.
        """
        self.person2.infection_status = pe.property.InfectionStatus.Exposed
        self.person2.time_of_status_change = 1.0
        self.person2.next_infection_status = \
            pe.property.InfectionStatus.InfectMild
        self.person3.infection_status = pe.property.InfectionStatus.Susceptible
        self.person3.time_of_status_change = 1.0
        self.person3.next_infection_status = \
            pe.property.InfectionStatus.Exposed
        test_sweep = pe.sweep.HostProgressionSweep()
        test_sweep.bind_population(self.test_population)

        # Tests population bound successfully.
        self.assertEqual(test_sweep._population.cells[0].persons[1].
                         infection_status, pe.property.InfectionStatus.Exposed)

        test_sweep(1.0)
        self.assertEqual(self.person2.infection_status,
                         pe.property.InfectionStatus.InfectMild)
        self.assertEqual(self.person3.infection_status,
                         pe.property.InfectionStatus.Exposed)
        self.assertEqual(self.person1.infection_status,
                         pe.property.InfectionStatus.Susceptible)
        self.assertIsInstance(self.person2.time_of_status_change, float)
        self.assertIsInstance(self.person3.time_of_status_change, float)
        self.assertTrue(2.0 <= self.person2.time_of_status_change <= 11.0)
        self.assertTrue(0.0 <= self.person3.time_of_status_change)


if __name__ == "__main__":
    unittest.main()
