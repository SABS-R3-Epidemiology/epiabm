#
# Helper functions based on Covidsim code
#
from .person import Person


class CovidsimHelpers:
    """Class to create helper functions from Covidsim code to aid
    comparison to Covidsim.
    """

    @staticmethod
    def calc_house_inf(infector: Person, timestep: int):
        """Calculate the infectiveness of a household.

        :param infector: Infector
        :type infector: Person
        :param timestep: Current simulation timestep
        :type timestep: int
        :return: Infectiveness parameter of household
        :rtype: float
        """
        return 1.0

    @staticmethod
    def calc_house_susc(infector: Person, infectee: Person, timestep: int):
        """Calculate the susceptibility of a household.

        :param infector: Infector
        :type infector: Person
        :param infectee: Infectee
        :type infectee: Person
        :param timestep: Current simulation timestep
        :type timestep: int
        :return: Susceptibility parameter of household
        :rtype: float
        """
        return CovidsimHelpers.calc_person_susc(infector, infectee, timestep)

    @staticmethod
    def calc_person_susc(infector: Person, infectee: Person, timestep: int):
        """Calculate the susceptibility of a person.

        :param infector: Infector
        :type infector: Person
        :param infectee: Infectee
        :type infectee: Person
        :param timestep: Current simulation timestep
        :type timestep: int
        :return: Susceptibility parameter of person
        :rtype: float
        """
        return 1.0
