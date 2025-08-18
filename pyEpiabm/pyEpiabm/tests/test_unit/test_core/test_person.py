import unittest
from unittest.mock import patch, MagicMock

import pyEpiabm as pe
from pyEpiabm.tests.test_unit.parameter_config_tests import TestPyEpiabm


class TestPerson(TestPyEpiabm):
    """Test the 'Person' class.
    """
    def setUp(self) -> None:
        self.cell = pe.Cell()
        self.cell.add_microcells(1)
        self.microcell = self.cell.microcells[0]
        self.microcell.add_people(1)
        self.person = self.microcell.persons[0]

    def test__init__(self):
        self.assertGreaterEqual(self.person.age, 0)
        self.assertTrue(0 <= self.person.age < 85)
        self.assertTrue(0 <= self.person.age_group < 17)
        self.assertEqual(self.person.infectiousness, 0)
        self.assertEqual(self.person.num_times_infected, 0)
        self.assertEqual(self.person.microcell, self.microcell)

    @patch("random.randint")
    @patch("random.choices")
    def test_set_random_age(self, mock_choices, mock_int):
        mock_choices.return_value = [4]
        mock_int.return_value = 2
        self.person.set_random_age()
        mock_choices.assert_called_once()
        mock_int.assert_called_once()
        self.assertEqual(self.person.age, 22)

        # Testing now without age functionality in the model
        with patch('pyEpiabm.Parameters.instance') as mock_param:
            mock_param.return_value.use_ages = False
            self.person.set_random_age()
            mock_param.assert_called_once()
            self.assertEqual(self.person.age, None)
            self.assertEqual(self.person.age_group, 0)

    @patch("random.randint")
    @patch("random.choices")
    def test_update_age_group(self, mock_choices, mock_int):
        mock_choices.return_value = [4]
        mock_int.return_value = 2
        self.person.set_random_age()
        self.assertEqual(self.person.age_group, 4)
        self.person.age = 4
        self.person.update_age_group()
        self.assertEqual(self.person.age_group, 0)
        self.person.age = 85
        self.person.update_age_group()
        self.assertEqual(self.person.age_group, 16)

    def test_repr(self):
        self.assertEqual(repr(self.person),
                         f"Person ({self.person.id}), "
                         f"Age = {self.person.age}, "
                         f"Status = {self.person.infection_status}.")

    def test_is_symptomatic(self):
        self.person.update_status(pe.property.InfectionStatus.InfectMild)
        self.assertTrue(self.person.is_symptomatic())
        self.person.update_status(pe.property.InfectionStatus.InfectASympt)
        self.assertFalse(self.person.is_symptomatic())

    def test_is_infectious(self):
        self.assertFalse(self.person.is_infectious())
        self.person.update_status(pe.property.InfectionStatus.InfectMild)
        self.assertTrue(self.person.is_infectious())

    def test_is_susceptible(self):
        self.person.update_status(pe.property.InfectionStatus.Susceptible)
        self.assertTrue(self.person.is_susceptible())
        self.person.update_status(pe.property.InfectionStatus.InfectMild)
        self.assertFalse(self.person.is_susceptible())

    def test_update_status(self):
        self.person.update_status(pe.property.InfectionStatus.InfectMild)
        self.assertEqual(
            self.person.infection_status,
            pe.property.InfectionStatus.InfectMild)
        self.person.household = MagicMock()
        self.person.update_status(pe.property.InfectionStatus.Exposed)
        self.assertEqual(
            self.person.infection_status,
            pe.property.InfectionStatus.Exposed)
        self.assertEqual(len(self.person.household.susceptible_persons), 0)

    def test_configure_place(self):
        # Tests both the add and remove functions
        self.assertEqual(len(self.person.places), 0)
        test_place = pe.Place((1.0, 1.0), pe.property.PlaceType.Workplace,
                              self.cell, self.microcell)
        self.person.add_place(test_place)
        self.assertTrue(len(self.person.places) > 0)
        test_cell = pe.Cell()
        test_place_2 = pe.Place((1.0, 1.0), pe.property.PlaceType.Workplace,

                                test_cell, pe.Microcell(test_cell))
        self.assertRaises(AttributeError, self.person.add_place, test_place_2)

        self.person.remove_place(test_place)
        self.assertEqual(len(self.person.places), 0)
        self.assertRaises(KeyError, self.person.remove_place, test_place_2)

    def test_is_place_closed(self):
        closure_place_type = pe.Parameters.instance().intervention_params[
            'place_closure']['closure_place_type']
        # Not in place closure
        self.assertFalse(hasattr(self.person.microcell, 'closure_start_time'))
        self.assertFalse(self.person.is_place_closed(closure_place_type))
        # Place closure time starts but the place is not in closure_place_type
        self.person.microcell.closure_start_time = 1
        self.person.place_types.append(pe.property.PlaceType.Workplace)
        self.assertFalse(self.person.is_place_closed(closure_place_type))
        # Place closure time starts and the place is in closure_place_type
        self.person.place_types.append(pe.property.PlaceType.PrimarySchool)
        self.assertTrue(self.person.is_place_closed(closure_place_type))

    def test_vaccinate(self):
        self.person.vaccinate(time=5)
        self.assertTrue(self.person.is_vaccinated)
        self.assertEqual(self.person.date_vaccinated, 5)

    def test_set_id(self):
        init_id = self.microcell.id + "." + "." + \
                  str(len(self.microcell.persons) - 1)
        self.assertEqual(self.person.id, init_id)
        self.person.set_id("2.3.4.5")
        self.assertEqual(self.person.id, "2.3.4.5")
        self.assertRaises(TypeError, self.person.set_id, 2.0)
        self.assertRaises(ValueError, self.person.set_id, "0.1")
        self.assertRaises(ValueError, self.person.set_id, "1234")
        self.assertRaises(ValueError, self.person.set_id, "0.0.0.0.5")
        self.person.set_id("1.1.1.1")
        self.microcell.persons.append(self.person)
        new_person = pe.Person(self.microcell)
        self.microcell.persons.append(new_person)
        self.assertRaises(ValueError, new_person.set_id, "1.1.1.1")

    def test_set_time_of_recovery(self):
        self.person.set_time_of_recovery(time=5)
        self.assertEqual(self.person.time_of_recovery, 5)

    def test_increment_num_times_infected(self):
        self.person.increment_num_times_infected()
        self.assertEqual(self.person.num_times_infected, 1)

    def test_increment_secondary_infections_erroneous(self):
        with self.assertRaises(RuntimeError) as ve:
            self.person.increment_secondary_infections()
        self.assertEqual("Cannot call increment_secondary_infections "
                         "while secondary_infections_counts is empty",
                         str(ve.exception))

    def test_increment_secondary_infections(self):
        self.person.secondary_infections_counts = [2, 5, 1]
        self.person.increment_secondary_infections()
        self.assertListEqual(self.person.secondary_infections_counts,
                             [2, 5, 2])

    def test_set_latent_period(self):
        self.person.set_latent_period(latent_period=5)
        self.assertEqual(self.person.latent_period, 5)

    def test_set_exposure_period(self):
        self.person.set_exposure_period(exposure_period=5)
        self.assertEqual(self.person.exposure_period, 5)

    def test_set_infector_latent_period(self):
        self.person.set_infector_latent_period(latent_period=5)
        self.assertEqual(self.person.infector_latent_period, 5)

    def test_store_serial_interval_erroneous(self):
        with self.assertRaises(RuntimeError) as ve_1:
            self.person.store_serial_interval()
        self.assertEqual(str(ve_1.exception),
                         "Cannot call store_serial_interval while the"
                         " exposure_period is None")
        # Infect once with an exposure period for latent period failure
        with self.assertRaises(RuntimeError) as ve_2:
            self.person.set_exposure_period(2.0)
            self.person.store_serial_interval()
        self.assertEqual(str(ve_2.exception),
                         "Cannot call store_serial_interval while the"
                         " latent_period is None")
        # Add latent period, get success
        self.person.set_latent_period(3.0)
        self.person.time_of_status_change = 4.0
        self.person.store_serial_interval()
        # Do not add the exposure period for failure
        self.person.time_of_status_change = 19.0
        with self.assertRaises(RuntimeError) as ve_3:
            self.person.store_serial_interval()
        self.assertEqual(str(ve_3.exception),
                         "Cannot call store_serial_interval while the"
                         " exposure_period is None")

    def test_store_serial_interval(self):
        self.person.set_exposure_period(1.0)
        self.person.set_latent_period(1.0)
        self.person.time_of_status_change = 2.0
        self.person.store_serial_interval()
        self.person.set_exposure_period(2.0)
        self.person.set_latent_period(4.0)
        self.person.time_of_status_change = 6.0
        self.person.store_serial_interval()
        self.person.set_exposure_period(5.0)
        self.person.set_latent_period(4.0)
        self.person.time_of_status_change = 19.0
        self.person.store_serial_interval()
        self.assertDictEqual(self.person.serial_interval_dict,
                             {0.0: [2.0, 6.0], 10.0: [9.0]})
        self.assertIsNone(self.person.exposure_period)

    def test_store_generation_time_erroneous(self):
        with self.assertRaises(RuntimeError) as ve_1:
            self.person.store_generation_time()
        self.assertEqual(str(ve_1.exception),
                         "Cannot call store_generation_time while the"
                         " exposure_period is None")
        # Infect once with an exposure period for latent period failure
        with self.assertRaises(RuntimeError) as ve_2:
            self.person.set_exposure_period(2.0)
            self.person.store_generation_time()
        self.assertEqual(str(ve_2.exception),
                         "Cannot call store_generation_time while the"
                         " latent_period is None")
        # Add latent period with infector latent period failure
        with self.assertRaises(RuntimeError) as ve_3:
            self.person.set_latent_period(2.0)
            self.person.time_of_status_change = 6.0
            self.person.store_generation_time()
        self.assertEqual(str(ve_3.exception),
                         "Cannot call store_generation_time while the"
                         " infector_latent_period is None")
        # No error if the time_of_status_change <= latent_period +
        # exposure_period
        self.person.time_of_status_change = 4.0
        self.person.store_generation_time()
        self.assertEqual(self.person.generation_time_dict, {})
        # Add infector latent period, get success
        self.person.set_infector_latent_period(3.0)
        self.person.time_of_status_change = 8.0
        self.person.store_generation_time()
        self.assertEqual(self.person.generation_time_dict, {1.0: [5.0]})
        # Do not add the exposure period for failure
        self.person.time_of_status_change = 19.0
        with self.assertRaises(RuntimeError) as ve_4:
            self.person.store_generation_time()
        self.assertEqual(str(ve_4.exception),
                         "Cannot call store_generation_time while the"
                         " infector_latent_period is None")

    def test_store_generation_time(self):
        self.person.set_exposure_period(1.0)
        self.person.set_latent_period(1.0)
        self.person.set_infector_latent_period(1.0)
        self.person.time_of_status_change = 3.0
        self.person.store_generation_time()
        self.person.set_exposure_period(2.0)
        self.person.set_latent_period(1.0)
        self.person.set_infector_latent_period(3.0)
        self.person.time_of_status_change = 6.0
        self.person.store_generation_time()
        self.person.set_exposure_period(5.0)
        self.person.set_latent_period(4.0)
        self.person.set_infector_latent_period(5.0)
        self.person.time_of_status_change = 19.0
        self.person.store_generation_time()
        self.assertDictEqual(self.person.generation_time_dict,
                             {0.0: [2.0, 5.0], 5.0: [10.0]})
        self.assertIsNone(self.person.infector_latent_period)


if __name__ == '__main__':
    unittest.main()
