#
# Calculate household force of infection based on Covidsim code
#

from pyEpiabm.core import Person


class HouseholdInfection:
    """Class to calculate the infectiousness and susceptibility
    parameters for the force of infection parameter, within households.

    """
    @staticmethod
    def household_inf(infector: Person, timestep: int):
        """Calculate the infectiousness of a household.

        Parameters
        ----------
        infector : Person
            Infector
        timestep : int
            Current simulation timestep

        Returns
        -------
        float
            Infectiousness parameter of household

        """
        return 0.1

    @staticmethod
    def household_susc(infector: Person, infectee: Person, timestep: int):
        """Calculate the susceptibility of a household.

        Parameters
        ----------
        infector : Person
            Infector
        infectee : Person
            Infectee
        timestep : int
            Current simulation timestep

        Returns
        -------
        float
            Susceptibility parameter of household

        """
        return 0.1

    @staticmethod
    def household_foi(infector: Person, infectee: Person, timestep: int):
        """Calculate the force of infection parameter of a household,
        for a particular infector and infectee.

        Parameters
        ----------
        infector : Person
            Infector
        infectee : Person
            Infectee
        timestep : int
            Current simulation timestep

        Returns
        -------
        float
            Force of infection parameter of household

        """
        infectiousness = HouseholdInfection.household_inf(infector, timestep)
        susceptibility = HouseholdInfection.household_susc(infector, infectee,
                                                           timestep)
        return (infectiousness * susceptibility)