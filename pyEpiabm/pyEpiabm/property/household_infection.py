#
# Calculate household force of infection based on Covidsim code
#

from pyEpiabm.core import Parameters

from .personal_infection import PersonalInfection


class HouseholdInfection:
    """Class to calculate the infectiousness and susceptibility
    parameters for the force of infection parameter, within households.

    """
    @staticmethod
    def household_inf(infector, timestep: int):
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
        return PersonalInfection.person_inf(infector)

    @staticmethod
    def household_susc(infector, infectee, timestep: int):
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
        return PersonalInfection.person_calc(infector, infectee)

    @staticmethod
    def household_foi(infector, infectee, time: int):
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
        seasonality = 1.0  # Not yet implemeted
        false_pos = 1 / (1 - Parameters.instance().false_positive_rate)
        infectiousness = (HouseholdInfection.household_inf(infector, time)
                          * seasonality * false_pos
                          * Parameters.instance().household_transmission)

        susceptibility = HouseholdInfection.household_susc(infector, infectee,
                                                           time)
        return (infectiousness * susceptibility)
