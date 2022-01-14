import unittest
import pyEpiabm as pe


class TestUpdatePlaceSweep(unittest.TestCase):
    """Test the 'UpdatePlaceSweep' class.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """Initialises a population with one infected person. Sets up a
        single household containing this person.
        """
        cls.pop = pe.core.Population()
        cls.pop.add_cells(1)
        cls.cell = cls.pop.cells[0]
        cls.pop.cells[0].add_microcells(1)
        cls.microcell = cls.cell.microcells[0]
        cls.pop.cells[0].microcells[0].add_people(1)
        cls.person = cls.pop.cells[0].microcells[0].persons[0]
        cls.person.infection_status = pe.property.InfectionStatus.InfectMild
        cls.microcell.add_place(1, (1, 1), pe.property.PlaceType.Hotel)
        cls.place = cls.cell.places[0]
        pe.core.Parameters.instance().time_steps_per_day = 1
        cls.time = 1

    def test_bind(self):
        """Tests that the update place sweep correctly binds
        the given population.
        """
        test_sweep = pe.sweep.UpdatePlaceSweep()
        test_sweep.bind_population(self.pop)
        self.assertEqual(test_sweep._population.cells[0].
                         places[0].place_type, pe.property.PlaceType.Hotel)

    def test__call__(self):
        """Test whether the update place sweep function takes an
        initially empty place and correctly adds a person to
        the place.
        """
        test_sweep = pe.sweep.UpdatePlaceSweep()
        test_sweep.bind_population(self.pop)
        self.assertFalse(self.place.persons)

        self.place.add_person(self.person)
        test_sweep(self.time)
        self.assertTrue(self.place.persons)
        self.place.add_person(self.person)
        test_sweep(self.time)
        self.assertEqual(len(self.place.persons), 1)


if __name__ == "__main__":
    unittest.main()
