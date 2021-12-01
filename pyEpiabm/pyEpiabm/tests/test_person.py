import unittest
import pyEpiabm as pe


class TestPerson(unittest.TestCase):
    """
    Test the 'Person' class.
    """
    @classmethod
    def setUpClass(cls) -> None:
        cls.cell = pe.Cell()
        cls.microcell = pe.Microcell(cls.cell)
        cls.person = pe.Person(cls.microcell)

    def test__init__(self):
        self.assertEqual(self.person.age, 0)
        self.assertEqual(self.person.susceptibility, 0)
        self.assertEqual(self.person.infectiveness, 0)
        self.assertEqual(self.person.microcell, self.microcell)

    def test_repr(self):
        self.assertEqual(repr(self.person), "Person, Age = 0")

    def test_is_infectious(self):
        self.assertFalse(self.person.is_infectious())
        self.person.infection_status = pe.InfectionStatus.InfectMild
        self.assertTrue(self.person.is_infectious())

    def test_is_susceptible(self):
        self.person.infection_status = pe.InfectionStatus.Susceptible
        self.assertTrue(self.person.is_susceptible())
        self.person.infection_status = pe.InfectionStatus.InfectMild
        self.assertFalse(self.person.is_susceptible())


if __name__ == '__main__':
    unittest.main()
