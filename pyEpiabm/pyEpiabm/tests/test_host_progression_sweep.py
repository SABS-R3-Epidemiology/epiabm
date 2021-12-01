import unittest
import pyEpiabm as pe



class TestHostProgressionSweep(unittest.TestCase):

    def test_construct(self):
        pe.HostProgressionSweep()
    


    def test_call(self):

        test_population = pe.Population()
        test_population.add_cells(1)
        test_cell = test_population.cells[0]
        test_population.cells[0].add_microcells(1)
        test_microcell = test_cell.microcells[0]
        test_population.cells[0].microcells[0].add_people(2)
        person1 = test_population.cells[0].microcells[0].persons[0]
        person2 = test_population.cells[0].microcells[0].persons[1]
        person2.infection_status = pe.InfectionStatus.Exposed
        person2.time_of_status_update = 1
        person2.next_infection_status = pe.InfectionStatus.InfectMild
        test_sweep = pe.HostProgressionSweep()
        test_sweep.bind_population(test_population)

        test_sweep.__call__(1)
        self.assertEqual(person2.infection_status,
                         pe.InfectionStatus.InfectMild)
        self.assertEqual(person2.next_infection_status,
                         pe.InfectionStatus.Recovered)
        self.assertEqual(person1.infection_status,
                         pe.InfectionStatus.Susceptible)
        self.assertIsInstance(person2.time_of_status_update, int)
        self.assertTrue(2 <= person2.time_of_status_update <= 11)


if __name__ == '__main__':
    unittest.main()

