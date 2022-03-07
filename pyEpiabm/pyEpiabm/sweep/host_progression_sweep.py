#
# Progression of infection within individuals
#

import random
import numpy as np

import pyEpiabm as pe
from pyEpiabm.property import InfectionStatus
from pyEpiabm.utility import InverseCdf
from pyEpiabm.utility import TransitionTimeMatrix
from .abstract_sweep import AbstractSweep


class HostProgressionSweep(AbstractSweep):
    """Class for sweeping through population and updating host infection status
    and time to next infection status change.
    """

    def __init__(self):
        """Initialise parameters to be used in class methods. State
        transition matrix is set where each row of the matrix corresponds
        to a current infection status of a person. The columns of that
        row then indicate the transition probabilities for the remaining
        infection statuses. Number of infection states is also set by
        taking the size of the InfectionStatus enum.

        """
        self.state_transition_matrix = \
            pe.Parameters.instance().state_transition_matrix
        self.number_of_states = len(InfectionStatus)
        assert self.state_transition_matrix.shape ==\
            (self.number_of_states, self.number_of_states),\
            'Matrix dimensions must match number of infection states'

    def _update_time_to_status_change(self, person, time):
        """Assigns time until next infection status update,
        given as a random integer between 1 and 10. Used
        for persons with infection statuses that have no transition/
        latent time implemented yet - temporary function.

        Parameters
        ----------
        Person : Person
            Instance with infection status attributes
        time: float
            Current simulation time

        """
        # This is left as a random integer for now but will be made more
        # complex later.
        new_time = random.randint(1, 10)
        new_time = float(new_time)
        person.time_of_status_change = time + new_time

    def _set_latent_time(self, person, time):
        """Calculates latency period as calculated in CovidSim,
        and updates the time_of_status_change for the given
        Person, given as the time until next infection status
        for a person who has been set as exposed.

        Parameters
        ----------
        Person : Person
            Instance with infection status attributes
        time: float
            Current simulation time

        """
        latent_period = pe.Parameters.instance().latent_period
        latent_period_iCDF = pe.Parameters.instance().latent_period_iCDF
        latent_icdf_object = InverseCdf(latent_period, latent_period_iCDF)
        latent_time = latent_icdf_object.icdf_choose_exp()

        assert latent_time >= 0.0, 'Negative latent time'

        person.time_of_status_change = time + latent_time

    def _set_infectiousness(self, person):
        """Assigns the infectiousness of a person for when they go from
        the exposed infection state to the next state, either InfectAsympt,
        InfectMild or InfectGP.
        Called right after an exposed person has been given its
        new infection status in the call method below.

        Parameters
        ----------
        Person : Person
            Instance of person class with infection status attributes

        Returns
        -------
        float
            Infectiousness of a person

        """
        init_infectiousness = np.random.gamma(1, 1)
        if person.infection_status == InfectionStatus.InfectASympt:
            infectiousness = init_infectiousness *\
                             pe.Parameters.instance().asympt_infectiousness
        elif (person.infection_status == InfectionStatus.InfectMild or
              person.infection_status == InfectionStatus.InfectGP):
            infectiousness = init_infectiousness *\
                             pe.Parameters.instance().sympt_infectiousness
        person.infectiousness = infectiousness

    def _update_next_infection_status(self, person):
        """Assigns next infection status based on current infection status
        and on probabilities of transition to different statuses. Weights
        are taken from row in state transition matrix that corresponds to
        the person's current infection status. Weights are then used in
        random.choices method to select person's next infection status.

        Parameters
        ----------
        Person : Person
            Instance of person class with infection status attributes

        """

        row_index = person.infection_status.name
        weights = self.state_transition_matrix.loc[row_index].to_numpy()
        outcomes = range(1, self.number_of_states + 1)

        if len(weights) != len(outcomes):
            raise AssertionError('The number of infection statuses must \
                                match the number of transition probabilities')

        next_infection_status_number = random.choices(outcomes, weights)[0]
        next_infection_status = InfectionStatus(next_infection_status_number)
        person.next_infection_status = next_infection_status

    def _update_time_to_status_change(self, person, time):
        """Assigns time until next infection status update,
         given as a random integer between 1 and 10. Used
         for persons with infection statuses that have no transition/
         latent time implemented yet - temporary function.
        :param Person: Person instance with infection status attributes
        :type Person: Person
        :param time: Current simulation time
        :type time: float
        """
        # This is left as a random integer for now but will be made more
        # complex later.
        new_time = random.randint(1, 10)
        new_time = float(new_time)
        person.time_of_status_change = time + new_time

    def _update_time_status_change(self, person, time):
        """Calculates transition time as calculated in CovidSim,
        and updates the time_of_status_change for the given
        Person, given as the time until next infection status
        for a person who has a new infection status. If it is expected that
        the person will not transition again (for example in Recovered or Dead
        statuses), then the time of status change is set to infinity.

        :param Person: Person class with infection status attributes
        :type Person: Person
        :param time: Current simulation time
        :type time: float
        """
        # SOMETHING WRONG, TESTS FAILING. TO SEE.
        # Gets the parameters that will be used:
        latent_to_symptom_delay =\
            pe.Parameters.instance().latent_to_sympt_delay
        model_time_step = 1 / pe.Parameters.instance().time_steps_per_day
        delay = np.floor(latent_to_symptom_delay / model_time_step)

        # Defines the transition time. If the person will not transition again,
        # the transition time is set to infinity. Else, the transition time is
        # defined using the TransitionTimeMatrix class, with a method choose
        # from the InverseCdf class.
        if (person.infection_status == InfectionStatus.Recovered or
                person.infection_status == InfectionStatus.Dead):
            transition_time = np.inf
        else:
            row_index = person.infection_status.name
            column_index = person.next_infection_status.name
            transition_time_object = TransitionTimeMatrix()
            transition_time_matrix =\
                transition_time_object.fill_transition_time()
            transition_time_icdf_object =\
                transition_time_matrix.loc[row_index, column_index]
            transition_time = transition_time_icdf_object.icdf_choose_noexp()

        # Adds delay to transition time for first level symptomatic infection
        # statuses (InfectMild or InfectGP), as is done in CovidSim.
        if (person.infection_status == InfectionStatus.InfectMild or
                person.infection_status == InfectionStatus.InfectGP):
            time = time + delay
        # Assigns the time of status change using current time and transition
        # time:
        person.time_of_status_change = time + transition_time

    def __call__(self, time: float):
        """Sweeps through all people in the population, updates
        their infection status if it is time and assigns them their
        next infection status and the time of their next status change.

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
                    if person.infection_status.name in ['InfectASympt',
                                                        'InfectMild',
                                                        'InfectGP']:
                        self._set_infectiousness(person)
                    if person.infection_status == InfectionStatus.Recovered:
                        person.next_infection_status = None
                    else:
                        self._update_next_infection_status(person)
                    self._update_time_status_change(person, time)
