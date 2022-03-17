import unittest
from unittest import mock

import pyEpiabm as pe
from pyEpiabm.core import Parameters


class TestAssignHouseholdAgesSweep(unittest.TestCase):
    """Tests the 'AssignHouseholdAgesSweep' class.
    """

    def setUp(self) -> None:
        """Set up population we can use throughout the test"""
        self.test_population = pe.Population()
        self.test_population.add_cells(1)
        self.test_population.cells[0].add_microcells(1)
        self.test_population.cells[0].microcells[0].add_people(6)
        self.person1 = self.test_population.cells[0].microcells[0].persons[0]
        self.person2 = self.test_population.cells[0].microcells[0].persons[1]
        self.person3 = self.test_population.cells[0].microcells[0].persons[2]
        self.person4 = self.test_population.cells[0].microcells[0].persons[3]
        self.person5 = self.test_population.cells[0].microcells[0].persons[4]
        self.person6 = self.test_population.cells[0].microcells[0].persons[5]
        self.age_params = Parameters.instance().household_age_params
        self.two_people = [self.person1, self.person2]
        self.three_people = [self.person1, self.person2, self.person3]
        self.four_people = [self.person1, self.person2,
                            self.person3, self.person4]

    def test_construct(self):
        """Tests that the assign household ages sweep initialises correctly.
        """
        pe.sweep.AssignHouseholdAgesSweep()

    @mock.patch('random.random')
    def test_one_person_household_age_elderly_person_case(self, mocked_random):
        """Tests method that assigns age to someone in a one person
        hosuehold for the case that the person is elderly.
        """
        # list of mocked values that will trigger the specific case of
        # the test below
        case_trigger_value = (Parameters.instance().household_age_params
                              ["one_pers_house_prob_old"] - 0.0001)
        mock_list = ([case_trigger_value, 0.0])
        mocked_random.side_effect = mock_list

        test_sweep = pe.sweep.AssignHouseholdAgesSweep()
        test_sweep.one_person_household_age(self.person1)
        self.assertTrue(self.person1.age
                        >= self.age_params["no_child_pers_age"])
        self.assertEqual(mocked_random.call_count, 2)

    @mock.patch('random.random')
    def test_one_person_household_age_young_single_case(self, mocked_random):
        """Tests method that assigns age to someone in a one person
        hosuehold for the case that the person is elderly.self.
        """
        # list of mocked values that will trigger the specific case of
        # the test below
        test_sweep = pe.sweep.AssignHouseholdAgesSweep()
        # adjust matrix to make sure this case is hit
        test_sweep.age_params["one_pers_house_prob_old"] = 0.0
        case_trigger_value = (((Parameters.instance().household_age_params
                                ["one_pers_house_prob_young"])
                              / (1 - Parameters.instance().
                              household_age_params["one_pers_house_prob_old"]))
                              - 0.001)
        mock_list = [case_trigger_value, 0.0]
        mocked_random.side_effect = mock_list

        test_sweep.one_person_household_age(self.person1)
        self.assertTrue(self.person1.age >= self.age_params["min_adult_age"])
        self.assertTrue(self.person1.age
                        <= self.age_params["young_and_single"])
        self.assertEqual(mocked_random.call_count, 2)

    @mock.patch('random.random')
    def test_one_person_household_age_adult_alone(self, mocked_random):
        """Tests method that assigns age to someone in a one person
        hosuehold for the case that the person is an adult living alone.
        """
        test_sweep = pe.sweep.AssignHouseholdAgesSweep()
        mocked_random.return_value = 2.0
        test_sweep.one_person_household_age(self.person1)
        self.assertTrue(self.person1.age >= self.age_params["min_adult_age"])

    def test_two_person_household_ages_people_list_test(self):
        """Tests method that assigns ages to people in a two person
        hosuehold throws error if it is passed a list of people
        greater than size 2.
        """
        test_sweep = pe.sweep.AssignHouseholdAgesSweep()

        # check that error is raised if provided list of people
        # is larger than 2
        test_list = [self.person1, self.person2, self.person3]
        with self.assertRaises(AssertionError):
            test_sweep.two_person_household_ages(test_list)

    @mock.patch('random.random')
    def test_two_person_household_ages_people_old_case(self, mocked_random):
        """Tests method that assigns ages to people in a two person
        hosuehold for the case that both of them are elderly.
        """
        # list of mocked values that will trigger the specific case of
        # the test below
        case_trigger_case = (Parameters.instance().household_age_params
                             ["two_pers_house_prob_old"] - 0.0001)
        mock_list = [case_trigger_case, 0.0, 0.0]
        mocked_random.side_effect = mock_list

        test_sweep = pe.sweep.AssignHouseholdAgesSweep()
        test_sweep.two_person_household_ages(self.two_people)
        self.assertTrue(self.person1.age
                        >= self.age_params["no_child_pers_age"])
        self.assertTrue(self.person2.age <= self.person1.age
                        + self.age_params["max_MF_partner_age_gap"])
        self.assertTrue(self.person2.age >= self.person1.age
                        - self.age_params["max_FM_partner_age_gap"])
        self.assertTrue(self.person2.age
                        >= self.age_params["no_child_pers_age"])
        self.assertEqual(mocked_random.call_count, 3)

    @mock.patch('random.random')
    def test_two_person_household_ages_child_adult_case(self, mocked_random):
        """Tests method that assigns ages to people in a two person
        hosuehold for the case of one child and adult living
        together.
        """
        test_sweep = pe.sweep.AssignHouseholdAgesSweep()
        test_sweep.age_params["two_pers_house_prob_old"] = 0.0
        # Value that will trigger the specific case of
        # the test below
        case_trigger_value = ((self.age_params["one_child_two_pers_prob"]
                              / (1 - self.age_params
                              ["two_pers_house_prob_old"])) - 0.00001)
        mocked_random.return_value = case_trigger_value

        test_sweep.two_person_household_ages(self.two_people)
        self.assertTrue(self.person1.age <= self.age_params["max_child_age"])
        self.assertTrue(self.person2.age <= self.person1.age
                        + self.age_params["max_parent_age_gap"])
        self.assertTrue(self.person2.age >= self.person1.age
                        + self.age_params["min_parent_age_gap"])
        self.assertTrue(self.person2.age >= self.age_params["min_adult_age"])
        mocked_random.assert_called_once()

    @mock.patch('random.random')
    def test_two_person_household_ages_young_adults(self, mocked_random):
        """Tests method that assigns ages to people in a two person
        hosuehold for the case of two young adults living
        together.
        """
        # Value that will trigger the specific case of
        # the test below
        test_sweep = pe.sweep.AssignHouseholdAgesSweep()
        test_sweep.age_params["two_pers_house_prob_old"] = 0.0
        test_sweep.age_params["one_child_two_pers_prob"] = 0.0
        case_trigger_value = ((self.age_params["two_pers_house_prob_young"]
                              / (1 - self.age_params["two_pers_house_prob_old"]
                                 - self.age_params
                                 ["one_child_two_pers_prob"])) - 0.001)
        mock_list = [case_trigger_value, 0.0]
        mocked_random.side_effect = mock_list

        test_sweep.two_person_household_ages(self.two_people)
        self.assertTrue(self.person1.age >= self.age_params["min_adult_age"])
        self.assertTrue(self.person1.age
                        <= self.age_params["young_and_single"])
        self.assertTrue(self.person2.age <= self. person1.age
                        + self.age_params["max_MF_partner_age_gap"])
        self.assertTrue(self.person2.age >= self.person1.age
                        - self.age_params["max_FM_partner_age_gap"])
        self.assertTrue(self.person2.age >= self.age_params["min_adult_age"])

    @mock.patch('random.random')
    def test_two_person_household_ages_adults(self, mocked_random):
        """Tests method that assigns ages to people in a two person
        hosuehold for the case of two adults living
        together.
        """

        test_sweep = pe.sweep.AssignHouseholdAgesSweep()
        mocked_random.return_value = 2.0
        test_sweep.two_person_household_ages(self.two_people)
        self.assertTrue(self.person1.age >= self.age_params["min_adult_age"])
        self.assertTrue(self.person2.age <= self.person1.age
                        + self.age_params["max_MF_partner_age_gap"])
        self.assertTrue(self.person2.age >= self.person1.age
                        - self.age_params["max_FM_partner_age_gap"])
        self.assertTrue(self.person2.age >= self.age_params["min_adult_age"])

    @mock.patch('random.random')
    def test_calc_number_of_children_method(self, mocked_random):
        """Tests method that calculates and return the
        number of children depending on input household
        size.
        """

        test_sweep = pe.sweep.AssignHouseholdAgesSweep()
        # test for possible cases of size three household
        mocked_random.return_value = 0.0
        val = test_sweep.calc_number_of_children(3)
        self.assertEqual(val, 0)

        mocked_random.side_effect = [2.0, 0.0]
        val = test_sweep.calc_number_of_children(3)
        self.assertEqual(val, 2)

        mocked_random.side_effect = [2.0, 2.0]
        val = test_sweep.calc_number_of_children(3)
        self.assertEqual(val, 1)

        test_sweep.age_params = {"zero_child_three_pers_prob": -1.0,
                                 "two_child_three_pers_prob": -1.0}
        val = test_sweep.calc_number_of_children(3)
        self.assertEqual(val, 1)

        # reinitialise sweep due to changing values in above test
        test_sweep = pe.sweep.AssignHouseholdAgesSweep()

        # test for possible cases of size 4 household
        mocked_random.side_effect = [-1.0]
        val = test_sweep.calc_number_of_children(4)
        self.assertEqual(val, 1)

        mocked_random.side_effect = [2.0]
        val = test_sweep.calc_number_of_children(4)
        self.assertEqual(val, 2)

        # test for possible cases of size 5 household
        mocked_random.side_effect = [-1.0]
        val = test_sweep.calc_number_of_children(5)
        self.assertTrue(val, 3)

        mocked_random.side_effect = [2.0]
        val = test_sweep.calc_number_of_children(5)
        self.assertEqual(val, 2)

        # test for case of households larger than 5 people
        mocked_random.side_effect = [1]
        val = test_sweep.calc_number_of_children(6)
        self.assertTrue(val == 1)

    @mock.patch(
        'pyEpiabm.sweep.AssignHouseholdAgesSweep.calc_number_of_children')
    def test_three_plus_person_household_ages_no_children(self,
                                                          mocked_children):
        """Tests method that assigns ages to people in a three person
        hosuehold for the case where they have no children.
        """
        test_sweep = pe.sweep.AssignHouseholdAgesSweep()
        mocked_children.return_value = 0
        test_sweep.three_or_more_person_household_ages(self.three_people)
        self.assertTrue(self.person2.age >= self.age_params["min_adult_age"])
        self.assertTrue(self.person1.age >= self.age_params["min_adult_age"])
        self.assertTrue(self.person3.age <= self.person2.age
                        + self.age_params["max_MF_partner_age_gap"])
        self.assertTrue(self.person3.age >= self.person2.age
                        - self.age_params["max_FM_partner_age_gap"])

    @mock.patch('random.random')
    @mock.patch('random.choices')
    @mock.patch('random.randint')
    @mock.patch(
        'pyEpiabm.sweep.AssignHouseholdAgesSweep.calc_number_of_children')
    def test_three_plus_person_household_ages_child_under_five(self,
                                                               mocked_children,
                                                               mocked_int,
                                                               mocked_choice,
                                                               mocked_random):
        """Tests method which assigns ages to people in a household of three or more
        for the case of a single child under five. Also tests the case of just
        two adults at home.
        """
        test_sweep = pe.sweep.AssignHouseholdAgesSweep()
        mocked_children.side_effect = [1]
        mocked_int.side_effect = [1, 0, 0]
        mocked_choice.side_effect = [[0], [6], [6]]
        mocked_random.side_effect = [0.0, 2.0, 2.0]
        test_sweep.three_or_more_person_household_ages(self.three_people)
        self.assertTrue(self.person1.age >= 0)
        self.assertTrue(self.person1.age <= 5)
        self.assertTrue(self.person1.age <= self.age_params["max_child_age"])
        self.assertTrue(self.person2.age
                        <= self.age_params["max_parent_age_gap"]
                        + self.person1.age)
        self.assertTrue(self.person2.age
                        >= self.age_params["min_parent_age_gap"])
        self.assertTrue(self.person2.age >= self.age_params["mind_adult_age"])
        self.assertTrue(self.person3.age <= self.person2.age
                        + self.age_params["max_MF_partner_age_gap"])
        self.assertTrue(self.person3.age >= self.person2.age
                        - self.age_params["max_FM_partner_age_gap"])
        self.assertTrue(self.person3.age <= self.person1.age
                        + self.age_params["max_parent_age_gap"])

    @mock.patch('random.random')
    @mock.patch('random.choices')
    @mock.patch('random.randint')
    @mock.patch(
        'pyEpiabm.sweep.AssignHouseholdAgesSweep.calc_number_of_children')
    def test_three_plus_person_household_ages_two_child_one_under_five(
                                                    self, mocked_children,
                                                    mocked_int,
                                                    mocked_choice,
                                                    mocked_random):
        """Tests method which assigns ages to people in a household of three or more
        for the case of two children with youngest child under five.
        """
        test_sweep = pe.sweep.AssignHouseholdAgesSweep()
        mocked_children.side_effect = [2]
        mocked_int.side_effect = [1, 0]
        mocked_choice.side_effect = [[0], [6]]
        mocked_random.side_effect = [0.0, 2.0]
        test_sweep.three_or_more_person_household_ages(self.three_people)
        self.assertTrue(self.person1.age >= 0)
        self.assertTrue(self.person1.age <= 5)
        self.assertTrue(self.person2.age <= self.age_params["max_child_age"])
        self.assertTrue(self.person3.age <= self.person1.age
                        + self.age_params["max_parent_age_gap"] + 5)
        self.assertTrue(self.person3.age >= self.person2.age
                        + self.age_params["min_parent_age_gap"])
        self.assertTrue(self.person3.age >= self.age_params["min_adult_age"])

    @mock.patch(
        'pyEpiabm.sweep.AssignHouseholdAgesSweep.calc_number_of_children')
    def test_three_plus_person_household_ages_more_adults(self,
                                                          mocked_children):
        """Tests method which assigns ages to people in a household of three or more
        for the case of there being at least three more adults in the house
        than children.
        """
        test_sweep = pe.sweep.AssignHouseholdAgesSweep()
        mocked_children.return_value = 1
        # edit parameter values so to hit coverage for all lines of method
        test_sweep.num_age_groups = 2
        test_sweep.age_proportions = [0.5, 0.5]
        test_sweep.age_group_width = 1
        test_sweep.three_or_more_person_household_ages(self.four_people)
        self.assertTrue(self.person4.age
                        >= self.age_params["no_child_pers_age"])
        # reset params to original values
        test_sweep.num_age_groups = len(Parameters.instance().age_proportions)
        test_sweep.age_proportions = Parameters.instance().age_proportions
        test_sweep.age_group_width = 5

    def test_call(self):
        """Tests the main function of the assign household ages
        sweep. People are put into households of different sizes, each
        being passed to a different method of the sweep. Their ages are then
        verified.
        """
        # set up populations and put people in households
        test_sweep = pe.sweep.AssignHouseholdAgesSweep()
        test_sweep.bind_population(self.test_population)
        one_pers_household = pe.Household()
        two_pers_household = pe.Household()
        three_pers_household = pe.Household()
        one_pers_household.add_person(self.person1)
        two_pers_household.add_person(self.person2)
        two_pers_household.add_person(self.person3)
        three_pers_household.add_person(self.person4)
        three_pers_household.add_person(self.person5)
        three_pers_household.add_person(self.person6)

        # reset everyone's ages to None
        for cell in self.test_population.cells:
            for person in cell.persons:
                person.age = None

        # call sweep and check people have proper ages
        test_sweep()
        self.assertTrue(self.person1.age >= self.age_params["min_adult_age"])
        for person in two_pers_household.persons:
            self.assertTrue(0 <= person.age <= 100)
        for person in three_pers_household.persons:
            print(person.age)
            self.assertTrue(0 <= person.age <= 100)


if __name__ == "__main__":
    unittest.main()
