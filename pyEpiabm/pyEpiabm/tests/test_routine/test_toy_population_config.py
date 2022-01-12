import unittest
import pyEpiabm as pe
from parameterized import parameterized
import random


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
        test_pop = pe.ToyPopulationFactory().make_pop(pop_size, cell_number,
                                                      microcell_number)

        total_people = 0
        count_non_empty_cells = 0
        for cell in test_pop.cells:
            for microcell in cell.microcells:
                total_people += len(microcell.persons)
            if len(cell.persons) > 0:
                count_non_empty_cells += 1
        # test there are at least one non-empty cell.
        self.assertTrue(count_non_empty_cells >= 1)

        # test that everyone in the population has been assigned a microcell.
        self.assertEqual(total_people, pop_size)

        # test a population class object is returned.
        self.assertIsInstance(test_pop, pe.Population)

    @parameterized.expand([(random.randint(1000, 10000) * numReps,
                            random.randint(1, 10) * numReps,
                            random.randint(1, 10) * numReps,
                            random.randint(1, 10) * numReps)
                          for _ in range(numReps)])
    def test_if_households(self, pop_size, cell_number, microcell_number,
                           household_number):
        """Tests when households are implemented.
        """

        # Initialises population with households.
        toy_pop = pe.ToyPopulationFactory().make_pop(pop_size, cell_number,
                                                     microcell_number,
                                                     household_number)
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

        # Initialises population with places.
        toy_pop = pe.ToyPopulationFactory().make_pop(pop_size, cell_number,
                                                     microcell_number,
                                                     place_number=place_number)

        places = []
        for cell in toy_pop.cells:
            for microcell in cell.microcells:
                places += microcell.places

        # Test the correct number of place shave been added to each microcell.
        self.assertEqual(place_number,
                         len(toy_pop.cells[0].microcells[0].places))


if __name__ == '__main__':
    unittest.main()
