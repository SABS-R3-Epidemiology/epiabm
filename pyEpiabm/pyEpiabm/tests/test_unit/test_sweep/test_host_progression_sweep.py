import unittest
from unittest import mock
import numpy as np
import pandas as pd

import pyEpiabm as pe
from pyEpiabm.property import InfectionStatus
from pyEpiabm.tests.test_unit.parameter_config_tests import TestPyEpiabm


class TestHostProgressionSweep(TestPyEpiabm):
    """Tests the 'HostProgressionSweep' class.
    """

    def setUp(self) -> None:
        """Sets up two populations we can use throughout the test.
        3 people are located in one microcell.
        """
        # Example coefficients for StateTransitionMatrix

        self.coefficients = {
            "prob_exposed_to_asympt": 0.4,
            "prob_exposed_to_mild": 0.4,
            "prob_exposed_to_gp": 0.2,
            "prob_gp_to_recov": 0.9,
            "prob_gp_to_hosp": 0.1,
            "prob_hosp_to_recov": 0.6,
            "prob_hosp_to_icu": 0.2,
            "prob_hosp_to_death": 0.2,
            "prob_icu_to_icurecov": 0.5,
            "prob_icu_to_death": 0.5
        }
        self.multipliers = {
            "gp_to_hosp": [0.25, 0.421052632],
            "gp_to_death": [0.25, 0.421052632],
            "exposed_to_infect": [0.75, 0.842105263],
            "hosp_to_death": [0.9, 1],
            "hosp_to_icu": [0.9, 1],
            "icu_to_death": [0.9, 1]
        }
        self.mock_inf_prog = np.array(
            [0.487464241, 1, 1.229764827, 1.312453175,
             1.307955665, 1.251658756, 1.166040358,
             1.065716869, 0.960199498, 0.855580145,
             0.755628835, 0.662534099, 0.577412896,
             0.500665739, 0.432225141, 0.371729322,
             0.318643018, 0.272340645, 0.232162632,
             0.19745264, 0.167581252, 0.141960133,
             0.120049578, 0.101361532, 0.085459603,
             0.071957123, 0.060514046, 0.050833195,
             0.04265624, 0.035759641, 0.029950735,
             0.025064045, 0.02095788, 0.017511251,
             0.014621091, 0.012199802, 0.010173075,
             0.008477992, 0.007061366, 0.005878301,
             0.00489096, 0.004067488, 0.003381102,
             0.00280931, 0.002333237, 0.001937064,
             0.001607543, 0.001333589, 0.001105933,
             0.00091683, 0.000759816, 0.000629496,
             0.000521372, 0.000431695, 0.000357344,
             0.000295719, 0.000244659])

        # Create population that will be used to test all
        #  methods except update status
        self.test_population1 = pe.Population()
        self.test_population1.add_cells(1)
        self.cell = self.test_population1.cells[0]
        self.test_population1.cells[0].add_microcells(1)
        self.test_population1.cells[0].microcells[0].add_people(3)
        self.test_population1.cells[0].microcells[0].add_place(1, [1, 1],
                                                               place_type=5)
        self.place1 = self.test_population1.cells[0].microcells[0].places[0]
        self.person1 = self.test_population1.cells[0].microcells[0].persons[0]
        self.person2 = self.test_population1.cells[0].microcells[0].persons[1]
        self.person3 = self.test_population1.cells[0].microcells[0].persons[2]

        # test update status method
        self.test_population2 = pe.Population()
        self.test_population2.add_cells(1)
        self.test_population2.cells[0].add_microcells(1)
        self.test_population2.cells[0].microcells[0]. \
            add_people(len(InfectionStatus))
        self.people = []
        for i in range(len(InfectionStatus)):
            person = self.test_population2.cells[0].microcells[0].persons[i]
            person.update_status(InfectionStatus(i + 1))
            self.people.append(person)

    def test_construct(self):
        """Tests that the host progression sweep initialises correctly.
        """
        pe.sweep.HostProgressionSweep()

    def test_set_infectiousness(self):
        """Tests that the set infectiousness function returns a positive
        float and the correct infection start time.
        """
        # Test with person1 as InfectASympt infection status and time an
        # integer.
        self.person1.update_status(InfectionStatus.InfectASympt)
        pe.sweep.HostProgressionSweep.set_infectiousness(self.person1, 0)
        self.assertIsInstance(self.person1.initial_infectiousness, float)
        self.assertTrue(0 <= self.person1.initial_infectiousness)
        self.assertEqual(self.person1.infection_start_time, 0)
        # Test with person1 as InfectMild infection status and time a non-zero
        # integer
        self.person1.update_status(InfectionStatus.InfectMild)
        pe.sweep.HostProgressionSweep.set_infectiousness(self.person1, 5)
        self.assertIsInstance(self.person1.initial_infectiousness, float)
        self.assertTrue(0 <= self.person1.initial_infectiousness)
        self.assertEqual(self.person1.infection_start_time, 5)
        # Test with person1 as InfectGP and time a float
        self.person1.update_status(InfectionStatus.InfectGP)
        pe.sweep.HostProgressionSweep.set_infectiousness(self.person1, 1.5)
        self.assertIsInstance(self.person1.initial_infectiousness, float)
        self.assertTrue(0 <= self.person1.initial_infectiousness)
        self.assertEqual(self.person1.infection_start_time, 1.5)

    def test_set_infectiousness_neg_time(self):
        """Tests that a value error is raised if the input time in 'set
        infectiousness' method is negative.
        """
        self.person1.update_status(InfectionStatus.InfectASympt)
        with self.assertRaises(ValueError):
            pe.sweep.HostProgressionSweep.set_infectiousness(self.person1, -2)

    @mock.patch('random.uniform')
    def test_carehome_residents_die(self, mock_rand):
        """Tests that carehome_residents die with probability=1 if they reach
        ICU, and with probability = 1 - carehome_rel_prob_hosp if they reach
        hospital
        """
        mock_rand.return_value = 2
        test_sweep = pe.sweep.HostProgressionSweep()

        self.person1.care_home_resident = 1
        self.person1.update_status(InfectionStatus.InfectICU)
        test_sweep.update_next_infection_status(self.person1, 1.0)
        self.assertEqual(self.person1.next_infection_status,
                         InfectionStatus.Dead)

        self.person2.care_home_resident = 1
        self.person2.infection_status = InfectionStatus.InfectHosp
        test_sweep.update_next_infection_status(self.person2, 1.0)
        self.assertEqual(self.person2.next_infection_status,
                         InfectionStatus.Dead)
        mock_rand.assert_called_once_with(0, 1)

    def test_update_next_infection_status(self):
        """Tests that an assertion error is raised if length of weights
        and outcomes are different. Tests that the update_next_infection_status
        method works with an identity state matrix as state_transition_matrix.
        Tests that the method works for each infection status with all people
        going to InfectICURecov infection status. Tests that method works for
        a random upper triangular state transition matrix. This only works
        with waning immunity turned off.
        """
        test_sweep = pe.sweep.HostProgressionSweep()

        test_sweep.state_transition_matrix['Test col'] = ""
        with self.assertRaises(AssertionError):
            test_sweep.update_next_infection_status(self.people[0], 1.0)

        identity_matrix = pd.DataFrame(np.identity(len(InfectionStatus)),
                                       columns=[status.name for
                                                status in InfectionStatus],
                                       index=[status.name for
                                              status in InfectionStatus])
        test_sweep.state_transition_matrix = identity_matrix
        for person in self.people:
            with self.subTest(person=person):
                test_sweep.update_next_infection_status(person, 1.0)
                if person.infection_status.name in ['Recovered', 'Dead',
                                                    'Vaccinated']:
                    self.assertEqual(person.next_infection_status, None)
                else:
                    self.assertEqual(person.infection_status,
                                     person.next_infection_status)

        matrix = np.zeros([len(InfectionStatus), len(InfectionStatus)])
        # Set ICU recovery infection status column values to 1. This way
        # everyone who is not recovered or dead will have their next
        # infection status set as ICURecov
        matrix[:, InfectionStatus.InfectICURecov.value - 1] = 1
        matrix = pd.DataFrame(matrix,
                              columns=[status.name for
                                       status in InfectionStatus],
                              index=[status.name for
                                     status in InfectionStatus])
        test_sweep.state_transition_matrix = matrix
        for person in self.people:
            with self.subTest(person=person):
                test_sweep.update_next_infection_status(person, 1.0)
                if person.infection_status.name in ['Recovered', 'Dead',
                                                    'Vaccinated']:
                    self.assertEqual(person.next_infection_status, None)
                else:
                    self.assertEqual(person.next_infection_status,
                                     InfectionStatus.InfectICURecov)

        random_matrix = np.random.rand(len(InfectionStatus),
                                       len(InfectionStatus))
        random_matrix = np.triu(random_matrix)
        random_matrix = pd.DataFrame(random_matrix,
                                     columns=[status.name for
                                              status in InfectionStatus],
                                     index=[status.name for
                                            status in InfectionStatus])
        test_sweep.state_transition_matrix = random_matrix
        for person in self.people:
            with self.subTest(person=person):
                test_sweep.update_next_infection_status(person, 1.0)
                if person.infection_status.name in ['Recovered', 'Dead',
                                                    'Vaccinated']:
                    self.assertEqual(person.next_infection_status, None)
                else:
                    current_enum_value = person.infection_status.value
                    next_enum_value = person.next_infection_status.value
                    self.assertTrue(current_enum_value <= next_enum_value)

    def test_update_next_infection_status_waning_immunity(self):
        """Tests that Recovered people return to Susceptible when their status
        is updated if waning immunity is turned on.
        """
        with mock.patch('pyEpiabm.Parameters.instance') as mock_param:
            mock_param.return_value.use_waning_immunity = 1.0
            mock_param.return_value.asympt_infect_period = 14
            mock_param.return_value.time_steps_per_day = 1
            mock_param.return_value.rate_multiplier_params = self.multipliers
            test_sweep = pe.sweep.HostProgressionSweep()
            self.person1.update_status(InfectionStatus.Recovered)
            test_sweep.update_next_infection_status(self.person1, 1.0)
            self.assertEqual(InfectionStatus.Susceptible,
                             self.person1.next_infection_status)

            # Assert that the _get_waning_weights function is called under
            # the correct conditions
            with mock.patch('pyEpiabm.sweep.HostProgressionSweep.'
                            '_get_waning_weights') as mock_func:
                self.person1.time_of_recovery = 30
                self.person1.infection_status = InfectionStatus.Exposed
                mock_func.return_value = [1] + [0]*10
                test_sweep.update_next_infection_status(self.person1, 1.0)
                mock_func.assert_called_once_with(self.person1, 1.0)

    def test__get_waning_weights(self):
        """Tests the _get_waning_weights() function to ensure that the correct
        weights are returned when waning immunity is turned on.
        """
        with mock.patch('pyEpiabm.Parameters.instance') as mock_param:
            mock_param.return_value.use_waning_immunity = 1.0
            mock_param.return_value.asympt_infect_period = 14
            mock_param.return_value.time_steps_per_day = 1
            mock_param.return_value.host_progression_lists = self.coefficients
            mock_param.return_value.rate_multiplier_params = self.multipliers
            test_sweep = pe.sweep.HostProgressionSweep()
            self.person1.infection_status = InfectionStatus.Exposed
            self.person1.time_of_recovery = 20
            current_time = 50
            weights = test_sweep._get_waning_weights(self.person1,
                                                     current_time)
            # We are using the RateMultiplier functions with t = 30, so the
            # expected weights have been calculated below
            a = self.coefficients["prob_exposed_to_asympt"]
            b = self.coefficients["prob_exposed_to_mild"]
            c = self.coefficients["prob_exposed_to_gp"]
            p_90, p_180 = self.multipliers["exposed_to_infect"]
            p = pe.utility.RateMultiplier(p_90, p_180)
            p_30 = p(30)
            expected_weights = [0, 0, a + (1 - p_30) * b + (1 - p_30) * c,
                                p_30 * b, p_30 * c, 0, 0, 0, 0, 0, 0]
            for i in range(len(weights)):
                self.assertAlmostEqual(expected_weights[i], weights[i])

    def test_update_time_status_change_no_age(self, current_time=100.0):
        """Tests that people who have their time to status change set correctly
        depending on their current infection status. This test is with waning
        immunity turned off.
        """
        test_sweep = pe.sweep.HostProgressionSweep()
        for i in range(len(InfectionStatus)):
            person = self.people[i]
            person.update_status(InfectionStatus(i + 1))
            person.next_infection_status = None

        for person in self.people:
            with self.subTest(person=person):
                if person.infection_status == InfectionStatus.Susceptible:
                    with self.assertRaises(ValueError):
                        test_sweep.update_next_infection_status(person,
                                                                current_time)
                        test_sweep.update_time_status_change(person,
                                                             current_time)
                    continue  # Method should not be used to infect people

                test_sweep.update_next_infection_status(person, current_time)
                test_sweep.update_time_status_change(person, current_time)
                time_of_status_change = person.time_of_status_change
                if person.infection_status.name in ['Recovered', 'Dead',
                                                    'Vaccinated']:
                    self.assertEqual(time_of_status_change, np.inf)
                elif person.infection_status.name in ['InfectMild',
                                                      'InfectGP']:
                    delayed_time = current_time + test_sweep.delay
                    self.assertLessEqual(delayed_time, time_of_status_change)
                else:
                    self.assertLessEqual(current_time, time_of_status_change)

    def test_update_time_status_change_waning_immunity(self):
        """Tests that the time to status change of a Recovered person with
        waning immunity is equal to the output of the InverseCDF method. This
        test should be changed if and when there is a different Recovery period
        """
        with mock.patch('pyEpiabm.Parameters.instance') as mock_param:
            mock_param.return_value.use_waning_immunity = 1.0
            mock_param.return_value.asympt_infect_period = 14
            mock_param.return_value.time_steps_per_day = 1
            mock_param.return_value.rate_multiplier_params = self.multipliers
            test_sweep = pe.sweep.HostProgressionSweep()
            self.person1.update_status(InfectionStatus.Recovered)
            self.person1.next_infection_status = InfectionStatus.Susceptible
            current_time = 1.0
            test_sweep.update_time_status_change(self.person1, current_time)
            self.assertEqual(2.0, self.person1.time_of_status_change)

    def test_neg_trans_raise(self):
        """Tests exception is raised with negative transition delta,
        originating from default value in array that has not been set.
        """
        test_sweep = pe.sweep.HostProgressionSweep()
        person = self.people[1]
        test_sweep.update_next_infection_status(person, 1.0)

        test_sweep.transition_time_matrix = \
            pe.sweep.TransitionTimeMatrix().matrix
        with self.assertRaises(ValueError):
            test_sweep.update_time_status_change(person, 1.0)

    def test_icdf_exception_raise(self):
        """Tests exception is raised with incorrect icdf or value in time
        transition matrix.
        """
        test_sweep = pe.sweep.HostProgressionSweep()
        person = self.people[1]
        test_sweep.update_next_infection_status(person, 1.0)
        row_index = person.infection_status.name
        column_index = person.next_infection_status.name

        zero_trans_mat = np.zeros((len(InfectionStatus), len(InfectionStatus)))
        labels = [status.name for status in InfectionStatus]
        init_matrix = pd.DataFrame(zero_trans_mat,
                                   columns=labels,
                                   index=labels,
                                   dtype=object)
        test_sweep.transition_time_matrix = init_matrix
        test_sweep.transition_time_matrix. \
            loc[row_index, column_index] = mock.Mock()
        test_sweep.transition_time_matrix.loc[row_index, column_index]. \
            icdf_choose_noexp.side_effect = AttributeError
        with self.assertRaises(AttributeError):
            test_sweep.update_time_status_change(person, 1.0)
        test_sweep.transition_time_matrix.loc[row_index, column_index]. \
            icdf_choose_noexp.assert_called_once()

    def test_infectiousness_progression(self):
        """Tests that the output is a numpy ndarray and that the tail of the
        array is 0, starting at the first element after the last infectious
        time step, when the number of time steps per day is 1 and the
        infectious period is 14 days.
        """
        with mock.patch('pyEpiabm.Parameters.instance') as mock_param:
            mock_param.return_value.time_steps_per_day = 1
            mock_param.return_value.asympt_infect_period = 14
            mock_param.return_value.infectiousness_prof = self.mock_inf_prog
            mock_param.return_value.rate_multiplier_params = self.multipliers
            # Parameters to determine where the tail starts, has to be the same
            # as for the parameters called in HostProgressionSweep.
            infectious_period = pe.Parameters.instance().asympt_infect_period
            model_time_step = 1 / pe.Parameters.instance().time_steps_per_day
            num_infectious_ts = int(np.ceil(infectious_period /
                                            model_time_step))
            # Initialisation
            test_sweep = pe.sweep.HostProgressionSweep()
            infect_prog = test_sweep.infectiousness_progression
            # Checks output type is numpy array
            self.assertIsInstance(infect_prog, np.ndarray)
            # Checks elements are 0 after k and greater than 0 before
            tail = infect_prog[num_infectious_ts:2550]
            zeros = np.zeros(2550 - num_infectious_ts)
            self.assertTrue((tail == zeros).all())
            self.assertTrue((infect_prog[0:num_infectious_ts] >
                             np.zeros(num_infectious_ts)).all())

    def test_infectiousness_progression_small_time_steps(self):
        """Tests that the method workd when there are more than 1 time step
        per day. Also tests that a value error is raised if the model time
        steps length is too small (ie the number of time steps per day is
        too big).
        """
        with mock.patch('pyEpiabm.Parameters.instance') as mock_param:
            # Same test as test_infectiousness_progression, but with 100 time
            # steps per day:
            mock_param.return_value.time_steps_per_day = 100
            mock_param.return_value.asympt_infect_period = 14
            mock_param.return_value.rate_multiplier_params = self.multipliers
            mock_param.return_value.infectiousness_prof = self.mock_inf_prog
            infectious_period = pe.Parameters.instance().asympt_infect_period
            model_time_step = 1 / pe.Parameters.instance().time_steps_per_day
            num_infectious_ts = int(np.ceil(infectious_period /
                                            model_time_step))
            test_sweep = pe.sweep.HostProgressionSweep()
            infect_prog = test_sweep.infectiousness_progression
            # Checks output type is numpy array
            self.assertIsInstance(infect_prog, np.ndarray)
            # Checks elements are 0 after num_infectious_ts and greater than 0
            # before
            tail = infect_prog[num_infectious_ts:2550]
            zeros = np.zeros(2550 - num_infectious_ts)
            self.assertTrue((tail == zeros).all())
            self.assertTrue((infect_prog[0:num_infectious_ts] >
                             np.zeros(num_infectious_ts)).all())

            # Very small value for time steps to raise error:
            mock_param.return_value.time_steps_per_day = 10000
            with self.assertRaises(ValueError):
                pe.sweep.HostProgressionSweep()

    def test_limit_case_infectiousness_progression(self):
        """Tests the case in the infectiousness progression method where the
        parameter associated infectiousness value would be greater or equal to
        the infectiousness profile resolution. In that case, the elements of
        the array infectiousness progression are simply set to 0.
        """
        with mock.patch('numpy.floor') as mock_floor:
            with mock.patch('pyEpiabm.Parameters.instance') as mock_param:
                mock_param.return_value.time_steps_per_day = 1
                mock_param.return_value.asympt_infect_period = 14
                mock_param.return_value.infectiousness_prof = \
                    self.mock_inf_prog
                mock_param.return_value.rate_multiplier_params = \
                    self.multipliers
                num_infectious_ts = int(np.ceil(pe.Parameters.instance().
                                                asympt_infect_period
                                                * pe.Parameters.instance().
                                                time_steps_per_day))
                # We need to mock the np.floor function to have j greater or
                # equal to the infectiousness profile resolution
                mock_floor.return_value = 57
                test_sweep = pe.sweep.HostProgressionSweep()
                infect_prog = test_sweep.infectiousness_progression
                # Checks that the output is a numpy array
                self.assertIsInstance(infect_prog, np.ndarray)
                # Checks that all elements are equal to 0
                zeros = np.zeros(2550)
                self.assertTrue((infect_prog == zeros).all())
                # Checks that it is called the right number of times (the right
                # number of times is the number of infectious time steps plus
                # one because it is used in the delay calculation)
                self.assertEqual(mock_floor.call_count, num_infectious_ts + 1)

    def test_update_infectiousness(self):
        """Tests the update infectiousness method. Checks that a person with
        a Susceptible, Exposed, Recovered or Dead infection status still has
        an infectiousness of 0. Checks that a person with an infected status
        gets its infectiousness updated, with a float value.
        """
        test_sweep = pe.sweep.HostProgressionSweep()
        # We set an initial infectiousness for everyone of 1.1
        for i in range(len(InfectionStatus)):
            person = self.people[i]
            person.update_status(InfectionStatus(i + 1))
            person.next_infection_status = None
            person.initial_infectiousness = 1.1
            person.infection_start_time = 0
        # Updates infectiousness after one day
        for person in self.people:
            test_sweep._updates_infectiousness(person, 1)
        # Assert that non infectious people have infectiousness of 0
        for i in [0, 1, 8, 9]:
            with self.subTest(i=i):
                self.assertEqual(self.people[i].infectiousness, 0)
        # Assert that infected people have positive float infectiousness
        for infected_person in self.people[2:8]:
            with self.subTest(infected_person=infected_person):
                self.assertGreater(infected_person.infectiousness, 0)
                self.assertIsInstance(infected_person.infectiousness, float)

    def test_invalid_update_infectiousness(self):
        test_sweep = pe.sweep.HostProgressionSweep()
        self.person1.infectiousness = 1
        self.person1.infection_start_time = 0
        self.person1.update_status(InfectionStatus.Dead)

        self.assertEqual(self.person1.infection_start_time, 0)
        self.assertEqual(self.person1.infectiousness, 1)
        test_sweep._updates_infectiousness(self.person1, 1)
        self.assertEqual(self.person1.infectiousness, 0)
        self.assertIsNone(self.person1.infection_start_time)

    def test_compare_value_update_infectiousness(self):
        """Tests that a person's infectiousness is correctly updated by
        comparing the infectiousness of a person at the same simulation
        time in simulations with two different time steps lengths.
        """
        with mock.patch('pyEpiabm.Parameters.instance') as mock_param:
            # Parameters used in update infectiousness for both time steps
            # length:
            mock_param.return_value.asympt_infect_period = 14
            mock_param.return_value.infectiousness_prof = self.mock_inf_prog
            mock_param.return_value.rate_multiplier_params = self.multipliers
            infectious_period = pe.Parameters.instance().asympt_infect_period

            # Generating the list of infectiousness values for when we have 1
            # time step per day
            mock_param.return_value.time_steps_per_day = 1
            model_time_step = 1 / pe.Parameters.instance().time_steps_per_day
            num_infectious_ts = int(np.ceil(infectious_period /
                                            model_time_step))
            test_sweep_ts1 = pe.sweep.HostProgressionSweep()
            # We generate an array containing the times of the simulation
            time_steps_1 = np.zeros(num_infectious_ts)
            time_steps_1[0] = model_time_step
            for i in range(num_infectious_ts):
                time_steps_1[i] = time_steps_1[i - 1] + model_time_step

            # Generating the list of infectiousness values for when we have 2
            # time steps per day
            mock_param.return_value.time_steps_per_day = 2
            model_time_step = 1 / pe.Parameters.instance().time_steps_per_day
            num_infectious_ts = int(np.ceil(infectious_period /
                                            model_time_step))
            test_sweep_ts2 = pe.sweep.HostProgressionSweep()
            # We generate an array containing the times of the simulation
            time_steps_2 = np.zeros(num_infectious_ts)
            time_steps_2[0] = model_time_step
            for i in range(num_infectious_ts):
                time_steps_2[i] = time_steps_2[i - 1] + model_time_step

            # We set an asymptotically infected person with infectiousness 1
            # for each time simulation time step length
            person_1, person_2 = self.people[1:3]
            for person in [person_1, person_2]:
                person.update_status(InfectionStatus(3))
                person.initial_infectiousness = 1
                person.infection_start_time = 0
            # We generate a list containing the infectiousness values of the
            # person for each simulation time step length
            person_infectiousness_ts1 = list()
            person_infectiousness_ts2 = list()
            for t in time_steps_1:
                test_sweep_ts1._updates_infectiousness(person_1, t)
                person_infectiousness_ts1.append(person_1.infectiousness)
            for t in time_steps_2:
                test_sweep_ts2._updates_infectiousness(person_2, t)
                person_infectiousness_ts2.append(person_2.infectiousness)

            # We truncate this list to only keep infectiousness values on
            # whole days to compare with case where we have 1 time step per day
            person_infectiousness_ts2 = person_infectiousness_ts2[1::2]
            # Now we compare both arrays to confirm that any difference is
            # smaller than 1e-4
            np.testing.assert_almost_equal(person_infectiousness_ts1,
                                           person_infectiousness_ts2, 4)

    @mock.patch('pyEpiabm.sweep.HostProgressionSweep.sympt_testing_queue')
    @mock.patch(
        'pyEpiabm.sweep.HostProgressionSweep.asympt_uninf_testing_queue')
    @mock.patch('pyEpiabm.Parameters.instance')
    @mock.patch('pyEpiabm.utility.InverseCdf.icdf_choose_noexp')
    def test_call_main(self, mock_next_time, mock_param,
                       mock_asympt, mock_sympt):
        """Tests the main function of the Host Progression Sweep.
        Person 1 is set to susceptible and becoming exposed. Person 2 is set to
        exposed and becoming infectious in one time step. Checks the
        population updates as expected. Check that Person 3 stays as
        susceptible.
        """
        mock_next_time.return_value = 1.0
        mock_param.return_value.host_progression_lists = self.coefficients
        mock_param.return_value.rate_multiplier_params = self.multipliers
        mock_param.return_value.latent_to_sympt_delay = 1
        mock_param.return_value.time_steps_per_day = 1
        mock_param.return_value.model_time_step = 1
        mock_param.return_value.asympt_infect_period = 14
        mock_param.return_value.sympt_infectiousness = 1.5
        mock_param.return_value.infectiousness_prof = self.mock_inf_prog
        # First check that people progress through the
        # infection stages correctly.
        self.person2.update_status(pe.property.InfectionStatus.Exposed)
        self.person2.time_of_status_change = 1.0
        self.person2.next_infection_status = \
            pe.property.InfectionStatus.InfectMild
        self.person1.update_status(pe.property.InfectionStatus.Susceptible)
        self.person1.time_of_status_change = 1.0
        self.person1.next_infection_status = \
            pe.property.InfectionStatus.Exposed
        test_sweep = pe.sweep.HostProgressionSweep()
        test_sweep.bind_population(self.test_population1)

        # Tests population bound successfully.
        self.assertEqual(test_sweep._population.cells[0].persons[1].
                         infection_status, pe.property.InfectionStatus.Exposed)
        test_sweep(1.0)
        self.assertEqual(self.person2.infection_status,
                         pe.property.InfectionStatus.InfectMild)
        self.assertEqual(self.person1.infection_status,
                         pe.property.InfectionStatus.Exposed)
        self.assertEqual(self.person3.infection_status,
                         pe.property.InfectionStatus.Susceptible)
        # Checks infectiousness update and infection start time
        self.assertEqual(self.person3.infectiousness, 0)
        self.assertEqual(self.person3.infection_start_time, None)
        self.assertEqual(self.person1.infectiousness, 0)
        self.assertEqual(self.person1.infection_start_time, None)
        self.assertGreater(self.person2.infectiousness, 0)
        self.assertIsInstance(self.person2.infection_start_time, float)
        # Checks time of status change
        self.assertIsInstance(self.person2.time_of_status_change, float)
        self.assertIsInstance(self.person1.time_of_status_change, float)
        self.assertTrue(2.0 <= self.person2.time_of_status_change <= 11.0)
        self.assertTrue(0.0 <= self.person1.time_of_status_change)
        self.assertEqual(mock_next_time.call_count, 2)

        mock_asympt.assert_called_once_with([(self.cell, self.person3)], 1.0)
        self.assertEqual(mock_sympt.call_count, 2)

    def test_call_specific(self):
        """Tests the specific cases in the call method such as people
        with None as their time to next infection status are the correct
        infection status and that people who have been set as recovered
        are dealt with correctly.
        """
        # Check assertion error for infection status when None is set
        # as time to status change.

        # First reconfigure population and sweep.
        self.person1.time_of_status_change = None
        self.person1.update_status(InfectionStatus.Susceptible)
        self.person2.time_of_status_change = None
        self.person2.update_status(InfectionStatus.Exposed)
        self.person3.time_of_status_change = None
        self.person3.update_status(InfectionStatus.Susceptible)
        test_sweep = pe.sweep.HostProgressionSweep()
        test_sweep.bind_population(self.test_population1)

        # Run sweep and check assertion error is raised for Person 1.
        with self.assertRaises(AssertionError):
            test_sweep(1.0)

        # Reconfigure population and check that Person 1 has the correct
        # properties on being set as recovered.
        self.person1.time_of_status_change = 1.0
        self.person1.update_status(InfectionStatus.InfectMild)
        self.person1.next_infection_status = InfectionStatus.Recovered
        self.person2.update_status(InfectionStatus.Susceptible)
        test_sweep(1.0)
        self.assertEqual(self.person1.infection_status,
                         InfectionStatus.Recovered)
        self.assertEqual(self.person1.next_infection_status, None)
        self.assertEqual(self.person1.time_of_status_change, np.inf)
        self.assertEqual(self.person1.infectiousness, 0)
        self.assertEqual(self.person1.infection_start_time, None)

    def test_call_waning_immunity(self):
        """Tests that a Recovered person will progress to Susceptible at the
        correct time if waning immunity is turned on. Also tests that the
        person exits the method with time_of_next_status_change being None
        """
        with mock.patch('pyEpiabm.Parameters.instance') as mock_param:
            mock_param.return_value.use_waning_immunity = 1.0
            mock_param.return_value.asympt_infect_period = 14
            mock_param.return_value.time_steps_per_day = 1
            mock_param.return_value.rate_multiplier_params = self.multipliers
            test_sweep = pe.sweep.HostProgressionSweep()
            test_sweep.bind_population(self.test_population1)
            self.person1.update_status(InfectionStatus.Recovered)
            self.person1.next_infection_status = InfectionStatus.Susceptible
            self.person2.update_status(InfectionStatus.InfectMild)
            self.person2.next_infection_status = InfectionStatus.Recovered
            current_time = 1.0
            test_sweep.update_time_status_change(self.person1, current_time)
            time_of_change = self.person1.time_of_status_change
            self.person2.time_of_status_change = time_of_change
            test_sweep(time_of_change)
            self.assertEqual(self.person1.infection_status,
                             InfectionStatus.Susceptible)
            self.assertEqual(self.person1.time_of_status_change, None)
            self.assertEqual(self.person2.infection_status,
                             InfectionStatus.Recovered)
            self.assertEqual(self.person2.time_of_recovery, time_of_change)

    @mock.patch(
        'pyEpiabm.sweep.HostProgressionSweep.asympt_uninf_testing_queue')
    def test_asymptomatic_list(self, mock_asympt):
        self.person1.time_of_status_change = None
        self.person1.update_status(InfectionStatus.Susceptible)
        self.person2.time_of_status_change = np.inf
        self.person2.update_status(InfectionStatus.Recovered)
        self.person3.time_of_status_change = 1.0
        self.person3.update_status(InfectionStatus.Exposed)
        self.person3.next_infection_status = InfectionStatus.InfectASympt

        test_sweep = pe.sweep.HostProgressionSweep()
        test_sweep.bind_population(self.test_population1)
        test_sweep(1.0)

        mock_asympt.assert_called_with([(self.cell, self.person1),
                                        (self.cell, self.person2),
                                        (self.cell, self.person3)], 1.0)

    @mock.patch('pyEpiabm.utility.InverseCdf.icdf_choose_noexp')
    @mock.patch('pyEpiabm.Parameters.instance')
    def test_multiple_transitions_in_one_time_step(self, mock_param,
                                                   mock_next_time):
        """Reconfigure population and check that a person is able to progress
        infection status multiple times in the same time step. This will be
        checked by setting the time transition time to 0 so Person 1 should
        progress from susceptible through the whole infection timeline ending
        up as either recovered or dead in one time step. This is only the case
        when we do not have waning immunity.
        """
        mock_param.return_value.use_waning_immunity = 0
        mock_param.return_value.time_steps_per_day = 1
        mock_param.return_value.asympt_infect_period = 14
        mock_param.return_value.latent_to_sympt_delay = 0.5
        mock_param.return_value.host_progression_lists = self.coefficients
        mock_param.return_value.rate_multiplier_params = self.multipliers
        mock_next_time.return_value = 0.0
        self.person1.time_of_status_change = 1.0
        self.person1.update_status(InfectionStatus.Susceptible)
        self.person1.next_infection_status = InfectionStatus.Exposed
        test_sweep = pe.sweep.HostProgressionSweep()
        test_sweep.bind_population(self.test_population1)
        test_sweep(1.0)
        self.assertIn(self.person1.infection_status,
                      [InfectionStatus.Recovered,
                       InfectionStatus.Dead])

    @mock.patch('random.random')
    def test_sympt_queue(self, mock_random):
        mock_random.return_value = 0
        test_sweep = pe.sweep.HostProgressionSweep()
        test_sweep.bind_population(self.test_population1)

        self.person1.update_status(InfectionStatus.InfectMild)
        self.person2.update_status(InfectionStatus.InfectMild)
        self.person3.update_status(InfectionStatus.InfectMild)
        self.person1.date_positive = None
        self.person2.date_positive = None
        self.person3.date_positive = None

        self.person1.care_home_resident = True
        self.person2.key_worker = True

        test_sweep.sympt_testing_queue(self.cell, self.person1)
        test_sweep.sympt_testing_queue(self.cell, self.person2)
        test_sweep.sympt_testing_queue(self.cell, self.person3)

        self.assertEqual(self.cell.PCR_queue.qsize(), 3)
        self.assertEqual(self.cell.LFT_queue.qsize(), 0)

        self.person1.date_positive = 1
        self.person1.next_infection_status = InfectionStatus.Recovered

        test_sweep.sympt_testing_queue(self.cell, self.person1)

        self.assertIsNone(self.person1.date_positive)

        self.assertEqual(mock_random.call_count, 8)

    @mock.patch('random.random')
    def test_LFT_queue(self, mock_random):
        mock_random.return_value = 0
        test_sweep = pe.sweep.HostProgressionSweep()

        self.person2.update_status(InfectionStatus.InfectMild)
        self.person2.date_positive = None

        with mock.patch('pyEpiabm.Parameters.instance') as mock_param:
            mock_param.return_value. \
                intervention_params = {'disease_testing':
                                       {'sympt_pcr': [-1, -1, -1],
                                        'testing_sympt': [0.5, 0.5, 0.5]}}

            test_sweep.sympt_testing_queue(self.cell, self.person2)
            self.assertEqual(self.cell.LFT_queue.qsize(), 1)

        self.person1.update_status(InfectionStatus.InfectASympt)
        self.person1.date_positive = None

        person_list = [(self.cell, self.person1)]

        with mock.patch('pyEpiabm.Parameters.instance') as mock_param:
            mock_param.return_value. \
                intervention_params = {'disease_testing':
                                       {'asympt_uninf_pcr':
                                        [-1, -1, -1],
                                        'testing_asympt_uninf':
                                        [0.5, 0.5, 0.5]}}

            test_sweep.asympt_uninf_testing_queue(person_list, 1)
            self.assertEqual(self.cell.LFT_queue.qsize(), 2)

        self.assertEqual(mock_random.call_count, 4)

    @mock.patch('random.random')
    def test_asympt_queue(self, mock_random):
        mock_random.return_value = 0
        test_sweep = pe.sweep.HostProgressionSweep()
        test_sweep.bind_population(self.test_population1)

        self.person1.update_status(InfectionStatus.InfectASympt)
        self.person2.update_status(InfectionStatus.InfectASympt)
        self.person3.update_status(InfectionStatus.InfectASympt)

        self.person1.date_positive = None
        self.person2.date_positive = None
        self.person3.date_positive = None

        self.person1.care_home_resident = True
        self.person2.key_worker = True

        person_list = [(self.cell, self.person1), (self.cell, self.person2),
                       (self.cell, self.person3)]

        test_sweep.asympt_uninf_testing_queue(person_list, 1.0)

        self.assertEqual(self.cell.PCR_queue.qsize(), 3)
        self.assertEqual(self.cell.LFT_queue.qsize(), 0)

        self.person3.date_positive = 0
        person_list_2 = [(self.cell, self.person3)]

        test_sweep.asympt_uninf_testing_queue(person_list_2, 10.0)
        self.assertIsNone(self.person3.date_positive)

        self.person1.update_status(InfectionStatus.InfectMild)
        person_list_3 = [(self.cell, self.person1)]
        self.assertRaises(ValueError, test_sweep.asympt_uninf_testing_queue,
                          person_list_3, 1.0)

        self.assertEqual(mock_random.call_count, 8)


if __name__ == "__main__":
    unittest.main()
