import unittest

import pyEpiabm as pe
from pyEpiabm.property import PlaceInfection
from pyEpiabm.tests.test_unit.parameter_config_tests import TestPyEpiabm


class TestPlaceInfection(TestPyEpiabm):
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
        super(TestPlaceInfection, cls).setUpClass()  # Sets up parameters
        cls.cell = pe.Cell()
        cls.microcell = pe.Microcell(cls.cell)
        cls.infector = pe.Person(cls.microcell)
        cls.infector.infectiousness = 1.0
        cls.infectee = pe.Person(cls.microcell)
        cls.place = pe.Place((1, 1), pe.property.PlaceType.Workplace,
                             cls.cell, cls.microcell)
        cls.place.add_person(cls.infector)
        cls.place.add_person(cls.infectee)
        cls.time = 1.0

    def test_place_susc(self):
        result = PlaceInfection.place_susc(self.place, self.infector,
                                           self.infectee, self.time)
        self.assertTrue(result > 0)
        self.assertIsInstance(result, float)

    def test_place_inf(self):
        result = PlaceInfection.place_inf(self.place, self.infector, self.time)
        self.assertTrue(result > 0)
        self.assertIsInstance(result, float)

        # Parameter free test
        place = pe.Place((1, 1), pe.property.PlaceType.OutdoorSpace,
                         self.cell, self.microcell)
        result = PlaceInfection.place_inf(place, self.infector, self.time)
        self.assertTrue(result > 0)
        self.assertIsInstance(result, float)

    def test_place_foi(self):
        result = PlaceInfection.place_foi(self.place, self.infector,
                                          self.infectee, self.time)
        self.assertTrue(result > 0)
        self.assertIsInstance(result, float)

    def test_place_case_isolation(self):
        # Not isolating (isolation_start_time = None)
        result = PlaceInfection.place_foi(self.place, self.infector,
                                          self.infectee, self.time)

        # Case isolate
        isolation_effectiveness = pe.Parameters.instance().intervention_params[
            'case_isolation']['isolation_effectiveness']
        self.infector.isolation_start_time = 1
        result_isolating = PlaceInfection.place_foi(self.place, self.infector,
                                                    self.infectee, self.time)
        self.assertEqual(result*isolation_effectiveness,
                         result_isolating)

    def test_place_place_closure(self):
        # Not place closure (closure_start_time = None)
        result = PlaceInfection.place_inf(self.place, self.infector, self.time)
        self.assertNotEqual(result, 0)

        # Place closure
        self.infector.microcell.closure_start_time = 1
        result_closure = PlaceInfection.place_inf(self.place, self.infector,
                                                  self.time)
        self.assertEqual(result_closure, 0)

    def test_place_household_quarantine(self):
        # Not in quarantine (quarantine_start_time = None)
        result = PlaceInfection.place_foi(self.place, self.infector,
                                          self.infectee, self.time)

        # Household quarantine
        quarantine_place_effectiveness = \
            pe.Parameters.instance().intervention_params[
                'household_quarantine']['quarantine_place_effectiveness']
        self.infector.quarantine_start_time = 1
        result_isolating = PlaceInfection.place_foi(self.place, self.infector,
                                                    self.infectee, self.time)
        place_idx = self.place.place_type.value - 1
        # foi scaled twice: infectiousness and susceptibility
        self.assertEqual(result*quarantine_place_effectiveness[place_idx]
                         * quarantine_place_effectiveness[place_idx],
                         result_isolating)

    def test_place_social_distancing(self):
        # Not in social distancing (distancing_start_time = None)
        result = PlaceInfection.place_susc(self.place, self.infector,
                                           self.infectee, self.time)
        place_idx = self.place.place_type.value - 1

        # Normal social distancing
        self.infector.microcell.distancing_start_time = 1
        self.infector.distancing_enhanced = False
        distancing_place_susc = pe.Parameters.instance().\
            intervention_params['social_distancing'][
                'distancing_place_susc']
        result_distancing = PlaceInfection.place_susc(
            self.place, self.infector, self.infectee, self.time)
        self.assertEqual(result*distancing_place_susc[place_idx],
                         result_distancing)
        # Enhanced social distancing
        self.infector.distancing_enhanced = True
        distancing_place_enhanced_susc = pe.Parameters.instance().\
            intervention_params['social_distancing'][
                'distancing_place_enhanced_susc']
        result_distancing_enhanced = PlaceInfection.place_susc(
            self.place, self.infector, self.infectee, self.time)
        self.assertEqual(result*distancing_place_enhanced_susc[place_idx],
                         result_distancing_enhanced)


if __name__ == '__main__':
    unittest.main()
