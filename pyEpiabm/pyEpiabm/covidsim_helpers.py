#
# Helper functions based on Covidsim code
#
from .person import Person
from .place import Place


class CovidsimHelpers:
    """Class to create helper functions from Covidsim code to aid
    comparison to Covidsim.

    # Most of the volume of covidsim code is adapting these susceptibility
    # infectiousness parameters, especially for the place infections.
    # May need to make this a more general class.
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
        return 0.1

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
        return .1

    @staticmethod
    def calc_place_susc(place: Place, infector: Person, infectee: Person,
                        timestep: int):
        """Calculate the susceptibility of a person.

        :param infector: Infector
        :type infector: Person
        :param infectee: Infectee
        :type infectee: Person
        :param place: Place
        :type place: Place
        :param timestep: Current simulation timestep
        :type timestep: int
        :return: Susceptibility parameter of place
        :rtype: float
        """
        return .2

    @staticmethod
    def calc_place_inf(place: Place, infector: Person, infectee: Person,
                       timestep: int):
        """Calculate the susceptibility of a person.

        :param place: Place
        :type place: Place
        :param infector: Infector
        :type infector: Person
        :param infectee: Infectee
        :type infectee: Person
        :param timestep: Current simulation timestep
        :type timestep: int

        :return: infectiousness
        :rtype: float
        """
        return 0.5
