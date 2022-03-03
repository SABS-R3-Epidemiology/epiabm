import unittest
from unittest import mock
import numpy as np
import pandas as pd

import pyEpiabm as pe
from pyEpiabm.property.infection_status import InfectionStatus


class TestHostProgressionSweep(unittest.TestCase):
    """Tests the 'HostProgressionSweep' class.
    """
    @classmethod
    def setUpClass(cls) -> None:
        """Sets up a population we can use throughout the test.
        2 people are located in one microcell.
        """

        # Create population that will be used to test all
        #  methods except update status
        cls.test_population1 = pe.Population()
        cls.test_population1.add_cells(1)
        cls.test_population1.cells[0].add_microcells(1)
        cls.test_population1.cells[0].microcells[0].add_people(3)
        cls.person1 = cls.test_population1.cells[0].microcells[0].persons[0]
        cls.person2 = cls.test_population1.cells[0].microcells[0].persons[1]
        cls.person3 = cls.test_population1.cells[0].microcells[0].persons[2]

        # Create a population with people of all infection statuses to
        # test update status method
        cls.test_population2 = pe.Population()
        cls.test_population2.add_cells(1)
        cls.test_population2.cells[0].add_microcells(1)
        cls.test_population2.cells[0].microcells[0].add_people(len(InfectionStatus))
        cls.people = []
        for i in range(len(InfectionStatus)):
            person = cls.test_population2.cells[0].microcells[0].persons[i]
            person.update_status(InfectionStatus(i + 1))
            cls.people.append(person)


    def test_construct(self):
        """Tests that the host progression sweep initialises correctly.
        """
        pe.sweep.HostProgressionSweep()

    def test_set_latent_time(self):
        """Tests that set latent time returns a float greater than
        or equal to 0.0.
        """
        current_time = 5.0
        test_sweep = pe.sweep.HostProgressionSweep()
        test_sweep._set_latent_time(self.person1, current_time)
        self.assertIsInstance(self.person1.time_of_status_change, float)
        self.assertTrue(5.0 <= self.person1.time_of_status_change)

    @mock.patch('pyEpiabm.utility.InverseCdf.icdf_choose_exp')
    def test_neg_latent_time(self, mock_choose):
        """Tests that an Assertion Error is raised if the set latent time
        is negative.
        """
        current_time = 0.0
        mock_choose.return_value = -1
        with self.assertRaises(AssertionError):
            test_sweep = pe.sweep.HostProgressionSweep()
            test_sweep._set_latent_time(self.person1, current_time)

       
    def test_set_infectiousness(self):
         """Tests that the set infectiousness function returns a positive
         float.
         """
         test_sweep = pe.sweep.HostProgressionSweep()
         infectiousness = test_sweep._set_infectiousness(self.person1)
         self.assertIsInstance(infectiousness, float)
         self.assertTrue(0 <= infectiousness)
      
    def test_update_time(self):
        """Tests the update time function on the test population. This generates
        a random float (uniformly) between 1.0 and 10.0.
        """
        current_time = 5.0
        test_sweep = pe.sweep.HostProgressionSweep()
        test_sweep._update_time_to_status_change(self.person1, current_time)
        self.assertIsInstance(self.person1.time_of_status_change, float)
        self.assertTrue(6.0 <= self.person1.time_of_status_change <= 15.0)

    def test_update_next_infection_status(self):
        
        test_sweep = pe.sweep.HostProgressionSweep()

        # Check assertion is raised if length of weights
        # and outcomes are different
        test_sweep.state_transition_matrix['Test col'] = ""
        with self.assertRaises(AssertionError):
            test_sweep._update_next_infection_status(self.people[0])

        # Check that method works with identity state matrix
        identity_matrix = pd.DataFrame(np.identity(len(InfectionStatus)),
                                   columns=['Susceptible', 'Exposed',
                                            'InfectASympt', 'InfectMild',
                                            'InfectGP', 'InfectHosp',
                                            'InfectICU', 'InfectICURecov',
                                            'Recovered', 'Dead'],
                                   index=['Susceptible', 'Exposed',
                                          'InfectASympt', 'InfectMild',
                                          'InfectGP', 'InfectHosp',
                                          'InfectICU', 'InfectICURecov',
                                          'Recovered', 'Dead'])
        test_sweep.state_transition_matrix = identity_matrix
        for person in self.people:
            test_sweep._update_next_infection_status(person)
            self.assertEqual(person.infection_status, person.next_infection_status)
        
        # Check that method works for each infection status with all people going
        # to dead infection status
        matrix = np.zeros([len(InfectionStatus), len(InfectionStatus)])
        matrix[:, -1] = 1
        matrix = pd.DataFrame(matrix,
                                columns=['Susceptible', 'Exposed',
                                            'InfectASympt', 'InfectMild',
                                            'InfectGP', 'InfectHosp',
                                            'InfectICU', 'InfectICURecov',
                                            'Recovered', 'Dead'],
                                index=['Susceptible', 'Exposed',
                                          'InfectASympt', 'InfectMild',
                                          'InfectGP', 'InfectHosp',
                                          'InfectICU', 'InfectICURecov',
                                          'Recovered', 'Dead'])
        test_sweep.state_transition_matrix = matrix
        for person in self.people:
            test_sweep._update_next_infection_status(person)
            self.assertEqual(person.next_infection_status, InfectionStatus.Dead)
        
        # Check that method works for an upper triangular state transition matrix.
        random_matrix = np.random.rand(len(InfectionStatus), len(InfectionStatus))
        random_matrix = np.triu(random_matrix)
        random_matrix = pd.DataFrame(random_matrix,
                                   columns=['Susceptible', 'Exposed',
                                            'InfectASympt', 'InfectMild',
                                            'InfectGP', 'InfectHosp',
                                            'InfectICU', 'InfectICURecov',
                                            'Recovered', 'Dead'],
                                   index=['Susceptible', 'Exposed',
                                          'InfectASympt', 'InfectMild',
                                          'InfectGP', 'InfectHosp',
                                          'InfectICU', 'InfectICURecov',
                                          'Recovered', 'Dead'])
        test_sweep.state_transition_matrix = random_matrix
        for person in self.people:
            test_sweep._update_next_infection_status(person)
            current_enum_value = person.infection_status.value
            next_enum_value = person.next_infection_status.value
            self.assertTrue(current_enum_value <= next_enum_value)


    @mock.patch('pyEpiabm.utility.InverseCdf.icdf_choose_exp')
    def test_call_main(self, mock_latent):
         """Tests the main function of the Host Progression Sweep.
         Person 1 is set to susceptible and becoming exposed. Person 2 is set to
         exposed and becoming infectious in one time step. Checks the
         population updates as expected. Check that Person 3 stays as
         susceptible.
         """
         mock_latent.return_value = 1.0
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
         self.state_transition_matrix = pe.Parameters.instance().state_transition_matrix
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
         mock_latent.assert_called_once()

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
         test_sweep.state_transition_matrix = pe.Parameters.instance().state_transition_matrix

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

         # Reconfigure population and check that a person is able to progress
         # infcetion status mutliple times in the same time step. This will be
         # checked by setting the latent time as 0 so Person 1 should progress
         # from suscptible to one if the infected statuses in the same time step.
         pe.Parameters.instance().latent_period_iCDF = np.zeros(21)
         self.person1.time_of_status_change = 1.0
         self.person1.update_status(InfectionStatus.Susceptible)
         self.person1.next_infection_status = InfectionStatus.Exposed
         test_sweep(1.0)
         self.assertIn(self.person1.infection_status,
                          [InfectionStatus.InfectMild, InfectionStatus.InfectASympt, InfectionStatus.InfectGP])


if __name__ == "__main__":
    unittest.main()
