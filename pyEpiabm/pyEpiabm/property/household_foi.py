#
# Calculate household force of infection based on Covidsim code
#

import pyEpiabm.core
from pyEpiabm.core import Parameters

from .personal_foi import PersonalInfection


class HouseholdInfection:
    """Class to calculate the infectiousness and susceptibility
    parameters for the force of infection parameter, within households.

    """
    @staticmethod
    def household_inf(infector, time: float):
        """Calculate the infectiousness of a person in a given
        household. Does not include interventions such as isolation,
        or whether individual is a carehome resident.

        Parameters
        ----------
        infector : Person
            Infector
        time : float
            Current simulation time

        Returns
        -------
        float
            Infectiousness parameter of household

        """
        return infector.infectiousness

    @staticmethod
    def household_susc(infector, infectee, time: float):
        """Calculate the susceptibility of one person to another in a given
        household. Does not include interventions such as isolation,
        or whether individual is a carehome resident.

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
            Susceptibility parameter of household

        """
        return PersonalInfection.person_susc(infector, infectee, time)

    @staticmethod
    def household_foi(infector, infectee, time: float):
        """Calculate the force of infection parameter of a household,
        for a particular infector and infectee. Scales infectiousness
        if a person is vaccinated.

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
            Force of infection parameter of household

        """
        seasonality = 1.0  # Not yet implemented
        isolation = infector.microcell.cell.isolation_house_effectiveness \
            if infector.isolation_start_time is not None else 1
        false_pos = 1 / (1 - Parameters.instance().
                         false_positive_rate)
        vacc_inf_drop = 1
        if infector.is_vaccinated:
            vacc_params = Parameters.instance()\
                .intervention_params['vaccine_params']
            if time > (infector.date_vaccinated +
                       vacc_params['time_to_efficacy']):
                vacc_inf_drop *= (1 - vacc_params['vacc_inf_drop'])

        infectiousness = (HouseholdInfection.household_inf(infector, time)
                          * seasonality * false_pos
                          * vacc_inf_drop
                          * pyEpiabm.core.Parameters.instance().
                          household_transmission)

        susceptibility = HouseholdInfection.household_susc(infector, infectee,
                                                           time)
        return (isolation * infectiousness * susceptibility)
