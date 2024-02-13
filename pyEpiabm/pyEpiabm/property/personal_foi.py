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
    def person_susc(infector, infectee, time: float):
        """Calculate the susceptibility of one person to another.

        Does not yet import WAIFW matrix from Polymod data to determine
        age dependant contact between individuals.

        Parameters
        ----------
        infector : Person
            Infector
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
        if Parameters.instance().use_waning_immunity:
            params = defaultdict(list,
                                 Parameters.instance().antibody_level_params)
            m = IgGFOIMultiplier(params['igg_peak'], params['igg_half_life'],
                                 params['peak_increase_per_10_years_of_age'],
                                 params[
                                     'half_life_increase_per_10_years_of_age'],
                                 params['days_positive_pcr_to_max_igg'])
            time_since_infection = time - infectee.infection_start_time
            return 1.0 * m(time_since_infection, infectee.age_group)
        else:
            return 1.0
