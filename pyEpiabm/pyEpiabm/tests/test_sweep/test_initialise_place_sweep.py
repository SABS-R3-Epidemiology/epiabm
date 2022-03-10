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
        self.microcell.add_place(1, (1, 1), PlaceType.CareHome)
        self.place = self.cell.places[0]
        pe.Parameters.instance().time_steps_per_day = 1
        self.time = 1

    def test_bind(self):
        """Tests that the update place sweep correctly binds
        the given population.
        """
        test_pop = self.pop
        test_sweep = pe.sweep.InitialisePlaceSweep()
        test_sweep.bind_population(test_pop)
        self.assertEqual(test_sweep._population.cells[0].
                         places[0].place_type, pe.property.PlaceType.CareHome)

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
        test_sweep = pe.sweep.InitialisePlaceSweep()
        test_sweep.bind_population(test_pop)
        test_sweep()
        mock_update.called_with(place)

        place.place_type = PlaceType.Workplace
        mock_update.side_effect = place.add_person(person)
        test_sweep()
        mock_update.called_with(place)


if __name__ == "__main__":
    unittest.main()
