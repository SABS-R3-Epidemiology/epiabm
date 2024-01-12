import unittest
from unittest import mock

from pyEpiabm.property import PlaceType
from pyEpiabm.core import Parameters, Population
from pyEpiabm.sweep import UpdatePlaceSweep
from pyEpiabm.tests.test_unit.parameter_config_tests import TestPyEpiabm


class TestUpdatePlaceSweep(TestPyEpiabm):
    """Test the 'UpdatePlaceSweep' class.
    """

    def setUp(self) -> None:
        """Initialises a population with one infected person. Sets up a
        single household containing this person.
        """
        self.pop = Population()
        self.pop.add_cells(1)
        self.cell = self.pop.cells[0]
        self.pop.cells[0].add_microcells(1)
        self.microcell = self.cell.microcells[0]
        self.pop.cells[0].microcells[0].add_people(1)
        self.person = self.pop.cells[0].microcells[0].persons[0]
        self.microcell.add_place(1, (1, 1), PlaceType.Workplace)
        self.place = self.cell.places[0]
        Parameters.instance().time_steps_per_day = 1
        Parameters.instance().carehome_params['carehome_minimum_age'] = 65
        self.time = 1.0

    def test_bind(self):
        """Tests that the update place sweep correctly binds
        the given population.
        """
        test_pop = self.pop
        test_sweep = UpdatePlaceSweep()
        test_sweep.bind_population(test_pop)
        self.assertEqual(test_sweep._population.cells[0].
                         places[0].place_type, PlaceType.Workplace)

    @mock.patch("random.randint")
    @mock.patch('logging.warning')
    def test_update_place(self, log_mock, mock_random):
        """Test explicitly the update place function.
        """
        test_pop = self.pop
        place = test_pop.cells[0].places[0]
        person = test_pop.cells[0].persons[0]
        test_sweep = UpdatePlaceSweep()
        test_sweep.bind_population(test_pop)
        mock_random.return_value = 0

        test_sweep.update_place_group(place)
        self.assertTrue(place.persons)
        self.assertDictEqual(place.person_groups, {0: [person]})
        self.place.empty_place()
        mock_random.return_value = 1
        test_sweep.update_place_group(place, person_list=[person],
                                      group_size=1)
        self.assertDictEqual(place.person_groups,
                             {0: [], 1: [person]})

        # Test when max capacity not set
        self.place.empty_place([1])
        test_sweep.update_place_group(place, person_list=[person],
                                      power_law_params=[3, 1, 4])
        self.assertDictEqual(place.person_groups,
                             {0: [], 1: [person]})
        self.assertRaises(AssertionError, test_sweep.update_place_group,
                          place, person_list=[person], power_law_params=[3])

        # Test when group index set
        self.place.empty_place([1])
        test_sweep.update_place_group(place, person_list=[person],
                                      group_index=1)
        self.assertDictEqual(place.person_groups,
                             {0: [], 1: [person]})

        # Test with weights
        self.place.empty_place([1])
        test_sweep.update_place_group(place, person_list=[person],
                                      person_weights=[1])
        self.assertDictEqual(place.person_groups,
                             {0: [], 1: [person]})
        self.place.empty_place()
        test_sweep.update_place_group(place, person_list=[])
        log_mock.assert_called

        # Test when weigts are the wrong size
        self.assertRaises(AssertionError, test_sweep.update_place_group, place,
                          person_list=[person], person_weights=[])
        test_sweep.update_place_group(place, person_list=[person],
                                      person_weights=[0])
        log_mock.assert_called

        # Change to care homes
        self.place.place_type = PlaceType.CareHome

        # Test for care home resident
        self.place.empty_place()
        person.age = 70
        mock_random.return_value = 1
        test_sweep.update_place_group(place, person_list=[person],
                                      group_size=1)
        self.assertDictEqual(place.person_groups,
                             {0: [], 1: [person]})
        self.assertTrue(person.care_home_resident)

        # Test for key worker
        self.place.empty_place()
        person.age = 45
        mock_random.return_value = 1
        test_sweep.update_place_group(place, person_list=[person],
                                      group_size=1)
        self.assertDictEqual(place.person_groups, {0: [person], 1: []})
        self.assertTrue(person.key_worker)

    @mock.patch('random.random')
    def test_key_worker_assignment(self, mock_random):
        mock_random.return_value = 0

        Parameters.instance().use_key_workers = 0.5

        test_pop = self.pop
        place = test_pop.cells[0].places[0]
        person = test_pop.cells[0].persons[0]
        test_sweep = UpdatePlaceSweep()
        test_sweep.bind_population(test_pop)

        test_sweep.update_place_group(place, person_list=[person],
                                      group_size=1)
        self.assertTrue(person.key_worker)

    @mock.patch("numpy.random.poisson")
    def test_update_place_no_groups(self, mock_poisson):
        """Test handling of zero groups from poisson distribution.
        First call of mock gives non-zero capacity"""
        test_pop = self.pop
        place = test_pop.cells[0].places[0]
        person = test_pop.cells[0].persons[0]
        test_sweep = UpdatePlaceSweep()
        test_sweep.bind_population(test_pop)
        mock_poisson.side_effect = [5, 0]

        test_sweep.update_place_group(place, person_list=[person],
                                      group_size=1)
        self.assertDictEqual(place.person_groups,
                             {0: [person]})

    @mock.patch("pyEpiabm.sweep.UpdatePlaceSweep.update_place_group")
    def test__call__(self, mock_update):
        """Test whether the update place sweep function takes an
        initially empty place and correctly adds a person to
        the place.
        """
        test_pop = self.pop
        place = test_pop.cells[0].places[0]
        person = test_pop.cells[0].persons[0]
        mock_update.return_value = None
        test_sweep = UpdatePlaceSweep()
        test_sweep.bind_population(test_pop)
        self.assertFalse(place.persons)

        place.place_type = PlaceType.OutdoorSpace
        test_sweep(1)
        mock_update.assert_called_with(place)

        place.place_type = PlaceType.Workplace
        place.add_person(person, 1)
        place.remove_person(person)
        test_sweep(1)
        mock_update.assert_called


if __name__ == "__main__":
    unittest.main()
