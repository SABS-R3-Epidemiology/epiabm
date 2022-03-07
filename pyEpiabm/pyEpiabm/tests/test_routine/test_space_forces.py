import unittest

import pyEpiabm as pe
from pyEpiabm.property import InfectionStatus
from pyEpiabm.routine import SpatialInfection


class TestSpatialInfection(unittest.TestCase):
    """Test the 'PlaceInfection' class, which contains the
    infectiousness and susceptibility calculations that
    determine whether infection events occur within places.
    Each function should return a number greater than 0.
    """
    @classmethod
    def setUpClass(cls) -> None:
        """Intialise a population with one infector and one
        infectee, both in the same place and household.
        """
        cls.cell = pe.Cell()
        cls.cell.add_microcells(1)
        cls.microcell = cls.cell.microcells[0]
        cls.microcell.add_people(2)
        cls.infector = cls.microcell.persons[0]
        cls.infectee = cls.microcell.persons[1]
        cls.timestep = 1
        pe.Parameters.instance().basic_reproduction_num = 2.8

    def test_space_susc(self):
        result = SpatialInfection.space_susc(self.cell, self.infectee,
                                             self.timestep)
        self.assertTrue(result > 0)
        self.assertIsInstance(result, float)

    def test_space_inf(self):
        result = SpatialInfection.space_inf(self.cell, self.infector,
                                            self.timestep)
        self.assertTrue(result > 0)
        self.assertIsInstance(result, float)

    def test_space_foi(self):
        result = SpatialInfection.space_foi(self.cell, self.cell,
                                            self.infector, self.infectee,
                                            self.timestep)
        self.assertTrue(result > 0)
        self.assertIsInstance(result, float)

    def test_cell_inf(self):
        self.infector.update_status(InfectionStatus.InfectMild)
        result = SpatialInfection.cell_inf(self.cell, self.timestep)
        self.assertIsInstance(result, float)
        self.assertTrue(result >= 0)


if __name__ == '__main__':
    unittest.main()
