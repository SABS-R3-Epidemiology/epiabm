#
# Calculate infectiousness and susceptibility for an individual
#


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
        return infector.infectiousness

    @staticmethod
    def person_susc(infector, infectee, time: float):
        """Calculate the susceptibility of one person to another. Does not
        include interventions such as isolation, or whether individual is a
        carehome resident. Also does not yet include age variation, and uses
        default value of unity.

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
        return 1.0
