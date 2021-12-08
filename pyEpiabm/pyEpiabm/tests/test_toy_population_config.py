import unittest
import pyEpiabm as pe
from pyEpiabm.toy_population_config import ToyPopulation


class TestTopPopConfig(unittest.TestCase):
    """Test the Toy Population class.
    """
    @classmethod
    def setUpClass(cls) -> None:
        cls.pop_size = 1000
        cls.cell_number = 5
        cls.microcell_per_cell = 5
        cls.household_number = 10

    def test_init(self):
        # Population is initialised with no households
        self.toy_pop = pe.ToyPopulation(self.pop_size, self.cell_number,
                                        self.microcell_per_cell,
                                        self.household_number)

        total_people = 0
        count_non_empty_cells = 0
        count_non_trivial_households = 0
        for cell in self.toy_pop.population.cells:
            for microcell in cell.microcells:
                total_people = total_people + len(microcell.persons)
                for person in microcell.persons:
                    if len(person.household.persons) > 1:
                        count_non_trivial_households += 1
            if len(cell.persons) > 0:
                count_non_empty_cells += 1
        # test there are at least one non-empty cell
        self.assertTrue(count_non_empty_cells > 1)
        # test that everyone in the population has been assigned a microcell
        self.assertEqual(total_people, self.pop_size)
        # test that each household is trivial (contains one person)
        self.assertEqual(count_non_trivial_households, 0)

    def test_if_households(self):
        if_households = 1.0
        self.assertRaises(TypeError, ToyPopulation, self.pop_size, self.cell_number,
                                        self.microcell_per_cell,
                                        self.household_number,
                                        if_households)
        if_households = True
        self.toy_pop = pe.ToyPopulation(self.pop_size, self.cell_number,
                                        self.microcell_per_cell,
                                        self.household_number,
                                        if_households)
        total_people = 0
        households = []
        for cell in self.toy_pop.population.cells:
            for microcell in cell.microcells:
                for person in microcell.persons:
                    if person.household not in households:
                        households.append(person.household)
                    total_people = total_people + len(person.household.persons)
        print(len(households))



if __name__ == '__main__':
    unittest.main()
