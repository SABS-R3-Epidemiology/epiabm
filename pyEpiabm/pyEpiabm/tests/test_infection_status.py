import unittest
import pyEpiabm as pe


class TestInfectionStatus(unittest.TestCase):
    """
    Test the 'InfectionStatus' enum.
    """

    def test_construct(self):
        statuses = [ # noqa
            pe.InfectionStatus.Susceptible,
            pe.InfectionStatus.Exposed,
            pe.InfectionStatus.InfectASympt,
            pe.InfectionStatus.InfectMild,
            pe.InfectionStatus.InfectGP,
            pe.InfectionStatus.InfectHosp,
            pe.InfectionStatus.InfectICU,
            pe.InfectionStatus.InfectICURecov,
            pe.InfectionStatus.Recovered,
            pe.InfectionStatus.Dead]


if __name__ == '__main__':
    unittest.main()
