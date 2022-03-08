import unittest
from unittest import mock
import numpy as np
import pandas as pd

import pyEpiabm as pe
from pyEpiabm.property.infection_status import InfectionStatus


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
        float.
        """
        # Test with person1 as InfectASympt infection status
        self.person1.update_status(InfectionStatus.InfectASympt)
        test_sweep = pe.sweep.HostProgressionSweep()
        test_sweep._set_infectiousness(self.person1)
        self.assertIsInstance(self.person1.infectiousness, float)
        self.assertTrue(0 <= self.person1.infectiousness)
        # Test with person1 as InfectMild infection status
        self.person1.update_status(InfectionStatus.InfectMild)
        test_sweep._set_infectiousness(self.person1)
        self.assertIsInstance(self.person1.infectiousness, float)
        self.assertTrue(0 <= self.person1.infectiousness)
        # Test with person1 as InfectGP
        self.person1.update_status(InfectionStatus.InfectGP)
        test_sweep._set_infectiousness(self.person1)
        self.assertIsInstance(self.person1.infectiousness, float)
        self.assertTrue(0 <= self.person1.infectiousness)

    def test_update_next_infection_status(self):
        """Tests that an assertion error is raised if length of weights
        and outcomes are different. Tests that the update_next_infection_status
        method works with an identity state matrix as state_transition_matrix.
        Tests that the method works for each infection status with all people
        going to InfectICURecov infection status. Tests that method works for
        a random upper triangular state transition matrix.
        """
        test_sweep = pe.sweep.HostProgressionSweep()

        test_sweep.state_transition_matrix = \
            pe.Parameters.instance().state_transition_matrix.copy()
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
        self.state_transition_matrix = \
            pe.Parameters.instance().state_transition_matrix
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
        test_sweep.state_transition_matrix = \
            pe.Parameters.instance().state_transition_matrix

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
