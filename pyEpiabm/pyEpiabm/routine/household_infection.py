#
# Calculate household force of infection based on Covidsim code
#

from pyEpiabm.core import Parameters, Person


class HouseholdInfection:
    """Class to calculate the infectiousness and susceptibility
    parameters for the force of infection parameter, within households.

    """
    @staticmethod
    def household_inf(infector: Person, timestep: int):
        """Calculate the infectiousness of a person in a given
        household. Does not include interventions such as isolation,
        or whether individual is a carehome resident.

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
        return Person.infectiousness

    @staticmethod
    def household_susc(infector: Person, infectee: Person, timestep: int):
        """Calculate the susceptibility of one person to another in a given
        household. Does not include interventions such as isolation,
        or whether individual is a carehome resident.

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
        return personal_susc(infector: Person, infectee: Person, timestep: int)  # Not yet implemented

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
        seasonality = 1.0  # Not yet implemeted
        false_pos = 1 / (1 - Parameters.instance().false_positive_rate)
        infectiousness = (HouseholdInfection.household_inf(infector, timestep)
                          * seasonality * false_pos
                          * Parameters.instance.household_transmission)

        susceptibility = HouseholdInfection.household_susc(infector, infectee,
                                                           timestep)
        return (infectiousness * susceptibility)
