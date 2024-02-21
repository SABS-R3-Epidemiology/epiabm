#
# Calculate infectiousness and susceptibility for an individual
#
from collections import defaultdict

from pyEpiabm.core import Parameters
from pyEpiabm.utility import IgGFOIMultiplier


class PersonalInfection:
    """Class to calculate the infectiousness and susceptibility
    parameters of a :class:`Person`.

    """
    @staticmethod
    def person_inf(infector, time: float):
        """Calculate the infectiousness of a person.

        Parameters
        ----------
        infector : Person
            Infector
        time: float
            Current simulation time

        Returns
        -------
        float
            Infectiousness parameter of person

        """
        infector_inf = infector.infectiousness
        if infector.is_vaccinated:
            params = Parameters.instance().\
                intervention_params['vaccine_params']
            if time > (infector.date_vaccinated + params['time_to_efficacy']):
                infector_inf *= (1 - params['vacc_inf_drop'])

        return infector_inf

    @staticmethod
    def person_susc(infectee, time: float):
        """Calculate the susceptibility of one person to another.

        Does not yet import WAIFW matrix from Polymod data to determine
        age dependant contact between individuals.

        Parameters
        ----------
        infectee : Person
            Infectee
        time : float
            Current simulation time

        Returns
        -------
        float
            Susceptibility parameter of person

        """
        # If we are using waning immunity then we use a multiplier from
        # igg_foi_multiplier. Otherwise, we set the susceptibility to 1.0.
        if Parameters.instance().use_waning_immunity and\
                (infectee.num_times_infected >= 1):
            params = defaultdict(int,
                                 Parameters.instance().antibody_level_params)
            if not hasattr(PersonalInfection, 'm'):
                PersonalInfection.m =\
                    IgGFOIMultiplier(params['igg_peak_at_age_41'],
                                     params['igg_half_life_at_age_41'],
                                     params['peak_change_per_10_yrs_age'],
                                     params['half_life_change_per_10_yrs_age'],
                                     params['days_positive_pcr_to_max_igg'])
            time_since_infection = time - infectee.infection_start_time
            return 1.0 * PersonalInfection.m(time_since_infection,
                                             infectee.age_group)
        else:
            return 1.0
