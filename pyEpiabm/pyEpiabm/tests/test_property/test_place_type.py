import unittest

import pyEpiabm as pe


class TestPLaceType(unittest.TestCase):
    """Test the 'PlaceType' enum.
    """

    def test_construct(self):
        statuses = [ # noqa
           pe.property.PlaceType.Workplace,
           pe.property.PlaceType.CareHome,
           pe.property.PlaceType.SecondarySchool,
           pe.property.PlaceType.OutdoorSpace]


if __name__ == '__main__':
    unittest.main()
