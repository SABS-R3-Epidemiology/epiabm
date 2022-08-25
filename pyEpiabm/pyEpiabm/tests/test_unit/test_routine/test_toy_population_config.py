import random
import math
import unittest
from unittest.mock import patch
from parameterized import parameterized

import pyEpiabm as pe
from pyEpiabm.routine import ToyPopulationFactory
from pyEpiabm.tests.test_unit.parameter_config_tests import TestPyEpiabm


numReps = 1


class TestPopConfig(TestPyEpiabm):
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
        patch_log.assert_called_once_with("ValueError in ToyPopulation"
                                          + "Factory.make_pop()")

    @patch("numpy.random.seed")
    @patch("random.seed")
    def test_random_seed_param(self, mock_random, mock_np_random, n=42):
        pop_params = {"population_size": 100, "cell_number": 10,
                      "microcell_number": 10, "population_seed": n}
        ToyPopulationFactory.make_pop(pop_params)

        mock_random.assert_called_once_with(n)
        mock_np_random.assert_called_once_with(n)

    @parameterized.expand([(random.randint(1000, 10000) * numReps,
                            random.randint(1, 10) * numReps,
                            random.randint(1, 10) * numReps)
                          for _ in range(numReps)])
    def test_if_households(self, pop_size, cell_number, microcell_number):
        #Tests when households are implemented.
        
        # Initialises population with households
        pop_params = {"population_size": pop_size, "cell_number": cell_number,
                      "microcell_number": microcell_number, "use_households": True}
        toy_pop = ToyPopulationFactory.make_pop(pop_params)
        people_not_in_household = []
        for cell in toy_pop.cells:
            for microcell in cell.microcells:
                for person in microcell.persons:
                    if person.household == None:
                        people_not_in_household.append(person)

        #Check that everyone has been put into household
        self.assertEqual(len(people_not_in_household), 0)
                        

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

    @patch('logging.exception')
    def test_assign_cell_locations_rand(self, mock_log):
        pop_params = {"population_size": 10, "cell_number": 2,
                      "microcell_number": 2}
        test_pop = ToyPopulationFactory.make_pop(pop_params)
        for cell in test_pop.cells:
            with self.subTest(cell=cell):
                self.assertEqual(cell.location[0], 0)
                self.assertEqual(cell.location[1], 0)
        ToyPopulationFactory.assign_cell_locations(test_pop)
        for cell in test_pop.cells:
            with self.subTest(cell=cell):
                self.assertTrue((0 < cell.location[0])
                                & (1 > cell.location[0]))
                self.assertTrue((0 < cell.location[1])
                                & (1 > cell.location[1]))

        mock_log.assert_not_called()
        ToyPopulationFactory.assign_cell_locations(test_pop, method='other')
        mock_log.assert_called_once_with("ValueError in ToyPopulationFactory"
                                         + ".assign_cell_locations()")

    @parameterized.expand([(random.randint(2, 20) * numReps,
                            random.randint(2, 20) * numReps)
                           for _ in range(numReps)])
    def test_assign_cell_locations_unix(self, cell_num, mcell_num):
        pop_params = {"population_size": 100, "cell_number": cell_num,
                      "microcell_number": mcell_num}
        test_pop = ToyPopulationFactory.make_pop(pop_params)
        ToyPopulationFactory.assign_cell_locations(test_pop, "uniform_x")
        for i, cell in enumerate(test_pop.cells):
            with self.subTest(cell=cell):
                self.assertAlmostEqual(cell.location[0], i / (cell_num - 1))
                self.assertAlmostEqual(cell.location[1], 0)
                for j, mcell in enumerate(cell.microcells):
                    with self.subTest(mcell=mcell):
                        self.assertAlmostEqual(mcell.location[0],
                                               cell.location[0])
                        self.assertAlmostEqual(mcell.location[1],
                                               j / (mcell_num - 1))

    @parameterized.expand([(random.randint(2, 20) * numReps,
                            random.randint(2, 20) * numReps)
                          for _ in range(numReps)])
    def test_assign_cell_locations_grid(self, cell_num, mcell_num):
        pop_params = {"population_size": 100, "cell_number": cell_num,
                      "microcell_number": mcell_num}
        test_pop = ToyPopulationFactory.make_pop(pop_params)
        ToyPopulationFactory.assign_cell_locations(test_pop, "grid")
        grid_len = math.ceil(math.sqrt(cell_num))
        for i, cell in enumerate(test_pop.cells):
            with self.subTest(cell=cell):
                self.assertAlmostEqual(cell.location[0],
                                       (i % grid_len) / (grid_len - 1))
                self.assertAlmostEqual(cell.location[1],
                                       (i // grid_len) / (grid_len - 1))
                mcell_len = math.ceil(math.sqrt(len(cell.microcells)))
                for j, mcell in enumerate(cell.microcells):
                    with self.subTest(mcell=mcell):
                        test_x = (cell.location[0] +
                                  (j % mcell_len - .5 * (mcell_len - 1)) /
                                  (grid_len * (mcell_len - 1)))
                        test_y = (cell.location[1] +
                                  (j // mcell_len - .5 * (mcell_len - 1)) /
                                  (grid_len * (mcell_len - 1)))
                        self.assertAlmostEqual(mcell.location[0], test_x)
                        self.assertAlmostEqual(mcell.location[1], test_y)

    def test_assign_cell_locations_known_grid(self):
        pop_params = {"population_size": 100, "cell_number": 4,
                      "microcell_number": 4}
        test_pop = ToyPopulationFactory.make_pop(pop_params)
        ToyPopulationFactory.assign_cell_locations(test_pop, "grid")
        x_pos = [0, 1, 0, 1]
        y_pos = [0, 0, 1, 1]
        mx_pos0 = [-.25, .25, -.25, .25]
        my_pos0 = [-.25, -.25, .25, .25]
        mx_pos1 = [.75, 1.25, .75, 1.25]
        my_pos1 = [.75, .75, 1.25, 1.25]
        for i, cell in enumerate(test_pop.cells):
            with self.subTest(cell=cell):
                self.assertAlmostEqual(cell.location[0], x_pos[i])
                self.assertAlmostEqual(cell.location[1], y_pos[i])
        for j, mcell in enumerate(test_pop.cells[0].microcells):
            with self.subTest(cell=cell):
                self.assertAlmostEqual(mcell.location[0], mx_pos0[j])
                self.assertAlmostEqual(mcell.location[1], my_pos0[j])
        for j, mcell in enumerate(test_pop.cells[3].microcells):
            with self.subTest(cell=cell):
                self.assertAlmostEqual(mcell.location[0], mx_pos1[j])
                self.assertAlmostEqual(mcell.location[1], my_pos1[j])


if __name__ == '__main__':
    unittest.main()
