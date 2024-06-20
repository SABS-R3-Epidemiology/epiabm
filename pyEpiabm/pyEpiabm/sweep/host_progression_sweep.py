#
# Progression of infection within individuals
#
import random
import typing

import numpy as np
from collections import defaultdict

import pyEpiabm as pe
from pyEpiabm.core import Parameters, Person
from pyEpiabm.property import InfectionStatus

from .abstract_sweep import AbstractSweep
from .transition_matrices import StateTransitionMatrix, TransitionTimeMatrix


class HostProgressionSweep(AbstractSweep):
    """Class for sweeping through population and updating host infection status
    and time to next infection status change.

    """

    def __init__(self):
        """Initialise parameters to be used in class methods. State
        transition matrix is set where each row of the matrix corresponds
        to a current infection status of a person. The columns of that
        row then indicate the transition probabilities to the remaining
        infection statuses. Number of infection states is set by
        taking the size of the InfectionStatus enum. Waning transition matrix
        is initialised and adapts the state transition matrix with rate
        multipliers relating to waning immunity which are called from the
        parameters class. Transition time matrix is also initialised and
        associated parameters are called from the parameters class.

        Infectiousness progression defines an array used to scale a person's
        infectiousness and which depends on time since the start of the
        infection, measured in timesteps (following what is done in Covidsim).

        """
        # Instantiate state transition matrix
        use_ages = Parameters.instance().use_ages
        coefficients = defaultdict(int, Parameters.instance()
                                   .host_progression_lists)
        multipliers = defaultdict(list, Parameters.instance()
                                  .rate_multiplier_params)
        matrix_object = StateTransitionMatrix(coefficients, multipliers,
                                              use_ages)
        self.state_transition_matrix = matrix_object.matrix
        if pe.Parameters.instance().use_waning_immunity:
            self.waning_transition_matrix = matrix_object.waning_matrix

        self.number_of_states = len(InfectionStatus)
        assert self.state_transition_matrix.shape == \
               (self.number_of_states, self.number_of_states), \
               'Matrix dimensions must match number of infection states'

        # Instantiate transmission time matrix
        time_matrix_object = TransitionTimeMatrix()
        self.transition_time_matrix = \
            time_matrix_object.create_transition_time_matrix()
        # Instantiate parameters to be used in update transition time
        # method
        self.latent_to_symptom_delay = \
            pe.Parameters.instance().latent_to_sympt_delay
        # Defining the length of the model time step (in days, can be a
        # fraction of day as well).
        self.model_time_step = 1 / pe.Parameters.instance().time_steps_per_day
        self.delay = np.floor(self.latent_to_symptom_delay /
                              self.model_time_step)

        # Infectiousness progression
        # Instantiate parameters to be used in update infectiousness
        infectious_profile = pe.Parameters.instance().infectiousness_prof
        inf_prof_resolution = len(infectious_profile) - 1
        inf_prof_average = np.average(infectious_profile)
        infectious_period = pe.Parameters.instance().asympt_infect_period
        # Extreme case where model time step would be too small
        max_inf_steps = 2550
        # Define number of time steps a person is infectious:
        num_infectious_ts = \
            int(np.ceil(infectious_period / self.model_time_step))
        if num_infectious_ts >= max_inf_steps:
            raise ValueError('Number of timesteps in infectious period exceeds'
                             + ' limit')
        # Initialisation
        infectious_profile[inf_prof_resolution] = 0
        infectiousness_prog = np.zeros(max_inf_steps)
        # Fill infectiousness progression array by doing linear interpolation
        # of infectious_profile
        for i in range(num_infectious_ts):
            t = (((i * self.model_time_step) / infectious_period)
                 * inf_prof_resolution)
            # Infectiousness value associated to infectiousness profile:
            associated_inf_value = int(np.floor(t))
            t -= associated_inf_value
            if associated_inf_value < inf_prof_resolution:
                infectiousness_prog[i] = \
                    (infectious_profile[associated_inf_value] * (1 - t)
                     + infectious_profile[associated_inf_value + 1] * t)
            else:  # limit case where we define infectiousness to 0
                infectiousness_prog[i] = \
                    infectious_profile[inf_prof_resolution]
        # Scaling
        scaling_param = inf_prof_average
        for i in range(num_infectious_ts + 1):
            infectiousness_prog[i] /= scaling_param
        self.infectiousness_progression = infectiousness_prog

    @staticmethod
    def set_infectiousness(person: Person, time: float):
        """Assigns the initial infectiousness of a person for when they go from
        the exposed infection state to the next state, either InfectAsympt,
        InfectMild or InfectGP. Also assigns the infection start time and
        stores it as an attribute of the person.

        Called right after an exposed person has been given its
        new infection status in the call method below.
        This static method is non private as it is also used by the initial
        infected sweep to give new infected individuals an infectiousness.

        Parameters
        ----------
        Person : Person
            Instance of person class with infection status attributes
        time : float
            Current simulation time

        """
        init_infectiousness = np.random.gamma(1, 1)
        if person.infection_status == InfectionStatus.InfectASympt:
            infectiousness = (init_infectiousness *
                              pe.Parameters.instance().asympt_infectiousness)
            person.initial_infectiousness = infectiousness
        elif (person.infection_status == InfectionStatus.InfectMild or
              person.infection_status == InfectionStatus.InfectGP):
            infectiousness = (init_infectiousness *
                              pe.Parameters.instance().sympt_infectiousness)
            person.initial_infectiousness = infectiousness

        # Add new infection start time, increment number of times infected and
        # add a new entry to the secondary_infections_counts list
        person.infection_start_times.append(time)
        person.increment_num_times_infected()
        person.secondary_infections_counts.append(0)
        if person.infection_start_times[-1] < 0:
            raise ValueError('The infection start time cannot be negative')

    def update_next_infection_status(self, person: Person, time: float = None):
        """Assigns next infection status based on current infection status
        and on probabilities of transition to different statuses. Weights
        are taken from row in state transition matrix that corresponds to
        the person's current infection status. Weights are then used in
        random.choices method to select person's next infection status.
        Exception is carehome residents who die with probability=1 if reach ICU
        and probability=1-'carehome_rel_prob_hosp' if reach hospital.

        Parameters
        ----------
        person : Person
            Instance of person class with infection status attributes
        time : float
            Current simulation time (if necessary for the method, default =
            None)

        """
        if person.infection_status in [InfectionStatus.Dead,
                                       InfectionStatus.Vaccinated]:
            person.next_infection_status = None
            return
        elif (person.infection_status == InfectionStatus.Recovered and not
              Parameters.instance().use_waning_immunity):
            person.next_infection_status = None
            return
        elif (person.care_home_resident and
              person.infection_status == InfectionStatus.InfectICU):
            person.next_infection_status = InfectionStatus.Dead
            return
        elif (person.care_home_resident and
              person.infection_status == InfectionStatus.InfectHosp):
            carehome_params = Parameters.instance().carehome_params
            carehome_hosp = carehome_params['carehome_rel_prob_hosp']
            if random.uniform(0, 1) > carehome_hosp:
                person.next_infection_status = InfectionStatus.Dead
                return
        row_index = person.infection_status.name

        # If we are not using waning immunity or person.time_of_recovery is
        # None (so they have never reached Recovered) then we choose weights
        # from the state_transition_matrix. Otherwise, we use the
        # waning_transition_matrix.
        if (not Parameters.instance().use_waning_immunity or
                not person.time_of_recovery):
            weights = self.state_transition_matrix.loc[row_index].to_numpy()
            weights = [w[person.age_group] if isinstance(w, list) else w
                       for w in weights]
        else:
            if time is None:
                raise ValueError("Simulation time must be passed to "
                                 "update_next_infection_status when waning "
                                 "immunity is active")
            weights = self._get_waning_weights(person, time)

        outcomes = range(1, self.number_of_states + 1)
        if len(weights) != len(outcomes):
            raise AssertionError('The number of infection statuses must' +
                                 ' match the number of transition' +
                                 ' probabilities')

        next_infection_status_number = random.choices(outcomes, weights)[0]
        next_infection_status = \
            InfectionStatus(next_infection_status_number)

        person.next_infection_status = next_infection_status

    def _get_waning_weights(self, person: Person, time: float) -> typing.List:
        """Given that the current person has previously recovered, this method
        will return a list of updated weights based on the level of immunity
        the person has. The weights taken from the waning_transition_matrix
        are lambda expressions parameterized by t (time_since_recovery).

        Parameters
        ----------
        person : Person
            Instance of person class with infection status attributes
        time : float
            Current simulation time

        Returns
        -------
        list:
            List of weights representing the probability of transitioning to
            a given compartment.
        """
        row_index = person.infection_status.name
        time_since_recovery = time - person.time_of_recovery
        weights = list(self.waning_transition_matrix.loc[row_index])

        # Note that below, each entry w will be a lambda expression returning
        # a np.array either representing a float (shape = ()) or a list
        # (shape = (n,)) hence the conditions.
        new_weights = []
        for w in weights:
            if isinstance(w, (int, float)):
                new_weights.append(w)
            else:
                # This is evaluating the lambda expressions at t =
                # time_since_recovery
                w_evaluated = w(time_since_recovery)
                if w_evaluated.shape:
                    new_weights.append(w_evaluated[person.age_group])
                else:
                    new_weights.append(w_evaluated)
        return new_weights

    def update_time_status_change(self, person: Person, time: float):
        """Calculates transition time as calculated in CovidSim,
        and updates the time_of_status_change for the given
        Person, given as the time until next infection status
        for a person who has a new infection status. If it is expected that
        the person will not transition again (for example in Recovered or Dead
        statuses), then the time of status change is set to infinity.

        Parameters
        ----------
        person : Person
            Instance of Person class with :class:`InfectionStatus` attributes
        time : float
            Current simulation time

        """
        # Defines the transition time. If the person will not transition again,
        # the transition time is set to infinity. Else, the transition time is
        # defined using the TransitionTimeMatrix class, with the method
        # `choose` from the InverseCdf class.
        if person.infection_status == InfectionStatus.Susceptible:
            raise ValueError("Method should not be used to infect people")

        if person.infection_status in [InfectionStatus.Dead,
                                       InfectionStatus.Vaccinated]:
            transition_time = np.inf
        elif (person.infection_status == InfectionStatus.Recovered and not
              Parameters.instance().use_waning_immunity):
            transition_time = np.inf
        else:
            row_index = person.infection_status.name
            column_index = person.next_infection_status.name
            # Checks for susceptible to exposed case
            # where transition time is zero
            try:
                if person.infection_status != InfectionStatus.Recovered:
                    transition_time_icdf_object = \
                        self.transition_time_matrix.loc[row_index,
                                                        column_index]
                    transition_time = \
                        transition_time_icdf_object.icdf_choose_noexp()
                else:
                    # If someone is recovered, then their transition time
                    # will be equal to 1 when waning immunity is turned on.
                    # This means that everyone spends exactly 1 day in the
                    # Recovered compartment with waning immunity
                    transition_time = 1
            except AttributeError as e:
                if "object has no attribute 'icdf_choose_noexp'" in str(e):
                    transition_time = transition_time_icdf_object
                    assert isinstance(
                        transition_time_icdf_object,
                        (float, int)), \
                        ("Entries of transition time matrix" +
                         " must either be ICDF" + " objects or numbers")
                else:
                    raise

        # Adds delay to transition time for first level symptomatic infection
        # statuses (InfectMild or InfectGP), as is done in CovidSim.
        if person.infection_status in [InfectionStatus.InfectMild,
                                       InfectionStatus.InfectGP]:
            transition_time += self.delay
        # Assigns the time of status change using current time and transition
        # time:
        if transition_time < 0:
            raise ValueError('New transition time must be larger than' +
                             ' or equal to 0')

        person.time_of_status_change = time + transition_time

        # Finally, if the person is Exposed, we can store their latency period
        # as the transition_time. This can be used for calculating the serial
        # interval
        if person.infection_status == InfectionStatus.Exposed:
            latent_period = transition_time
            person.store_serial_interval(latent_period)

    def _updates_infectiousness(self, person: Person, time: float):
        """Updates infectiousness. Scales using the initial infectiousness
        if the person is in an infectious state. Updates the infectiousness to
        0 if the person has just been transferred to Recovered or Dead. Doesn't
        do anything if the person was already in Recovered, Dead, Susceptible,
        or Exposed (ie if the infectiousness of the person was 0).

        Parameters
        ----------
        Person : Person
            Instance of Person class with :class:`InfectionStatus`,
            initial infectiousness, and infection start time attributes
        time : float
            Current simulation time

        """
        # Updates infectiousness with scaling if person is infectious:
        if str(person.infection_status).startswith('InfectionStatus.Infect'):
            scale_infectiousness = self.infectiousness_progression
            time_since_infection = (int((time
                                         - person.infection_start_times[-1])
                                        / self.model_time_step))
            person.infectiousness = person.initial_infectiousness *\
                scale_infectiousness[time_since_infection]
        # Sets infectiousness to 0 if person just became Recovered, Dead, or
        # Vaccinated
        elif person.infectiousness != 0:
            if person.infection_status in [InfectionStatus.Recovered,
                                           InfectionStatus.Dead,
                                           InfectionStatus.Vaccinated]:
                person.infectiousness = 0

    def __call__(self, time: float):
        """Sweeps through all people in the population, updates their
        infection status if it is time and assigns them their next infection
        status and the time of their next status change. Also updates their
        infectiousness.

        Parameters
        ----------
        time : float
            Current simulation time

        """
        # store list of uninfected or asymptomatic people for processing
        # for disease testing.
        asympt_or_uninf_people = []
        for cell in self._population.cells:
            for person in cell.persons:
                if person.time_of_status_change is None:
                    assert person.is_susceptible()
                    asympt_or_uninf_people.append((cell, person))
                    continue  # pragma: no cover
                if person.infection_status in [InfectionStatus.Recovered,
                                               InfectionStatus.Vaccinated]:
                    asympt_or_uninf_people.append((cell, person))
                while person.time_of_status_change <= time:
                    person.update_status(person.next_infection_status)
                    if person.infection_status in \
                        [InfectionStatus.InfectASympt,
                         InfectionStatus.InfectMild,
                         InfectionStatus.InfectGP]:
                        self.set_infectiousness(person, time)
                        if not person.is_symptomatic():
                            asympt_or_uninf_people.append((cell, person))
                    self.update_next_infection_status(person, time)
                    if person.infection_status == InfectionStatus.Susceptible:
                        person.time_of_status_change = None
                        break
                    elif person.infection_status == InfectionStatus.Recovered:
                        person.set_time_of_recovery(time)
                    self.update_time_status_change(person, time)
                    self.sympt_testing_queue(cell, person)
                self._updates_infectiousness(person, time)

        self.asympt_uninf_testing_queue(asympt_or_uninf_people, time)

    def sympt_testing_queue(self, cell, person: Person):
        """ Adds symptomatic people to a testing queue with a given
        probability depedent on their status as either a care home
        resident or a key worker.

        Detailed description of the implementation can be found in github wiki:
        https://github.com/SABS-R3-Epidemiology/epiabm/wiki/Interventions#testing

        Parameters
        ----------
        cell : Cell
            cell for which the person is a member of and therefore
            will be added to the testing queue of.
        person : Person
            symptomatic inndividual to be added to a testing queue.

        """
        if hasattr(Parameters.instance(), 'intervention_params'):
            if 'disease_testing' in Parameters.instance(). \
              intervention_params.keys():
                testing_params = Parameters.instance(). \
                    intervention_params['disease_testing']
                r = random.random()
                type_r = random.random()

                if (person.is_symptomatic() and
                   person.date_positive is None):
                    if person.care_home_resident:
                        test_probability = testing_params['testing_sympt'][0]
                        type_probability = testing_params['sympt_pcr'][0]
                    elif person.key_worker:
                        test_probability = testing_params['testing_sympt'][1]
                        type_probability = testing_params['sympt_pcr'][1]
                    else:
                        test_probability = testing_params['testing_sympt'][2]
                        type_probability = testing_params['sympt_pcr'][2]

                    if r < test_probability:
                        if type_r < type_probability:
                            cell.enqueue_PCR_testing(person)
                        else:
                            cell.enqueue_LFT_testing(person)

                if (person.date_positive is not None and
                    (person.next_infection_status in
                     [InfectionStatus.Dead, InfectionStatus.Recovered])):
                    person.date_positive = None

    def asympt_uninf_testing_queue(self, person_list: list, time):
        """ Adds asymptomatic and uninfected people to a testing queue
        with a given probability depedent on their status as either a care
        home resident or key worker.

        Detailed description of the implementation can be found in github wiki:
        https://github.com/SABS-R3-Epidemiology/epiabm/wiki/Interventions#testing

        Parameters
        ----------
        person_list : list
            list of (cell, person) tuples giving the list of people
            to be added to a testing queue and their cell.
        time : float
            current time point to determine whether uninfected indivuals
            should stop being considered as positive.

        """
        if hasattr(Parameters.instance(), 'intervention_params'):
            if 'disease_testing' in Parameters.instance(). \
              intervention_params.keys():
                testing_params = Parameters.instance(). \
                    intervention_params['disease_testing']
                for item in person_list:
                    cell = item[0]
                    person = item[1]
                    if person.is_symptomatic():
                        raise ValueError("Function should not be called on" +
                                         "symptomatic individuals.")
                    r = random.random()
                    type_r = random.random()

                    if person.care_home_resident:
                        test_probability = testing_params[
                            'testing_asympt_uninf'][0]
                        type_probability = testing_params[
                            'asympt_uninf_pcr'][0]
                    elif person.key_worker:
                        test_probability = testing_params[
                            'testing_asympt_uninf'][1]
                        type_probability = testing_params[
                            'asympt_uninf_pcr'][1]
                    else:
                        test_probability = testing_params[
                            'testing_asympt_uninf'][2]
                        type_probability = testing_params[
                            'asympt_uninf_pcr'][2]

                    if (r < test_probability and
                       person.date_positive is None):
                        if type_r < type_probability:
                            cell.enqueue_PCR_testing(person)
                        else:
                            cell.enqueue_LFT_testing(person)

                    elif (person.date_positive is not None and
                          person.date_positive + 10 >= time):
                        person.date_positive = None
