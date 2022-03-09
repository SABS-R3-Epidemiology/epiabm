#
# Calculate household force of infection based on Covidsim code
#

from pyEpiabm.core import Person


class HouseholdInfection:
    """Class to calculate the infectiousness and susceptibility
    parameters for the force of infection parameter, within households.

    """
    @staticmethod
    def household_inf(infector: Person, time: float):
        """Calculate the infectiousness of a household.

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
        return 0.1

    @staticmethod
    def household_susc(infector: Person, infectee: Person, time: float):
        """Calculate the susceptibility of a household.

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
        return 0.1

    @staticmethod
    def household_foi(infector: Person, infectee: Person, time: float):
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
        infectiousness = HouseholdInfection.household_inf(infector, time)
        susceptibility = HouseholdInfection.household_susc(infector, infectee,
                                                           time)
        return (infectiousness * susceptibility)
