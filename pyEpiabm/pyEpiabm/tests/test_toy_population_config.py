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
        """Tests for when the population is implemented by default with
        no households.
        """
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
        """Tests when households are implemented.
        """
        if_households = 1.0
        # Tests that if_households only takes boolean input.
        self.assertRaises(TypeError, ToyPopulation, self.pop_size,
                          self.cell_number, self.microcell_per_cell,
                          self.household_number,
                          if_households)
        # Initialises population with households.
        if_households = True
        self.toy_pop = pe.ToyPopulation(self.pop_size, self.cell_number,
                                        self.microcell_per_cell,
                                        self.household_number,
                                        if_households)
        total_people = 0
        households = []
        num_empty_households = 0
        for cell in self.toy_pop.population.cells:
            for microcell in cell.microcells:
                for person in microcell.persons:
                    if person.household not in households:
                        households.append(person.household)
                    if len(person.household.persons) == 0:
                        num_empty_households += 1
                    total_people = total_people + len(person.household.persons)
        # Some households may be empty so won't be included. Tests that at most
        # 10% of the total implemented are empty.
        total_households = self.cell_number*self.microcell_per_cell*self.household_number  # noqa
        self.assertTrue(0.9*total_households < len(households) <= total_households)  # noqa
        # Second check that at most 10% of households are empty.
        self.assertTrue(num_empty_households < 0.1*total_households)


if __name__ == '__main__':
    unittest.main()
