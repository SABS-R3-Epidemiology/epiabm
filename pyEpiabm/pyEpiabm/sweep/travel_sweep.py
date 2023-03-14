#
# Introduce and remove individuals from population due to travelling
#

import numpy as np
import random
import math

from pyEpiabm.core import Population, Parameters, Microcell, Person
from pyEpiabm.property import InfectionStatus
from pyEpiabm.sweep import HostProgressionSweep

from .abstract_sweep import AbstractSweep


class TravelSweep(AbstractSweep):
    """Class to manage the introduction and removal of
    individuals. The number of individuals introduced
    depends on the number of total infectious cases in the
    population. All individuals are infectious when entering
    the population and will be distributed over microcells based
    on population density of the microcells. Individuals will
    be removed from the population after a certain number of days
    if they are isolated or quarantined.

    """

    def __init__(self):
        """Call in variables from the parameters file.

        """
        self.travel_params = Parameters.instance().travel_params
        self.introduce_population = Population()
        self.introduce_population.add_cells(1)
        self.initial_cell = self.introduce_population.cells[0]
        self.initial_cell.add_microcells(1)
        self.initial_microcell = self.initial_cell.microcells[0]
        self.travellers = []

    def __call__(self, time: float):
        """Based on number of infected cases in population, infected
        individuals are introduced to the population for a certain
        period. They are distributed over the microcells based on
        population density. They are not assigned permanently to
        a place for the duration of their visit.

        Parameters
        ----------
        time : float
            Simulation time

        """
        # Introduce number of individuals
        num_cases = sum(map(lambda cell: cell.number_infectious(),
                        self._population.cells))
        num_individuals_introduced_ratio = math.floor(
            num_cases * self.travel_params['ratio_introduce_cases'])
        if len(self.travel_params['constant_introduce_cases']) > 1:
            num_individuals_introduced_constant = self.travel_params[
                'constant_introduce_cases'][int(time)]
        else:
            num_individuals_introduced_constant = self.travel_params[
                'constant_introduce_cases'][0]
        number_individuals_introduced = num_individuals_introduced_ratio + \
            num_individuals_introduced_constant

        if number_individuals_introduced >= 1:
            self.create_introduced_individuals(
                time, number_individuals_introduced)
            self.assign_microcell_and_household(
                number_individuals_introduced)

            # Remove individuals introduced from introduce_population
            self.initial_cell.persons = []
            self.initial_microcell.persons = []

        # Remove individuals if the duration of their stay has passed
        self.remove_leaving_individuals(time)

    def create_introduced_individuals(self, time,
                                      number_individuals_introduced):
        """Create individuals and assign them an age and infectious status.
        This is based on age proportions if age is used in the model.
        Individuals are assigned an age between 15-80 years and are all
        infected (mild or asymptomatic).

        Parameters
        ----------
        time : float
            Simulation time
        number_individuals_introduced: int
            Infected individuals added to population at certain time step

        """
        asymp_prop = Parameters.instance().host_progression_lists[
            "prob_exposed_to_asympt"]
        if Parameters.instance().use_ages:
            # Age used in model
            age_prop = Parameters.instance().age_proportions
            # Travellers are between 15-80 years
            age_prop_adjusted = [0.0 if i in [0, 1, 2, 16] else prop for
                                 i, prop in enumerate(age_prop)]
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
            # Age not used in model
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
            person.travel_end_time = time + random.randint(
                self.travel_params["duration_travel_stay"][0],
                self.travel_params["duration_travel_stay"][1])
            # Assigns them their next infection status and the time of
            # their next status change. Also updates their infectiousness.
            person.next_infection_status = InfectionStatus.Recovered
            HostProgressionSweep.set_infectiousness(person, time)
            HostProgressionSweep().update_time_status_change(person, time)
            # Store travellers
            self.travellers.append(person)

    def assign_microcell_and_household(self, number_individuals_introduced):
        """Assign individuals introduced to microcells based on population
        density of micorcells in the general population. A number of microcells
        equal to the number_individuals_introduced (or max number of
        microcells) with highest population density are selected. The
        individuals are assigned to one of these microcells by a uniform random
        choice between them. Individuals can end up in the same microcell.
        Next, individuals are assigned to an wxisting or a new household within
        the selected microcell.

        Parameters
        ----------
        number_individuals_introduced: int
            Infected individuals added to population at certain time step

        """
        num_microcells_population = sum(len(cell.microcells) for cell in
                                        self._population.cells)
        microcells_to_choose_dict = {Microcell(self.initial_cell): 0 for _ in
                                     range(min(number_individuals_introduced,
                                               num_microcells_population))}
        for possible_cell in self._population.cells:
            for possible_microcell in possible_cell.microcells:
                density_microcells_list = microcells_to_choose_dict.values()
                if min(density_microcells_list) < len(
                        possible_microcell.persons):
                    # Remove old object
                    microcells_to_choose_dict.pop(list(
                        microcells_to_choose_dict.keys())[
                        list(microcells_to_choose_dict.values()).index(
                            min(density_microcells_list))])
                    # Add new microcell
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
                selected_household = random.choice(
                    selected_microcell.households)
                selected_household.add_person(person)
            else:
                # Create new household
                selected_microcell.add_household([person])

    def check_leaving_individuals(self, time, person):
        """Check if individuals travel_end_time is reached. If interventions
        are active and travelling individual is in isolation and/or quarantine
        individuals leave after their travel_end_time is reached and they are
        out of isolation and/or quarantine.

        Parameters
        ----------
        time : float
            Simulation time
        Person : Person
            Instance of Person class

        """
        if (hasattr(person, 'travel_end_time')) and \
                (time > person.travel_end_time):
            if all([hasattr(person, 'isolation_start_time'),
                    hasattr(person, 'quarantine_start_time')]):
                if (person.isolation_start_time is None and
                        person.quarantine_start_time is None) or \
                        (person.isolation_start_time <= time and
                         person.quarantine_start_time <= time):
                    return True
            elif hasattr(person, 'isolation_start_time'):
                if (person.isolation_start_time is None) or \
                        (person.isolation_start_time <= time):
                    return True
            elif hasattr(person, 'quarantine_start_time'):
                if (person.quarantine_start_time is None) or \
                        (person.quarantine_start_time <= time):
                    return True
            else:
                return True
        return False

    def remove_leaving_individuals(self, time):
        """Remove individuals after their travel_end_time is reached
        from cell, microcell and household.

        Parameters
        ----------
        time : float
            Simulation time

        """
        for person in list(reversed(self.travellers)):
            if self.check_leaving_individuals(time, person):
                Person.remove_person(person)
                self.travellers.remove(person)
