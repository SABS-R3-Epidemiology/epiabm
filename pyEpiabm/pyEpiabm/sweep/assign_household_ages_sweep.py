#
# Sweep to assign ages to people in households
#

import random

from pyEpiabm.core import Person
from pyEpiabm.core import Parameters
from .abstract_sweep import AbstractSweep


class AssignHouseholdAges(AbstractSweep):
    """Class to assign ages to people in
    households using the same age distribution
    model as covid-sim.
    """

    def __init__(self):
        """Call in variables from the parameters file.
        """
        self.mean_child_age_gap = Parameters.instance().mean_child_age_gap
        self.min_adult_age = Parameters.instance().min_adult_age
        self.max_MF_partner_age_gap =\
            Parameters.instance().max_MF_partner_age_gap
        self.max_FM_partner_age_gap =\
            Parameters.instance().max_FM_partner_age_gap
        self.min_parent_age_gap = Parameters.instance().min_parent_age_gap
        self.max_parent_age_gap = Parameters.instance().max_parent_age_gap
        self.max_child_age = Parameters.instance().max_child_age
        self.one_child_two_pers_prob =\
            Parameters.instance().one_child_two_pers_prob
        self.two_child_three_pers_prob =\
            Parameters.instance().two_child_three_pers_prob
        self.one_pers_house_prob_old =\
            Parameters.instance().one_pers_house_prob_old
        self.two_pers_house_prob_old =\
            Parameters.instance().two_pers_house_prob_old
        self.one_pers_house_prob_young =\
            Parameters.instance().one_pers_house_prob_young
        self.two_pers_house_prob_young =\
            Parameters.instance().two_pers_house_prob_young
        self.one_child_prob_youngest_child_under_five =\
            Parameters.instance().one_child_prob_youngest_child_under_five
        self.prob_youngest_child_under_five =\
            Parameters.instance().prob_youngest_child_under_five
        self.zero_child_three_pers_prob =\
            Parameters.instance().zero_child_three_pers_prob
        self.one_child_four_pers_prob =\
            Parameters.instance().one_child_four_pers_prob
        self.young_and_single_slope =\
            Parameters.instance().young_and_single_slope
        self.young_and_single = Parameters.instance().young_and_single
        self.no_child_pers_age = Parameters.instance().no_child_pers_age
        self.old_pers_age = Parameters.instance().old_pers_age
        self.three_child_five_pers_prob =\
            Parameters.instance().three_child_five_pers_prob
        self.older_gen_gap = Parameters.instance().older_gen_gap

    def one_person_household_age(self, person: Person):
        """ Method that assigns an age to the person
        belonging to a one person household. A random number is first drawn
        that decides which set of conditions the person's age
        should satisfy e.g. if they are old or young and single etc. The
        person's age is then repeatedly set until it makes realsitic sense
        e.g they are not a child living alone for example.

        Parameters
        ----------

        Person : Person
            Instance of Person class

        """

        r = random.random()

        if r < self.one_pers_house_prob_old:
            while True:
                person.set_random_age()
                break_ratio = ((person.age - self.no_child_pers_age + 1)
                               / (self.old_pers_age - self.no_child_pers_age
                               + 1))
                if (person.age >= self.no_child_pers_age) and\
                   (random.random() <= break_ratio):
                    break
        elif (self.one_pers_house_prob_young > 0) and \
            (r < (self.one_pers_house_prob_young
             / (1 - self.one_pers_house_prob_old))):
            while True:
                person.set_random_age()
                break_ratio = (
                    1 - self.young_and_single_slope
                    * ((person.age - self.min_adult_age)
                        / (self.young_and_single - self.min_adult_age)))
                if (person.age <= self.young_and_single) and\
                   (person.age >= self.min_adult_age) and\
                   (random.random() <= break_ratio):
                    break
        else:
            while True:
                person.set_random_age()
                if person.age >= self.min_adult_age:
                    break

    def two_person_household_ages(self, people):

        r = random.random()
        person1 = people[0]
        person2 = people[1]
        assert len(people) == 2,\
               'Only a list of two people should be passed to this method'

        if r < self.two_pers_house_prob_old:
            while True:
                person1.set_random_age()
                break_ratio = ((person1.age - self.no_child_pers_age + 1)
                               / (self.old_pers_age
                               - self.no_child_pers_age + 1))
                if (person1.age >= self.no_child_pers_age) and\
                   (random.random() <= break_ratio):
                    break
            while True:
                person2.set_random_age()
                break_ratio = ((person2.age - self.no_child_pers_age + 1)
                               / (self.old_pers_age
                               - self.no_child_pers_age + 1))
                if (person2.age <= person1.age
                   + self.max_MF_partner_age_gap) and\
                   (person2.age >= person1.age
                   - self.max_FM_partner_age_gap) and\
                   (person2.age >= self.no_child_pers_age) and\
                   (random.random <= break_ratio):
                    break
        elif r < (self.one_child_two_pers_prob
                  / (1 - self.two_pers_house_prob_old)):
            person1.set_random_age()
            # unsure about this
            while person1.age > self.max_child_age:
                person2.set_random_age()
                if (person2.age <= person1.age + self.max_parent_age_gap) and\
                   (person2.age >= person1.age + self.min_parent_age_gap) and\
                   (person2.age >= self.min_adult_age):
                    break
                person1.set_random_age()
        elif (self.two_pers_house_prob_young > 0) and\
             (r < (self.two_pers_house_prob_young
              / (1 - self.two_pers_house_prob_old
                 - self.one_child_two_pers_prob))):
            while True:
                person1.set_random_age()
                break_ratio = 1 - (self.young_and_single_slope
                                   * ((person1.age - self.min_adult_age)
                                      / (self.young_and_single
                                      - self.min_adult_age)))
                if (person1.age >= self.min_adult_age) and\
                   (person1.age <= self.young_and_single) and\
                   (random.random() <= break_ratio):
                    break
            while True:
                person2.set_random_age()
                if (person2.age <= person1.age
                   + self.max_MF_partner_age_gap) and\
                   (person2.age >= person1.age
                   - self.max_FM_partner_age_gap) and\
                   (person2.age >= self.min_adult_age):
                    break
        else:
            while True:
                person1.set_random_age()
                if person1.age >= self.min_adult_age:
                    break
            while True:
                person2.set_random_age()
                if (person2.age <= person1.age
                   + self.max_MF_partner_age_gap) and\
                   (person2.age >= person1.age
                    - self.max_FM_partner_age_gap) and\
                   (person2.age >= self.min_adult_age):
                    break
