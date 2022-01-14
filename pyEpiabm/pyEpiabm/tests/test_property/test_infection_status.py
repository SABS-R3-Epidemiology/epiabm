import unittest

from pyEpiabm.property import InfectionStatus


class TestInfectionStatus(unittest.TestCase):
    """Test the 'InfectionStatus' enum.
    """

    def test_construct(self):
        statuses = [ # noqa
            InfectionStatus.Susceptible,
            InfectionStatus.Exposed,
            InfectionStatus.InfectASympt,
            InfectionStatus.InfectMild,
            InfectionStatus.InfectGP,
            InfectionStatus.InfectHosp,
            InfectionStatus.InfectICU,
            InfectionStatus.InfectICURecov,
            InfectionStatus.Recovered,
            InfectionStatus.Dead]


if __name__ == '__main__':
    unittest.main()
