import unittest
import pyEpiabm as pe


class TestPLaceType(unittest.TestCase):
    """Test the 'PlaceType' enum.
    """

    def test_construct(self):
        statuses = [ # noqa
            pe.PlaceType.Hotel,
            pe.PlaceType.CareHome,
            pe.PlaceType.Resturant,
            pe.PlaceType.OutdoorSpace]


if __name__ == '__main__':
    unittest.main()
