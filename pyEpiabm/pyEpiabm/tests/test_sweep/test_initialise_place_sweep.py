import unittest
from unittest import mock

import pyEpiabm as pe
from pyEpiabm.property.infection_status import InfectionStatus
from pyEpiabm.property.place_type import PlaceType


class TestInitialisePlaceSweep(unittest.TestCase):
    """Test the 'UpdatePlaceSweep' class.
    """

    def setUp(self) -> None:
        """Initialises a population with one infected person. Sets up a
        single household containing this person.
        """
        self.pop = pe.Population()
        self.pop.add_cells(1)
        self.cell = self.pop.cells[0]
        self.pop.cells[0].add_microcells(1)
        self.microcell = self.cell.microcells[0]
        self.pop.cells[0].microcells[0].add_people(1)
        self.person = self.pop.cells[0].microcells[0].persons[0]
        self.person.update_status(InfectionStatus.InfectMild)
        self.microcell.add_place(1, (1, 1), PlaceType.Workplace)
        self.place = self.cell.places[0]
        pe.Parameters.instance().time_steps_per_day = 1
        self.time = 1
        self.params = pe.Parameters.instance().place_params

    def test_bind(self):
        """Tests that the update place sweep correctly binds
        the given population.
        """
        test_pop = self.pop
        test_sweep = pe.sweep.InitialisePlaceSweep()
        test_sweep.bind_population(test_pop)
        self.assertEqual(test_sweep._population.cells[0].
                         places[0].place_type, pe.property.PlaceType.Workplace)

    @mock.patch("pyEpiabm.sweep.InitialisePlaceSweep.create_age_weights")
    @mock.patch("pyEpiabm.sweep.UpdatePlaceSweep.update_place_group")
    def test__call__(self, mock_update, mock_weights):
        """Test whether the update place sweep function takes an
        initially empty place and correctly adds a person to
        the place.
        """
        test_pop = self.pop
        place = test_pop.cells[0].places[0]
        place.place_type = PlaceType.Workplace
        person = test_pop.cells[0].persons[0]
        mock_update.return_value = None
        mock_weights.return_value = [[person], [1]]

        test_sweep = pe.sweep.InitialisePlaceSweep()
        test_sweep.bind_population(test_pop)
        test_sweep()
        mock_update.assert_called_with(place, group_index=-1,
                                       mean_capacity=14.28,
                                       person_list=[person])
        mock_weights.assert_called_with(place, self.params)

        place.place_type = PlaceType.SecondarySchool
        mock_update.side_effect = place.add_person(person)
        test_sweep()
        mock_update.assert_called_with(place, group_size=25,
                                       person_list=[person],
                                       person_weights=[1],
                                       mean_capacity=1010)

        place.place_type = PlaceType.CareHome
        mock_update.side_effect = place.add_person(person)
        test_sweep()
        mock_update.assert_called_with(place)

    def test_weights_func(self):
        test_pop = self.pop
        place = test_pop.cells[0].places[0]
        person = test_pop.cells[0].persons[0]
        person.age = 35
        test_sweep = pe.sweep.InitialisePlaceSweep()
        test_sweep.bind_population(test_pop)

        [list, weights] = test_sweep.create_age_weights(place, self.params)
        self.assertListEqual([person], list)
        self.assertEqual(weights[0], self.params["age_group3_prop"][3])

        place.add_person(person)
        [list, weights] = test_sweep.create_age_weights(place, self.params)
        self.assertListEqual([], list)
        self.assertEqual(weights, [])


if __name__ == "__main__":
    unittest.main()
