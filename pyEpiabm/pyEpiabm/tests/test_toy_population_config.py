import unittest
import pyEpiabm as pe
from parameterized import parameterized
import random
from pyEpiabm.toy_population_config import ToyPopulation

numReps = 1


class TestPopConfig(unittest.TestCase):
    """Test the Toy Population class.
    """
    @parameterized.expand([(random.randint(1000, 10000),
                            random.randint(1, 10),
                            random.randint(1, 10),
                            random.randint(1, 10))
                          for _ in range(numReps)])
    def test_make_pop(self, pop_size, cell_number, microcell_per_cell,
                      household_number):
        """Tests for when the population is implemented by default with
        no households.
        """
        # Population is initialised with no households
        test_pop = pe.ToyPopulation().make_pop(pop_size, cell_number,
                                               microcell_per_cell,
                                               household_number)

        total_people = 0
        count_non_empty_cells = 0
        count_non_trivial_households = 0
        for cell in test_pop.cells:
            for microcell in cell.microcells:
                total_people = total_people + len(microcell.persons)
                for person in microcell.persons:
                    if len(person.household.persons) > 1:
                        count_non_trivial_households += 1
            if len(cell.persons) > 0:
                count_non_empty_cells += 1
        # test there are at least one non-empty cell.
        self.assertTrue(count_non_empty_cells > 1)

        # test that everyone in the population has been assigned a microcell.
        self.assertEqual(total_people, pop_size)

        # test that each household is trivial (contains one person).
        self.assertEqual(count_non_trivial_households, 0)

        # test a population class object is returned.
        self.assertIsInstance(test_pop, pe.Population)

    @parameterized.expand([(random.randint(1000, 10000) * numReps,
                            random.randint(1, 10) * numReps,
                            random.randint(1, 10) * numReps,
                            random.randint(1, 10) * numReps)
                          for _ in range(numReps)])
    def test_if_households(self, pop_size, cell_number, microcell_per_cell,
                           household_number):
        """Tests when households are implemented.
        """
        if_households = 1.0
        # Tests that if_households only takes boolean input.
        self.assertRaises(TypeError, ToyPopulation().make_pop, pop_size,
                          cell_number, microcell_per_cell,
                          household_number,
                          if_households)
        # Initialises population with households.
        if_households = True
        toy_pop = pe.ToyPopulation().make_pop(pop_size, cell_number,
                                              microcell_per_cell,
                                              household_number,
                                              if_households)
        total_people = 0
        households = []
        num_empty_households = 0
        for cell in toy_pop.cells:
            for microcell in cell.microcells:
                for person in microcell.persons:
                    if person.household not in households:
                        households.append(person.household)
                    if len(person.household.persons) == 0:
                        num_empty_households += 1
                    total_people += len(person.household.persons)
        # Some households may be empty so won't be included.
        total_households = cell_number * microcell_per_cell \
            * household_number
        self.assertTrue(len(households) <= total_households)
        self.assertTrue(num_empty_households < total_households)


if __name__ == '__main__':
    unittest.main()
