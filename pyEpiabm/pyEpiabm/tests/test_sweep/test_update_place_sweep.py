import unittest
from unittest import mock

from pyEpiabm.property.place_type import PlaceType
from pyEpiabm.core.population import Population
from pyEpiabm.core.parameters import Parameters
from pyEpiabm.sweep.update_place_sweep import UpdatePlaceSweep


class TestUpdatePlaceSweep(unittest.TestCase):
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

    @mock.patch('logging.warning')
    def test_update_place(self, log_mock):
        """Test explicitly the update place function.
        """
        test_pop = self.pop
        place = test_pop.cells[0].places[0]
        person = test_pop.cells[0].persons[0]
        test_sweep = UpdatePlaceSweep()
        test_sweep.bind_population(test_pop)
        test_sweep.update_place_group(place)
        self.assertTrue(place.persons)
        self.assertDictEqual(place.person_groups, {0: [person]})
        self.place.empty_place()
        test_sweep.update_place_group(place, person_list=[person],
                                      group_index=1)
        self.assertDictEqual(place.person_groups,
                             {0: [], 1: [person]})
        self.place.empty_place([1])
        test_sweep.update_place_group(place, person_list=[person],
                                      person_weights=[1], group_index=1)
        self.assertDictEqual(place.person_groups,
                             {0: [], 1: [person]})
        self.place.empty_place()
        test_sweep.update_place_group(place, person_list=[])
        log_mock.called

        self.assertRaises(AssertionError, test_sweep.update_place_group, place,
                          person_list=[person], person_weights=[],
                          group_index=1)

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
        mock_update.called_with(place)

        place.place_type = PlaceType.Workplace
        place.add_person(person, 1)
        place.remove_person(person)
        test_sweep(1)
        mock_update.called_with(place)


if __name__ == "__main__":
    unittest.main()
