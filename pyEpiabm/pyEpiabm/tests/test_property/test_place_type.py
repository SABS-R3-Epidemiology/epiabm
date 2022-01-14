import unittest
import pyEpiabm as pe


class TestPLaceType(unittest.TestCase):
    """Test the 'PlaceType' enum.
    """

    def test_construct(self):
        statuses = [ # noqa
           pe.property.PlaceType.Hotel,
           pe.property.PlaceType.CareHome,
           pe.property.PlaceType.Restaurant,
           pe.property.PlaceType.OutdoorSpace]


if __name__ == '__main__':
    unittest.main()
