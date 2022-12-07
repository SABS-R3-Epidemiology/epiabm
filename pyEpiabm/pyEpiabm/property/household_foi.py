#
# Calculate household force of infection based on Covidsim code
#

import pyEpiabm.core

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
        return PersonalInfection.person_inf(infector, time)

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
        for a particular infector and infectee.

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
        # false_pos = 1 / (1 - pyEpiabm.core.Parameters.instance().
        #                 false_positive_rate)
        true_pos = 1 - pyEpiabm.core.Parameters.instance().false_positive_rate

        # infectiousness = (HouseholdInfection.household_inf(infector, time)
        #                  * seasonality * false_pos
        #                  * pyEpiabm.core.Parameters.instance().
        #                  household_transmission)
        infectiousness = (HouseholdInfection.household_inf(infector, time)
                          * seasonality * true_pos
                          * pyEpiabm.core.Parameters.instance().
                          household_transmission)

        susceptibility = HouseholdInfection.household_susc(infector, infectee,
                                                           time)
        return (infectiousness * susceptibility)
