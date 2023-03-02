#
# Progression of infection within individuals
#

import random
import numpy as np
from collections import defaultdict

import pyEpiabm as pe
from pyEpiabm.core import Parameters, Person
from pyEpiabm.property import InfectionStatus
from pyEpiabm.utility import StateTransitionMatrix, TransitionTimeMatrix

from .abstract_sweep import AbstractSweep


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
        taking the size of the InfectionStatus enum. Transition time matrix
        is also initialised and associated parameters are called from the
        parameters class.

        Infectiousness progression defines an array used to scale a person's
        infectiousness and which depends on time since the start of the
        infection, measured in timesteps (following what is done in Covidsim).

        """
        # Instantiate state transition matrix
        use_ages = Parameters.instance().use_ages
        coefficients = defaultdict(int, Parameters.instance()
                                   .host_progression_lists)
        matrix_object = StateTransitionMatrix(coefficients, use_ages)
        self.state_transition_matrix = matrix_object.matrix

        self.number_of_states = len(InfectionStatus)
        assert self.state_transition_matrix.shape == \
            (self.number_of_states, self.number_of_states),\
            'Matrix dimensions must match number of infection states'

        # Instantiate transmission time matrix
        time_matrix_object = TransitionTimeMatrix()
        self.transition_time_matrix =\
            time_matrix_object.create_transition_time_matrix()
        # Instantiate parameters to be used in update transition time
        # method
        self.latent_to_symptom_delay =\
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
        num_infectious_ts =\
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
                infectiousness_prog[i] =\
                    (infectious_profile[associated_inf_value] * (1 - t)
                     + infectious_profile[associated_inf_value + 1] * t)
            else:  # limit case where we define infectiousness to 0
                infectiousness_prog[i] =\
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
        person.infection_start_time = time
        if person.infection_start_time < 0:
            raise ValueError('The infection start time cannot be negative')

    def update_next_infection_status(self, person: Person):
        """Assigns next infection status based on current infection status
        and on probabilities of transition to different statuses. Weights
        are taken from row in state transition matrix that corresponds to
        the person's current infection status. Weights are then used in
        random.choices method to select person's next infection status.
        Exception is carehome residents who die with probability=1 if reach ICU
        and probability=1-'carehome_rel_prob_hosp' if reach hospital.

        Parameters
        ----------
        Person : Person
            Instance of person class with infection status attributes

        """
        if person.infection_status in [InfectionStatus.Recovered,
                                       InfectionStatus.Dead]:
            person.next_infection_status = None
        elif (person.care_home_resident and
              person.infection_status == InfectionStatus.InfectICU):
            person.next_infection_status = InfectionStatus.Dead
        elif (person.care_home_resident and
              person.infection_status == InfectionStatus.InfectHosp):
            carehome_params = Parameters.instance().carehome_params
            carehome_hosp = carehome_params['carehome_rel_prob_hosp']
            if random.uniform(0, 1) > carehome_hosp:
                person.next_infection_status = InfectionStatus.Dead
        else:
            row_index = person.infection_status.name
            weights = self.state_transition_matrix.loc[row_index].to_numpy()
            weights = [w[person.age_group] if isinstance(w, list) else w
                       for w in weights]
            outcomes = range(1, self.number_of_states + 1)

            if len(weights) != len(outcomes):
                raise AssertionError('The number of infection statuses must' +
                                     ' match the number of transition' +
                                     ' probabilities')

            next_infection_status_number = random.choices(outcomes, weights)[0]
            next_infection_status =\
                InfectionStatus(next_infection_status_number)
            person.next_infection_status = next_infection_status

    def update_time_status_change(self, person: Person, time: float):
        """Calculates transition time as calculated in CovidSim,
        and updates the time_of_status_change for the given
        Person, given as the time until next infection status
        for a person who has a new infection status. If it is expected that
        the person will not transition again (for example in Recovered or Dead
        statuses), then the time of status change is set to infinity.

        Parameters
        ----------
        Person : Person
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

        if person.infection_status in [InfectionStatus.Recovered,
                                       InfectionStatus.Dead]:
            transition_time = np.inf
        else:
            row_index = person.infection_status.name
            column_index = person.next_infection_status.name
            transition_time_icdf_object =\
                self.transition_time_matrix.loc[row_index, column_index]
            # Checks for susceptible to exposed case
            # where transition time is zero
            try:
                transition_time =\
                    transition_time_icdf_object.icdf_choose_noexp()
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
            transition_time += HostProgressionSweep().delay
        # Assigns the time of status change using current time and transition
        # time:
        if transition_time < 0:
            raise ValueError('New transition time must be larger than' +
                             ' or equal to 0')

        person.time_of_status_change = time + transition_time

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
            time_since_infection = (int((time - person.infection_start_time)
                                        / self.model_time_step))
            person.infectiousness = person.initial_infectiousness *\
                scale_infectiousness[time_since_infection]
        # Sets infectiousness to 0 if person just became Recovered or Dead, and
        # sets its infection start time to None again.
        elif person.infectiousness != 0:
            if person.infection_status in [InfectionStatus.Recovered,
                                           InfectionStatus.Dead]:
                person.infectiousness = 0
                person.infection_start_time = None

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
        for cell in self._population.cells:
            for person in cell.persons:
                if person.time_of_status_change is None:
                    assert person.infection_status \
                                    in [InfectionStatus.Susceptible]
                    continue  # pragma: no cover
                while person.time_of_status_change <= time:
                    person.update_status(person.next_infection_status)
                    if person.infection_status in \
                            [InfectionStatus.InfectASympt,
                             InfectionStatus.InfectMild,
                             InfectionStatus.InfectGP]:
                        self.set_infectiousness(person, time)
                    self.update_next_infection_status(person)
                    self.update_time_status_change(person, time)
                self._updates_infectiousness(person, time)
