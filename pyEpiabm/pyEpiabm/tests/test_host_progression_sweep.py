import unittest
import pyEpiabm as pe


class TestHostProgressionSweep(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        '''Sets up a population we can use throughout the test.
        2 people in one microcell
        '''
        cls.test_population = pe.Population()
        cls.test_population.add_cells(1)
        cls.test_cell = cls.test_population.cells[0]
        cls.test_population.cells[0].add_microcells(1)
        cls.test_population.cells[0].microcells[0].add_people(2)
        cls.person1 = cls.test_population.cells[0].microcells[0].persons[0]
        cls.person2 = cls.test_population.cells[0].microcells[0].persons[1]

    def test_construct(self):
        pe.HostProgressionSweep()

    def test_update_status(self):
        # set person 2 to exposed and becoming infectious in one time step
        self.person2.infection_status = pe.InfectionStatus.InfectMild
        test_sweep = pe.HostProgressionSweep()
        test_sweep.bind_population(self.test_population)
        test_sweep._update_next_infection_status(self.person2)
        self.assertEqual(self.person2.next_infection_status,
                         pe.InfectionStatus.Recovered)
        self.person2.infection_status = pe.InfectionStatus.Recovered
        test_sweep.bind_population(self.test_population)
        self.assertRaises(TypeError, test_sweep._update_next_infection_status,
                          self.person2)

    def test_update_time(self):
        test_sweep = pe.HostProgressionSweep()
        time = test_sweep._update_time_to_status_change()
        self.assertIsInstance(time, int)
        self.assertTrue(1 <= time <= 10)

    def test_call(self):
        # set person 2 to exposed and becoming infectious in one time step
        self.person2.infection_status = pe.InfectionStatus.Exposed
        self.person2.time_of_status_change = 1
        self.person2.next_infection_status = pe.InfectionStatus.InfectMild
        test_sweep = pe.HostProgressionSweep()
        test_sweep.bind_population(self.test_population)

        # tests population bound successfully
        self.assertEqual(test_sweep._population.cells[0].persons[1].
                         infection_status, pe.InfectionStatus.Exposed)

        test_sweep(1)
        self.assertEqual(self.person2.infection_status,
                         pe.InfectionStatus.InfectMild)
        self.assertEqual(self.person2.next_infection_status,
                         pe.InfectionStatus.Recovered)
        self.assertEqual(self.person1.infection_status,
                         pe.InfectionStatus.Susceptible)
        self.assertIsInstance(self.person2.time_of_status_change, int)
        self.assertTrue(2 <= self.person2.time_of_status_change <= 11)


if __name__ == '__main__':
    unittest.main()
