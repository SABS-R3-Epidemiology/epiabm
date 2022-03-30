#
# Sweep to assign ages to people in households
#

import random
from scipy.stats import poisson
import numpy as np

from pyEpiabm.core import Person, Parameters
from .abstract_sweep import AbstractSweep


class AssignHouseholdAgesSweep(AbstractSweep):
    """Class to assign ages to people in
    households using the same age distribution
    model as covid-sim.
    """

    def __init__(self):
        """Call in variables from the parameters file.
        """
        self.age_params = Parameters.instance().household_age_params
        self.age_proportions = Parameters.instance().age_proportions
        self.num_age_groups = len(self.age_proportions)
        self.age_group_width = 5

    def one_person_household_age(self, person: Person):
        """Method that assigns an age to the person
        in a one person household. A random number is first drawn
        that decides which set of conditions the person's age
        should satisfy, e.g. if they are old or young and single etc. The
        person's age is then repeatedly set until it makes realsitic sense
        e.g they are not a child living alone.

        Parameters
        ----------

        Person : Person
            Instance of Person class

        """

        r = random.random()

        # case where an elderly person lives alone
        if r < self.age_params["one_pers_house_prob_old"]:
            while True:
                person.set_random_age()
                break_ratio = ((person.age
                                - self.age_params["no_child_pers_age"] + 1)
                               / (self.age_params["old_pers_age"]
                               - self.age_params["no_child_pers_age"]
                               + 1))
                if ((person.age >= self.age_params["no_child_pers_age"]) and
                   (random.random() <= break_ratio)):
                    break

        # case where a young and single adult lives alone
        elif ((self.age_params["one_pers_house_prob_young"] > 0) and
              (r < (self.age_params["one_pers_house_prob_young"]
               / (1 - self.age_params["one_pers_house_prob_old"])))):
            while True:
                person.set_random_age()
                break_ratio = (
                    1 - self.age_params["young_and_single_slope"]
                    * ((person.age - self.age_params["min_adult_age"])
                        / (self.age_params["young_and_single"]
                           - self.age_params["min_adult_age"])))
                if ((person.age <= self.age_params["young_and_single"]) and
                   (person.age >= self.age_params["min_adult_age"]) and
                   (random.random() <= break_ratio)):
                    break

        # case where it is just one adult living alone
        else:
            while True:
                person.set_random_age()
                if person.age >= self.age_params["min_adult_age"]:
                    break

    def two_person_household_ages(self, people):
        """Method that assigns ages to the people
        in a two person household. A random number is first drawn
        that decides which set of conditions the people's ages
        should satisfy, e.g. if they are both old or it is one parent
        and one child etc. The people's ages are then repeatedly set
        until it makes realsitic sense e.g their ages are compatible
        if they are a couple.

        Parameters
        ----------

        People : list
            List of two Instances of Person class

        """

        r = random.random()
        person1 = people[0]
        person2 = people[1]
        assert len(people) == 2,\
               'Only a list of two people should be passed to this method'

        # case where two elderly people live alone
        if r < self.age_params["two_pers_house_prob_old"]:
            while True:
                person1.set_random_age()
                break_ratio = ((person1.age
                               - self.age_params["no_child_pers_age"] + 1)
                               / (self.age_params["old_pers_age"]
                               - self.age_params["no_child_pers_age"] + 1))
                if ((person1.age >= self.age_params["no_child_pers_age"]) and
                   (random.random() <= break_ratio)):
                    break
            while True:
                person2.set_random_age()
                break_ratio = ((person2.age
                                - self.age_params["no_child_pers_age"] + 1)
                               / (self.age_params["old_pers_age"]
                               - self.age_params["no_child_pers_age"] + 1))
                if ((person2.age <= person1.age
                   + self.age_params["max_MF_partner_age_gap"]) and
                   (person2.age >= person1.age
                   - self.age_params["max_FM_partner_age_gap"]) and
                   (person2.age >= self.age_params["no_child_pers_age"]) and
                   (random.random() <= break_ratio)):
                    break

        # case where one child and one adult live together
        elif r < (self.age_params["one_child_two_pers_prob"]
                  / (1 - self.age_params["two_pers_house_prob_old"])):
            while True:
                person1.set_random_age()
                if person1.age <= self.age_params["max_child_age"]:
                    break
            while True:
                person2.set_random_age()
                if ((person2.age <= person1.age
                     + self.age_params["max_parent_age_gap"]) and
                   (person2.age >= person1.age
                    + self.age_params["min_parent_age_gap"]) and
                   (person2.age >= self.age_params["min_adult_age"])):
                    break

        # case where two young adults live together
        elif (self.age_params["two_pers_house_prob_young"] > 0) and\
             (r < (self.age_params["two_pers_house_prob_young"]
              / (1 - self.age_params["two_pers_house_prob_old"]
                 - self.age_params["one_child_two_pers_prob"]))):
            while True:
                person1.set_random_age()
                break_ratio = 1 - (self.age_params["young_and_single_slope"]
                                   * ((person1.age
                                       - self.age_params["min_adult_age"])
                                      / (self.age_params["young_and_single"]
                                      - self.age_params["min_adult_age"])))
                if ((person1.age >= self.age_params["min_adult_age"]) and
                   (person1.age <= self.age_params["young_and_single"]) and
                   (random.random() <= break_ratio)):
                    break
            while True:
                person2.set_random_age()
                if ((person2.age <= person1.age
                   + self.age_params["max_MF_partner_age_gap"]) and
                   (person2.age >= person1.age
                   - self.age_params["max_FM_partner_age_gap"]) and
                   (person2.age >= self.age_params["min_adult_age"])):
                    break

        # case where two adults of any appropriate age live together
        else:
            while True:
                person1.set_random_age()
                if person1.age >= self.age_params["min_adult_age"]:
                    break
            while True:
                person2.set_random_age()
                if ((person2.age <= person1.age
                   + self.age_params["max_MF_partner_age_gap"]) and
                   (person2.age >= person1.age
                    - self.age_params["max_FM_partner_age_gap"]) and
                   (person2.age >= self.age_params["min_adult_age"])):
                    break

    def calc_number_of_children(self, household_size: int):
        """ Method that calculates the amount of children in
        a household of three or more people.

        Parameters
        ----------

        household_size : int
            Number of people in a household

        Returns
        -------
        nc : int
            Number of children that will be in that household

        """

        n = household_size

        # calculate number of children in a 3 person household
        if n == 3:
            if ((self.age_params["zero_child_three_pers_prob"] > 0) or
                    (self.age_params["two_child_three_pers_prob"] > 0)):
                if (random.random()
                   < self.age_params["zero_child_three_pers_prob"]):
                    num_childs = 0
                else:
                    if (random.random()
                            < self.age_params["two_child_three_pers_prob"]):
                        num_childs = 2
                    else:
                        num_childs = 1
            else:
                num_childs = 1

        # calculate number of children in a 4 person household
        if n == 4:
            num_childs = 1 if (random.random()
                               < self.age_params
                               ["one_child_four_pers_prob"]) else 2

        # calculate number of children in a 5 person household
        if n == 5:
            num_childs = 3 if (random.random()
                               < self.age_params
                               ["three_child_five_pers_prob"]) else 2

        # calculate the number of children in a household with more than
        # 5 people
        if n > 5:
            num_childs = n - 2 - np.floor(3 * random.random())

        # return number of children
        return num_childs

    def three_or_more_person_household_ages(self, people: list):
        """ Method that assigns ages to the people
        in a three person or larger sized household.
        The number of children is first calculated, this then decides which
        set of conditions the people's ages should satisfy, e.g. if they
        are both old or it is one parent and one child etc. The people's
        ages are then repeatedly set until it makes realsitic sense e.g
        their ages are compatible if they are a couple.

        Parameters
        ----------

        People : list
            List of three or more Instances of Person class

        """

        n = len(people)
        num_childs = self.calc_number_of_children(n)

        # case of zero children in a household, only possible
        # in a household of size three
        if num_childs == 0:
            while True:
                people[0].set_random_age()
                people[1].set_random_age()
                if ((people[1].age >= self.age_params["min_adult_age"]) and
                        (people[0].age >= self.age_params["min_adult_age"])):
                    break
            while True:
                people[2].set_random_age()
                if ((people[2].age <= people[1].age
                     + self.age_params["max_MF_partner_age_gap"]) and
                        (people[2].age >= people[1].age
                         - self.age_params["max_FM_partner_age_gap"])):
                    break

        # set ages when children are members of a household
        else:
            while True:
                people[0].age = 0
                # set ages of children, increasing the ages between them if
                # there are multiple children in the house
                for i in range(1, num_childs):
                    people[i].age = (people[i-1].age + 1
                                     + poisson.rvs((self.age_params
                                                   ["mean_child_age_gap"]
                                                   - 1)))
                random_child_index = int(np.floor(
                                         random.random() * num_childs))
                age_group = random.choices(range(self.num_age_groups),
                                           weights=self.age_proportions)[0]
                age = random.randint(0, 4) + 5 * age_group
                people[0].age = age - people[random_child_index].age
                # increase base age of children relative to youngest child
                for i in range(1, num_childs):
                    people[i].age += people[0].age
                # set max age of youngest child
                youngest_age = 5 if \
                    (((num_childs == 1) and
                        (random.random()
                         < self.age_params
                         ["one_child_prob_youngest_child_under_five"])) or
                     ((num_childs == 2) and
                        (random.random()
                            < self.age_params
                            ["two_children_prob_youngest_under_five"]))) else \
                    self.age_params["max_child_age"]
                if ((people[0].age >= 0) and
                        (people[0].age <= youngest_age) and
                        (people[num_childs - 1].age
                         <= self.age_params["max_child_age"])):
                    break

            # sets age difference of parents and children
            parent_age_gap = (people[num_childs - 1].age - people[0].age
                              - (self.age_params["max_parent_age_gap"]
                              - self.age_params["min_parent_age_gap"]))
            if parent_age_gap > 0:
                parent_age_gap += \
                    self.age_params["max_parent_age_gap"]  # pragma: no cover
            else:
                parent_age_gap = self.age_params["max_parent_age_gap"]
            while True:
                people[num_childs].set_random_age()
                youngest_age = people[num_childs - 1].age
                # makes sure age of first parent is appropriate
                # for their children
                if ((people[num_childs].age <= people[0].age + parent_age_gap)
                    and (people[num_childs].age
                         >= youngest_age
                         + self.age_params["min_parent_age_gap"]) and
                        (people[num_childs].age
                         >= self.age_params["min_adult_age"])):
                    break

            # makes sure if both parents are in the same household their age
            # makes sense
            if ((n > num_childs + 1) and
                    (random.random()
                     > self.age_params["prop_other_parent_away"])):
                while True:
                    people[num_childs + 1].set_random_age()
                    if ((people[num_childs + 1].age
                        <= people[num_childs].age
                        + self.age_params["max_MF_partner_age_gap"]) and
                        (people[num_childs + 1].age
                        >= people[num_childs].age
                        - self.age_params["max_FM_partner_age_gap"]) and
                        (people[num_childs + 1].age
                        <= people[0].age + parent_age_gap) and
                        (people[num_childs + 1].age
                        >= youngest_age
                        + self.age_params["min_parent_age_gap"]) and
                            (people[num_childs + 1].age
                             >= self.age_params["min_adult_age"])):
                        break

            # considers case of more than 2 adults in house such as parents
            # and grandparents
            if n > num_childs + 2:
                j = (people[num_childs + 1].age if
                     people[num_childs + 1].age
                     > people[num_childs].age else people[num_childs].age)
                j += self.age_params["older_gen_gap"]
                if j >= self.num_age_groups * self.age_group_width:
                    j = self.num_age_groups * self.age_group_width - 1
                if j < self.age_params["no_child_pers_age"]:
                    j = self.age_params["no_child_pers_age"]
                for i in range(num_childs + 2, n):
                    while True:
                        people[i].set_random_age()
                        if people[i].age >= j:
                            break

    def __call__(self):
        """Given a population structure, loops over all people
        assigns them an age dependant on their household size.
        """

        households_list = []
        for cell in self._population.cells:
            for person in cell.persons:
                household = person.household
                # checks we haven't already looped through this household
                if household not in households_list:
                    if len(household.persons) == 1:
                        self.one_person_household_age(household.persons[0])
                    elif len(household.persons) == 2:
                        self.two_person_household_ages(household.persons)
                    else:
                        self.three_or_more_person_household_ages(
                            household.persons)
                    households_list.append(household)
