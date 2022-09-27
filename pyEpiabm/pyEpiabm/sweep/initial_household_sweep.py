#
# Sweep to assign people to households and set their ages
#

import random
import numpy as np

from pyEpiabm.core import Parameters, Person, Population

from .abstract_sweep import AbstractSweep


class InitialHouseholdSweep(AbstractSweep):
    """Class to assign ages to people in
    households using the same age distribution
    model as CovidSim.
    """

    def __init__(self):
        """Call in variables from the parameters file.
        """

        self.use_ages = Parameters.instance().use_ages
        self.household_size_distribution \
            = Parameters.instance().household_size_distribution
        self.max_household_size = Parameters.instance().max_household_size
        self.age_params = Parameters.instance().household_age_params
        self.age_proportions = Parameters.instance().age_proportions
        self.num_age_groups = len(self.age_proportions)
        self.age_group_width = 5

    def household_allocation(self, population: Population):
        """Method that takes in a population and assigns them to different
        sized households according to a household size distribution.

        Parameters
        ----------
        Population: Population
            Instance of Population class
        """

        for cell in population.cells:
            for microcell in cell.microcells:
                k = 0  # Counter of people with allocated household in mcell
                while k < len(microcell.persons):
                    m = 1  # Current size of household
                    s = random.random()

                    # Ancreases household size count relative to household size
                    # distribution. Count stops if maximum household size is
                    # reached or there aren't enough unassigned people left
                    # in microcell
                    while True:
                        if ((s <= self.household_size_distribution[m - 1]) or
                                (k + m >= len(microcell.persons)) or
                                (m >= self.max_household_size)):
                            break   # pragma: no cover
                        s -= self.household_size_distribution[m - 1]
                        m += 1

                    # Assign people to chosen size household
                    people_in_household = []
                    for i in range(k, k + m):
                        people_in_household.append(microcell.persons[i])
                    microcell.add_household(people_in_household)
                    k += m

    def one_person_household_age(self, person: Person):
        """Method that assigns an age to the person
        in a one person household. A random number is first drawn
        that decides which set of conditions the person's age
        should satisfy, e.g. if they are old or young and single etc. The
        person's age is then repeatedly set until it is realistic
        e.g they are not a child living alone.

        Parameters
        ----------
        Person : Person
            Instance of Person class

        """

        r = random.random()

        # Case where an elderly person lives alone
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

        # Case where a young and single adult lives alone
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

        # Case where it is just one adult living alone of any age
        # older than minimum adult age
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
        until they are realistic e.g their ages are compatible
        if they are a couple.

        Parameters
        ----------
        People : list
            List of two instances of Person class

        """

        r = random.random()
        assert len(people) == 2,\
               'Only a list of two people should be passed to this method'
        person1 = people[0]
        person2 = people[1]

        # Case where two elderly people live alone
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

        # Case where one child and one adult live together
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

        # Case where two young adults live together
        elif ((self.age_params["two_pers_house_prob_young"] > 0) and
                (r < (self.age_params["two_pers_house_prob_young"]
                      / (1 - self.age_params["two_pers_house_prob_old"]
                 - self.age_params["one_child_two_pers_prob"])))):
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

        # Case where two adults of any appropriate age live together
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
        int : Number of children that will be in that household

        """

        n = household_size

        # Calculate number of children in a 3 person household
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

        # Calculate number of children in a 4 person household
        if n == 4:
            num_childs = 1 if (random.random()
                               < self.age_params
                               ["one_child_four_pers_prob"]) else 2

        # Calculate number of children in a 5 person household
        if n == 5:
            num_childs = 3 if (random.random()
                               < self.age_params
                               ["three_child_five_pers_prob"]) else 2

        # Calculate the number of children in a household with more than
        # 5 people
        if n > 5:
            num_childs = n - 2 - np.floor(3 * random.random())

        return num_childs

    def three_or_more_person_household_ages(self, people: list):
        """ Method that assigns ages to the people
        in a three person or larger sized household.
        The number of children is first calculated, this then decides which
        set of conditions the people's ages should satisfy, e.g. if they
        are both old or it is one parent and one child etc. The people's
        ages are then repeatedly set until they are realistic e.g
        their ages are compatible if they are a couple.

        Parameters
        ----------
        People : list
            List of three or more instances of Person class

        """

        n = len(people)
        num_childs = int(np.floor(self.calc_number_of_children(n)))

        # Case of zero children in a household, only possible
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

        # Set ages when children are members of a household
        else:
            while True:
                people[0].age = 0
                # Set ages of children, increasing the ages between them if
                # there are multiple children in the house
                for i in range(1, num_childs):
                    people[i].age = (
                        people[i-1].age + 1
                        + np.random.poisson((self.age_params
                                            ["mean_child_age_gap"] - 1)))
                random_child_index = int(np.floor(
                                         random.random() * num_childs))
                age_group = random.choices(range(self.num_age_groups),
                                           weights=self.age_proportions)[0]
                age = random.randint(0, 4) + 5 * age_group
                people[0].age = age - people[random_child_index].age
                # Increase base age of children relative to youngest child
                for i in range(1, num_childs):
                    people[i].age += people[0].age
                # Set max age of youngest child
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
                # Makes sure age of first parent is appropriate
                # for their children
                if ((people[num_childs].age <= people[0].age + parent_age_gap)
                    and (people[num_childs].age
                         >= youngest_age
                         + self.age_params["min_parent_age_gap"]) and
                        (people[num_childs].age
                         >= self.age_params["min_adult_age"])):
                    break

            # Makes sure if both parents are in the same household their age
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

            # Considers case of more than 2 adults in house such as parents
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

    def __call__(self, sim_params):
        """Given a population structure, sorts the people into households
        of required size and if required loops over all people and assigns
        them an age dependant on their household size.
        """

        # Call method to put people into households and check to see
        # if people are already in households (this check makes testing
        # this method easier)
        for cell in self._population.cells:
            for microcell in cell.microcells:
                if len(microcell.households) == 0:
                    self.household_allocation(self._population)
                    break

        # If ages need to be set call method to assign
        # ages of people in households
        if self.use_ages:
            for cell in self._population.cells:
                cell.compartment_counter.clear_counter()
                for microcell in cell.microcells:
                    microcell.compartment_counter.clear_counter()
                    for household in microcell.households:
                        if len(household.persons) == 1:
                            self.one_person_household_age(household.persons[0])

                        elif len(household.persons) == 2:
                            self.two_person_household_ages(household.persons)

                        else:
                            self.three_or_more_person_household_ages(
                                household.persons)

                        for person in household.persons:
                            status = person.infection_status
                            age_group = person.age_group
                            person.microcell.compartment_counter.\
                                _increment_compartment(1, status, age_group)
                            person.microcell.cell.compartment_counter.\
                                _increment_compartment(1, status, age_group)
