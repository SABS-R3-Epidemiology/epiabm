import unittest
from unittest import mock
import numpy as np
import pandas as pd

import pyEpiabm as pe
from pyEpiabm.property import InfectionStatus


class TestHostProgressionSweep(unittest.TestCase):
    """Tests the 'HostProgressionSweep' class.
    """
    def setUp(self) -> None:
        """Sets up two populations we can use throughout the test.
        3 people are located in one microcell.
        """
        # Create population that will be used to test all
        #  methods except update status
        self.test_population1 = pe.Population()
        self.test_population1.add_cells(1)
        self.test_population1.cells[0].add_microcells(1)
        self.test_population1.cells[0].microcells[0].add_people(3)
        self.person1 = self.test_population1.cells[0].microcells[0].persons[0]
        self.person2 = self.test_population1.cells[0].microcells[0].persons[1]
        self.person3 = self.test_population1.cells[0].microcells[0].persons[2]

        # Create a population with people of all infection statuses to
        # test update status method
        self.test_population2 = pe.Population()
        self.test_population2.add_cells(1)
        self.test_population2.cells[0].add_microcells(1)
        self.test_population2.cells[0].microcells[0].\
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
        # integer
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
        """Tests that an assertion error is raised if the input time in 'set
        infectiousness' method is negative.
        """
        self.person1.update_status(InfectionStatus.InfectASympt)
        with self.assertRaises(AssertionError):
            pe.sweep.HostProgressionSweep.set_infectiousness(self.person1, -2)

    def test_update_next_infection_status(self):
        """Tests that an assertion error is raised if length of weights
        and outcomes are different. Tests that the update_next_infection_status
        method works with an identity state matrix as state_transition_matrix.
        Tests that the method works for each infection status with all people
        going to InfectICURecov infection status. Tests that method works for
        a random upper triangular state transition matrix.
        """
        test_sweep = pe.sweep.HostProgressionSweep()

        test_sweep.state_transition_matrix['Test col'] = ""
        with self.assertRaises(AssertionError):
            test_sweep._update_next_infection_status(self.people[0])

        identity_matrix = pd.DataFrame(np.identity(len(InfectionStatus)),
                                       columns=[status.name for
                                       status in InfectionStatus],
                                       index=[status.name for
                                       status in InfectionStatus])
        test_sweep.state_transition_matrix = identity_matrix
        for person in self.people:
            test_sweep._update_next_infection_status(person)
            if person.infection_status.name in ['Recovered', 'Dead']:
                self.assertEqual(person.next_infection_status, None)
            else:
                self.assertEqual(person.infection_status,
                                 person.next_infection_status)

        matrix = np.zeros([len(InfectionStatus), len(InfectionStatus)])
        # Set ICU recovery infection status column values to 1. This way
        # everyone who is not recovered or dead wiil have their next
        # infection status set as ICURecov
        matrix[:, -3] = 1
        matrix = pd.DataFrame(matrix,
                              columns=[status.name for
                                       status in InfectionStatus],
                              index=[status.name for
                                     status in InfectionStatus])
        test_sweep.state_transition_matrix = matrix
        for person in self.people:
            test_sweep._update_next_infection_status(person)
            if person.infection_status.name in ['Recovered', 'Dead']:
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
            test_sweep._update_next_infection_status(person)
            if person.infection_status.name in ['Recovered', 'Dead']:
                self.assertEqual(person.next_infection_status, None)
            else:
                current_enum_value = person.infection_status.value
                next_enum_value = person.next_infection_status.value
                self.assertTrue(current_enum_value <= next_enum_value)

    def test_update_time_status_change(self, current_time=100.0):
        """Tests that people who have their time to status change set correctly
        depending on their current infection status.
        """
        test_sweep = pe.sweep.HostProgressionSweep()
        for i in range(len(InfectionStatus)):
            person = self.people[i]
            person.update_status(InfectionStatus(i + 1))
            person.next_infection_status = None

        for person in self.people:
            test_sweep._update_next_infection_status(person)
            test_sweep._update_time_status_change(person, current_time)
            if person.infection_status.name in ['Recovered', 'Dead']:
                self.assertEqual(person.time_of_status_change, np.inf)
            elif person.infection_status.name in ['InfectMild', 'InfectGP']:
                delayed_time = current_time + test_sweep.delay
                self.assertTrue(delayed_time <= person.time_of_status_change)
            else:
                self.assertTrue(current_time <= person.time_of_status_change)

    def test_icdf_exception_raise(self):
        """Tests exception is raised with incorrect icdf or value in time
        transition matrix.
        """
        class BadICDF:
            def icdf_choose_noexp(self):
                raise AttributeError('test')

        test_sweep = pe.sweep.HostProgressionSweep()
        person = self.people[0]
        test_sweep._update_next_infection_status(self.people[0])
        row_index = person.infection_status.name
        column_index = person.next_infection_status.name
        test_sweep.transition_time_matrix.loc[row_index, column_index] \
            = BadICDF()
        with self.assertRaises(AttributeError):
            test_sweep._update_time_status_change(self.people[0], 1.0)

    def test_infectiousness_progression(self):
        """Tests that the output is a numpy ndarray and that the tail of the
        array is 0, starting at the element k.
        """
        # Parameters to determine where the tail starts
        infectious_period = pe.Parameters.instance().asympt_infect_period
        model_time_step = 1 / pe.Parameters.instance().time_steps_per_day
        k = int(np.ceil(infectious_period / model_time_step))
        # Initialisation
        test_sweep = pe.sweep.HostProgressionSweep()
        infect_prog = test_sweep._infectiousness_progression()
        # Checks output type is numpy array
        self.assertIsInstance(infect_prog, np.ndarray)
        # Checks elements are 0 after k
        tail = infect_prog[k:2550]
        zeros = np.zeros(2550-k)
        self.assertTrue((tail == zeros).all())

    def test_infectiousness_progression_small_time_steps(self):
        """Tests that an assertion error is raised if the model time steps
        length is too small (ie the time steps per day is too big).
        """
        # Stocks the real time steps per day value
        real = pe.Parameters.instance().time_steps_per_day

        # Assigns temporarily a new value for time steps per day to raise error
        pe.Parameters.instance().time_steps_per_day = 10000
        with self.assertRaises(ValueError):
            test_sweep = pe.sweep.HostProgressionSweep()
            test_sweep._infectiousness_progression()

        # Resets the value of time steps per day
        pe.Parameters.instance().time_steps_per_day = real

    def test_limit_case_infectiousness_progression(self):
        """Tests the case in the infectiousness progression method where the
        parameter j would be greater or equal to the infectiousness profile
        resolution. In that case, the elements of the array infectiousness
        progression are simply set to 0.
        """
        test_sweep = pe.sweep.HostProgressionSweep()

        with mock.patch('numpy.floor') as mock_floor:
            # We need to mock the np.floor function to have j greater or equal
            # to the infectiousness profile resolution
            mock_floor.return_value = 57
            infect_prog = test_sweep._infectiousness_progression()
            # Checks that the output is a numpy array
            self.assertIsInstance(infect_prog, np.ndarray)
            # Checks that all elements are equal to 0
            zeros = np.zeros(2550)
            self.assertTrue((infect_prog == zeros).all())

    def test_updates_infectiousness(self):
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
        self.assertEqual(self.people[0].infectiousness, 0)
        self.assertEqual(self.people[1].infectiousness, 0)
        self.assertEqual(self.people[8].infectiousness, 0)
        self.assertEqual(self.people[9].infectiousness, 0)
        # Assert that infected people have positive float infectiousness
        for infected_person in self.people[2:8]:
            self.assertGreater(infected_person.infectiousness, 0)
            self.assertIsInstance(infected_person.infectiousness, float)

    @mock.patch('pyEpiabm.utility.InverseCdf.icdf_choose_noexp')
    def test_call_main(self, mock_next_time):
        """Tests the main function of the Host Progression Sweep.
        Person 1 is set to susceptible and becoming exposed. Person 2 is set to
        exposed and becoming infectious in one time step. Checks the
        population updates as expected. Check that Person 3 stays as
        susceptible.
        """
        mock_next_time.return_value = 1.0
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

    @mock.patch('pyEpiabm.utility.InverseCdf.icdf_choose_noexp')
    def test_multiple_transitions_in_one_time_step(self, mock_next_time):
        """Reconfigure population and check that a person is able to progress
        infection status multiple times in the same time step. This will be
        checked by setting the time transition time as 0 so Person 1 should
        progress from susceptible through the whole infection timeline ending
        up as either recovered or dead in one time step.
        """

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


if __name__ == "__main__":
    unittest.main()
