#
# Calculate infectiousness and susceptibility for an individual
#

from pyEpiabm.core import Parameters


class PersonalInfection:
    """Class to calculate the infectiousness and susceptibility
    parameters of a :class:`Person`.

    """
    @staticmethod
    def person_inf(infector, time: float):
        """Calculate the infectiousness of a person. Does not
        include interventions such as isolation, or whether individual
        is a carehome resident. Scales infectiousness if a person is
        vaccinated.

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

        return 1.0
