import random
import math
import unittest
from unittest.mock import patch
from parameterized import parameterized

import pyEpiabm as pe
from pyEpiabm.routine import ToyPopulationFactory


numReps = 1


class TestPopConfig(unittest.TestCase):
    """Test the 'ToyPopConfig' class.
    """
    @parameterized.expand([(random.randint(1000, 10000),
                            random.randint(1, 10),
                            random.randint(1, 10))
                          for _ in range(numReps)])
    def test_make_pop(self, pop_size, cell_number, microcell_number):
        """Tests for when the population is implemented by default with
        no households. Parameters are assigned at random.
        """
        # Population is initialised with no households
        pop_params = {"population_size": pop_size, "cell_number": cell_number,
                      "microcell_number": microcell_number}
        test_pop = ToyPopulationFactory.make_pop(pop_params)

        total_people = 0
        count_non_empty_cells = 0
        for cell in test_pop.cells:
            for microcell in cell.microcells:
                total_people += len(microcell.persons)
            if len(cell.persons) > 0:
                count_non_empty_cells += 1
        # Test there are at least one non-empty cell
        self.assertTrue(count_non_empty_cells >= 1)

        # Test that everyone in the population has been assigned a microcell
        self.assertEqual(total_people, pop_size)

        # Test a population class object is returned
        self.assertIsInstance(test_pop, pe.Population)

    @patch("numpy.random.multinomial")
    @patch('logging.exception')
    def test_make_pop_exception(self, patch_log, patch_random):
        """Tests for when the population is implemented with errors
        """
        patch_random.side_effect = ValueError
        # Population is initialised with no households
        pop_params = {"population_size": 10, "cell_number": 1,
                      "microcell_number": 1}
        ToyPopulationFactory.make_pop(pop_params)
        patch_log.assert_called_once_with("Fatal error while generating"
                                          + " toy population")

    def summarise_pop(self, pop):
        # Returns lists of cell and microcell wise populations
        # Not a testing function, but used in test below

        pop_cells = []  # List of populations in each cell of population
        pop_microcells = []  # List of populations in each microcell
        for cell in pop.cells:
            pop_cells.append(len(cell.persons))
            for microcell in cell.microcells:
                pop_microcells.append(len(microcell.persons))
        return pop_cells, pop_microcells

    @parameterized.expand([(random.randint(1000, 10000),
                            random.randint(5, 10),
                            random.randint(2, 10),
                            random.randint(1, 100))
                          for _ in range(numReps)])
    def test_pop_seed(self, pop_size, cell_number, microcell_number, seed):
        """Tests for when the population is implemented by default with
        no households. Parameters are assigned at random.
        """
        # Define parameters for population generation
        pop_params = {"population_size": pop_size, "cell_number": cell_number,
                      "microcell_number": microcell_number,
                      "population_seed": seed}

        # Create two identical populations with the same seed
        seed_pop = ToyPopulationFactory.make_pop(pop_params)
        comp_pop = ToyPopulationFactory.make_pop(pop_params)

        self.assertEqual(str(seed_pop), str(comp_pop))

        seed_cells, seed_microcells = self.summarise_pop(seed_pop)
        comp_cells, comp_microcells = self.summarise_pop(comp_pop)
        self.assertEqual(seed_cells, comp_cells)
        self.assertEqual(seed_microcells, comp_microcells)

        # Also compare to a population with a different seed
        pop_params["population_seed"] = seed + 1  # Change seed of population
        diff_pop = ToyPopulationFactory().make_pop(pop_params)

        diff_cells, diff_microcells = self.summarise_pop(diff_pop)
        self.assertNotEqual(seed_cells, diff_cells)
        self.assertNotEqual(seed_microcells, diff_microcells)

    @parameterized.expand([(random.randint(1000, 10000) * numReps,
                            random.randint(1, 10) * numReps,
                            random.randint(1, 10) * numReps,
                            random.randint(1, 10) * numReps)
                          for _ in range(numReps)])
    def test_if_households(self, pop_size, cell_number, microcell_number,
                           household_number):
        """Tests when households are implemented.
        """

        # Initialises population with households
        pop_params = {"population_size": pop_size, "cell_number": cell_number,
                      "microcell_number": microcell_number,
                      "household_number": household_number}
        toy_pop = ToyPopulationFactory.make_pop(pop_params)
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
        # Some households may be empty so won't be included
        total_households = cell_number * microcell_number \
            * household_number
        self.assertTrue(len(households) <= total_households)
        self.assertTrue(num_empty_households < total_households)

    @parameterized.expand([(random.randint(1000, 10000) * numReps,
                            random.randint(1, 10) * numReps,
                            random.randint(1, 10) * numReps,
                            random.randint(1, 10) * numReps)
                          for _ in range(numReps)])
    def test_if_places(self, pop_size, cell_number, microcell_number,
                       place_number):
        """Tests when places are implemented.
        """

        # Initialises population with places
        pop_params = {"population_size": pop_size, "cell_number": cell_number,
                      "microcell_number": microcell_number,
                      "place_number": place_number}
        toy_pop = ToyPopulationFactory.make_pop(pop_params)

        places = []
        for cell in toy_pop.cells:
            for microcell in cell.microcells:
                places += microcell.places

        # Test the correct number of place shave been added to each microcell
        self.assertEqual(place_number,
                         len(toy_pop.cells[0].microcells[0].places))

    def test_assign_cell_locations_rand(self):
        pop_params = {"population_size": 10, "cell_number": 2,
                      "microcell_number": 1}
        test_pop = ToyPopulationFactory.make_pop(pop_params)
        for cell in test_pop.cells:
            self.assertEqual(cell.location[0], 0)
            self.assertEqual(cell.location[1], 0)
        ToyPopulationFactory.assign_cell_locations(test_pop)
        for cell in test_pop.cells:
            self.assertTrue((0 < cell.location[0]) & (1 > cell.location[0]))
            self.assertTrue((0 < cell.location[1]) & (1 > cell.location[1]))

        with self.assertRaises(ValueError):
            ToyPopulationFactory.assign_cell_locations(test_pop,
                                                       method='other')

    @parameterized.expand([(random.randint(2, 20) * numReps,)
                           for _ in range(numReps)])
    def test_assign_cell_locations_unix(self, cell_num):
        pop_params = {"population_size": 100, "cell_number": cell_num,
                      "microcell_number": 1}
        test_pop = ToyPopulationFactory.make_pop(pop_params)
        ToyPopulationFactory.assign_cell_locations(test_pop, "uniform_x")
        for i, cell in enumerate(test_pop.cells):
            self.assertAlmostEqual(cell.location[0], i / (cell_num - 1))
            self.assertAlmostEqual(cell.location[1], 0)

    @parameterized.expand([(random.randint(2, 20) * numReps,)
                          for _ in range(numReps)])
    def test_assign_cell_locations_grid(self, cell_num):
        pop_params = {"population_size": 100, "cell_number": cell_num,
                      "microcell_number": 1}
        test_pop = ToyPopulationFactory.make_pop(pop_params)
        ToyPopulationFactory.assign_cell_locations(test_pop, "grid")
        grid_len = math.ceil(math.sqrt(cell_num))
        for i, cell in enumerate(test_pop.cells):
            self.assertAlmostEqual(cell.location[0],
                                   (i % grid_len) / (grid_len - 1))
            self.assertAlmostEqual(cell.location[1],
                                   (i // grid_len) / (grid_len - 1))

    def test_assign_cell_locations_known_grid(self):
        pop_params = {"population_size": 100, "cell_number": 4,
                      "microcell_number": 1}
        test_pop = ToyPopulationFactory.make_pop(pop_params)
        ToyPopulationFactory.assign_cell_locations(test_pop, "grid")
        x_pos = [0, 1, 0, 1]
        y_pos = [0, 0, 1, 1]
        for i, cell in enumerate(test_pop.cells):
            self.assertAlmostEqual(cell.location[0], x_pos[i])
            self.assertAlmostEqual(cell.location[1], y_pos[i])


if __name__ == '__main__':
    unittest.main()
