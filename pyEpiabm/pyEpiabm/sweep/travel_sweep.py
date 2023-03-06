#
# Introduce to and remove individuals from population due to travelling
#
import numpy as np
import random
import math

from pyEpiabm.core import Population, Parameters, Microcell
from pyEpiabm.property import InfectionStatus
from pyEpiabm.sweep import HostProgressionSweep
from .abstract_sweep import AbstractSweep


class TravelSweep(AbstractSweep):
    """Class to run the introduction and removing of
    individuals. The number of introduced individuals
    depends on the number of total infectious cases in the
    population. All indivuals are infectious when entering
    the population and will distributed over microcells based
    on population density of the microcells. Individuals will
    be removed from the population after a certain number of days
    depening on if they are isolated or quarantined.
    """

    def __init__(self):
        """Call in variables from the parameters file
        """
        self.travel_params = Parameters.instance().travel_params
        self.introduce_population = Population()
        self.introduce_population.add_cells(1)
        self.initial_cell = self.introduce_population.cells[0]
        self.initial_cell.add_microcells(1)
        self.initial_microcell = self.initial_cell.microcells[0]

    def __call__(self, time: float):
        """ Based on number of infected cases in population, infected
        individuals are introduced to the population for a certain
        period. They are distributed over the microcells based on
        population density. They are not assigned perminently to
        a place for the durationg of their visit.

        Parameters
        ----------
        time : float
            Simulation time
        """
        # Introduce number of individuals
        num_cases = sum(map(lambda cell: cell.number_infectious(),
                        self._population.cells))
        number_individuals_introduced = math.floor(
            num_cases * self.travel_params['ratio_introduce_cases'])

        if number_individuals_introduced >= 1:
            # Make individuals
            # Assign age and infectious status based on age
            asymp_prop = Parameters.instance().host_progression_lists[
                "prob_exposed_to_asympt"]
            # if age is used in model
            if Parameters.instance().use_ages:
                age_prop = Parameters.instance().age_proportions
                # travellers are between 15-80 years
                age_prop_adjusted = [0.0 if i in [0, 1, 2, 16] else
                                     prop for i, prop in
                                     enumerate(age_prop)]
                w = age_prop_adjusted / sum(age_prop_adjusted)
                microcell_split = np.random.multinomial(
                    number_individuals_introduced, w, size=1)[0]
                for age in range(len(age_prop_adjusted)):
                    number_indiv_agegroup = microcell_split[age]
                    number_indiv_agegroup_InfectedAsympt = \
                        math.floor(asymp_prop[age] * number_indiv_agegroup)
                    number_indiv_agegroup_InfectedMild = \
                        number_indiv_agegroup - \
                        number_indiv_agegroup_InfectedAsympt
                    self.initial_microcell.add_people(
                        number_indiv_agegroup_InfectedAsympt,
                        status=InfectionStatus.InfectASympt,
                        age_group=age)
                    self.initial_microcell.add_people(
                        number_indiv_agegroup_InfectedMild,
                        status=InfectionStatus.InfectMild,
                        age_group=age)
            else:
                if isinstance(asymp_prop, list):
                    asymp_prop = asymp_prop[0]
                number_indiv_InfectedAsympt = \
                    math.floor(asymp_prop * number_individuals_introduced)
                number_indiv_InfectedMild = number_individuals_introduced - \
                    number_indiv_InfectedAsympt
                self.initial_microcell.add_people(
                        number_indiv_InfectedAsympt,
                        status=InfectionStatus.InfectASympt)
                self.initial_microcell.add_people(
                        number_indiv_InfectedMild,
                        status=InfectionStatus.InfectMild)

            for person in self.initial_cell.persons:
                # Assign introduced individuals a time to stay
                person.travel_end_time = time + random.randint(2, 14)
                # Assigns them their next infection status and the time of
                # their next status change. Also updates their infectiousness.
                person.next_infection_status = InfectionStatus.Recovered
                HostProgressionSweep.set_infectiousness(person, time)
                HostProgressionSweep().update_time_status_change(person, time)

            # Assign introduced individuals to microcells based on population
            # density of micorcells. Take a number of microcells equal to the
            # the number_individuals_introduced and assign individuals randomly
            # to one of these microcells, such that individuals can end up in
            # the same microcell.
            num_microcells_population = sum(len(cell.microcells) for cell in
                                            self._population.cells)
            microcells_to_choose_dict = {}
            for i in range(min(number_individuals_introduced,
                               num_microcells_population)):
                # initialise with default microcell
                microcells_to_choose_dict[Microcell(self.initial_cell)] = 0
            # Find highest density microcells
            for possible_cell in self._population.cells:
                for possible_microcell in possible_cell.microcells:
                    density_microcells_list = list(
                        microcells_to_choose_dict.values())
                    if min(density_microcells_list) < len(
                            possible_microcell.persons):
                        # remove old object
                        microcells_to_choose_dict.pop(list(
                            microcells_to_choose_dict.keys())[
                            list(microcells_to_choose_dict.values()).index(
                                min(density_microcells_list))])
                        # add new microcell
                        microcells_to_choose_dict[possible_microcell] = \
                            len(possible_microcell.persons)

            # Assign to microcell and household in existing population
            for person in self.initial_cell.persons:
                selected_microcell = random.choice(list(
                    microcells_to_choose_dict.keys()))
                # Assign person to microcell and microcell to person
                selected_microcell.add_person(person)
                person.microcell = selected_microcell
                r = random.random()
                if r < self.travel_params['prob_existing_household']:
                    # Assign to existing household
                    # Q: Do we need to check if household not full?
                    selected_household = random.choice(
                        selected_microcell.households)
                    selected_household.add_person(person)
                else:
                    # Create new household
                    selected_microcell.add_household([person])

            # Remove introduced individuals from introduce population
            self.initial_cell.persons = []
            self.initial_microcell.persons = []

        # Remove travelling people from population if their
        # travel_end_time reached
        persons_to_remove = []
        for cell in self._population.cells:
            for person in cell.persons:
                if (hasattr(person, 'travel_end_time')) and (
                        time > person.travel_end_time):
                    persons_to_remove.append(person)
                    # Remove from cell, microcell and household
                    person.microcell.cell.persons.remove(person)
                    person.microcell.persons.remove(person)
                    person.household.persons.remove(person)