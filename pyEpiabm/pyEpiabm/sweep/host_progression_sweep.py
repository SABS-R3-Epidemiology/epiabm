#
# Progression of infection within individuals
#
# from inspect import Parameter
import random
import numpy as np
import pyEpiabm as pe
from pyEpiabm.property import InfectionStatus
from pyEpiabm.utility import InverseCdf

from .abstract_sweep import AbstractSweep


class HostProgressionSweep(AbstractSweep):
    """Class for sweeping through population and updating host infection status
    and time to next infection status change.
    """

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

    def _set_latent_time(self, person, time):
        """Calculates latency period as calculated in CovidSim,
        and updates the time_of_status_change for the given
        Person, given as the time until next infection status
        for a person who has been set as exposed.

        :param Person: Person instance with infection status attributes
        :type Person: Person
        :param time: Current simulation time
        :type time: float
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
        *Needs to be called right after an exposed person has been given its
        new infection status in the sweep*

        :param Person: Person class with infection status attributes
        :type Person: Person
        :return: Infectiousness of a person
        :rtype: float
        """
        init_infectiousness = np.random.gamma(1, 1)
        if person.infection_status == InfectionStatus.InfectASympt:
            infectiousness = init_infectiousness *\
                             pe.Parameters.instance().asympt_infectiousness
        elif (person.infection_status == InfectionStatus.InfectMild or
              person.infection_status == InfectionStatus.InfectGP):
            infectiousness = init_infectiousness *\
                             pe.Parameters.instance().sympt_infectiousness
        return infectiousness

    def _set_next_inf_status_from_exposed(self):
        """Determines the next infection status of a person in the exposed
        infection status. Takes in a person and uses parameters from the
        parameters file for the proportions in each next status.

        :param Person: Person class with infection status attributes
        :type Person: Person
        :return: Next infection status of an 'exposed' person
        :rtype: InfectionStatus
        """
        # We need two random numbers to compare with proportions and assign
        # next infection states.
        rand_number1 = random.random()
        rand_number2 = random.random()
        # We define the parameters that will be used.
        prob_symptomatic = pe.Parameters.instance().prob_symptomatic
        prob_gp = pe.Parameters.instance().prob_gp
        # If the current infection status is exposed, a person can be
        # symptomatic or asymptomatic. If the person is symptomatic, it is
        # either in the mild infection state or in the GP infection state.
        if rand_number1 < prob_symptomatic:
            if rand_number2 < prob_gp:
                next_inf_status = InfectionStatus.InfectGP
            else:
                next_inf_status = InfectionStatus.InfectMild
        else:
            next_inf_status = InfectionStatus.InfectASympt
        return next_inf_status

    def _set_next_inf_status_from_gp(self):
        """Determines the next infection status of a person in the infected GP
        infection status. Takes in a person and uses parameters from the
        parameters file for the proportions in each next status.

        :param Person: Person class with infection status attributes
        :type Person: Person
        :return: Next infection status of a person with current infection
        status InfectGP
        :rtype: InfectionStatus
        """
        rand_number1 = random.random()
        rand_number2 = random.random()
        prob_gp_to_hosp = pe.Parameters.instance().prob_gp_to_hosp
        mortality_prob_gp = pe.Parameters.instance().mortality_prob_gp
        # If the current infection status is InfectGP, a person can be move
        # from there to be InfectHosp (gets worse), can die before going to
        # the hospital, or can recover.
        if rand_number1 < prob_gp_to_hosp:
            next_inf_status = InfectionStatus.InfectHosp
        elif rand_number2 < mortality_prob_gp:
            next_inf_status = InfectionStatus.Dead
        else:
            next_inf_status = InfectionStatus.Recovered
        return next_inf_status

    def _set_next_inf_status_from_hosp(self):
        """Determines the next infection status of a person in the infected hospital
        infection status. Takes in a person and uses parameters from the
        parameters file for the proportions in each next status.

        :param Person: Person class with infection status attributes
        :type Person: Person
        :return: Next infection status of a person with current infection
        status InfectHosp
        :rtype: InfectionStatus
        """
        rand_number1 = random.random()
        rand_number2 = random.random()
        prob_hosp_to_icu = pe.Parameters.instance().prob_hosp_to_icu
        mortality_prob_icu = pe.Parameters.instance().mortality_prob_icu
        # If the current infection status is InfectHosp, a person can be move
        # from there to be InfectICU (gets worse), can die before going to
        # the ICU, or can recover.
        if rand_number1 < prob_hosp_to_icu:
            next_inf_status = InfectionStatus.InfectICU
        elif rand_number2 < mortality_prob_icu:
            next_inf_status = InfectionStatus.Dead
        else:
            next_inf_status = InfectionStatus.Recovered
        return next_inf_status

    def _set_next_inf_status_from_icu(self):
        """Determines the next infection status of a person in the ICU
        infection status. Takes in a person and uses parameters from the
        parameters file for the proportions in each next status.

        :param Person: Person class with infection status attributes
        :type Person: Person
        :return: Next infection status of a person with current infection
        status InfectICU
        :rtype: InfectionStatus
        """
        rand_number = random.random()
        mortality_prob_icu = pe.Parameters.instance().mortality_prob_icu
        # If the current infection status is InfectICU, a person can either die
        # or recover. If the person recovers, they move to the infection status
        # InfectedICURecov and will eventually recover.
        if rand_number < mortality_prob_icu:
            next_inf_status = InfectionStatus.Dead
        else:
            next_inf_status = InfectionStatus.InfectICURecov
        return next_inf_status

    def _update_next_infection_status(self, person):
        """Assigns next infection status based on current infection status
        and on probabilities of outcome.

        :param Person: Person class with infection status attributes
        :type Person: Person
        """
        # If the current infection state of the person is mild or asymptomatic,
        # the person's next infection state is recovered.
        if person.infection_status == InfectionStatus.Exposed:
            person.next_infection_status = \
                self._set_next_inf_status_from_exposed()
        elif person.infection_status == InfectionStatus.InfectASympt:
            person.next_infection_status = InfectionStatus.Recovered
        elif person.infection_status == InfectionStatus.InfectMild:
            person.next_infection_status = InfectionStatus.Recovered
        elif person.infection_status == InfectionStatus.InfectGP:
            person.next_infection_status = \
                self._set_next_inf_status_from_gp()
        elif person.infection_status == InfectionStatus.InfectHosp:
            person.next_infection_status = \
                self._set_next_inf_status_from_hosp()
        elif person.infection_status == InfectionStatus.InfectICU:
            person.next_infection_status = \
                self._set_next_inf_status_from_icu()
        elif person.infection_status == InfectionStatus.InfectICURecov:
            person.next_infection_status = InfectionStatus.Recovered
        else:
            raise TypeError('update_next_infection_status should only ' +
                            'be applied to individuals with mild ' +
                            'infection status, or exposed')

    def __call__(self, time: float):
        """Sweeps through all people in the population, updates
        their infection status if it is time and assigns them their
        next infection status and the time of their next status change.

        :param time: Current simulation time
        :type time: float
        """

        for cell in self._population.cells:
            for person in cell.persons:
                if person.time_of_status_change is None:
                    assert person.infection_status \
                                    in [InfectionStatus.Susceptible]
                    continue  # pragma: no cover
                while person.time_of_status_change <= time:
                    person.update_status(person.next_infection_status)
                    if person.infection_status == InfectionStatus.Recovered:
                        person.next_infection_status = None
                        person.time_of_status_change = np.inf
                    else:
                        self._update_next_infection_status(person)
                        if person.infection_status == InfectionStatus.Exposed:
                            self._set_latent_time(person, time)
                        else:
                            self._update_time_to_status_change(person, time)
