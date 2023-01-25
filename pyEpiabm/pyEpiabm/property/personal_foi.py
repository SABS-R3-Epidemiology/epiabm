#
# Calculate infectiousness and susceptibility for an individual
#

import pyEpiabm.core
from pyEpiabm.core import Parameters

class PersonalInfection:
    """Class to calculate the infectiousness and susceptibility
    parameters of a :class:`Person`.

    """
    @staticmethod
    def person_inf(infector, time: float):
        """Calculate the infectiousness of a person. Does not
        include interventions such as isolation, or whether individual
        is a carehome resident.

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
        vacc_inf_drop = 1
        if infector.is_vaccinated:
            if time > infector.date_vaccinated + infector.time_to_efficacy:
                vacc_inf_drop *= infector.vacc_inf_drop

        return infector.infectiousness * vacc_inf_drop

    @staticmethod
    def person_susc(infector, infectee, time: float):
        """Calculate the susceptibility of one person to another. Does not
        include interventions such as isolation, or whether individual is a
        carehome resident.

        Also does not yet import WAIFW matrix from Polymod data to determine
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
            Susceptibility parameter of household

        """
        vacc_susc_drop = 1
        if infectee.is_vaccinated:
            if time > infectee.date_vaccinated + infectee.time_to_efficacy:
                vacc_susc_drop *= infectee.vacc_inf_drop  
        
        return 1.0 * vacc_susc_drop
