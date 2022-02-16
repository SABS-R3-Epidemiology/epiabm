#
# Calculate place force of infection based on Covidsim code
#

from pyEpiabm.core import Person, Place


class PlaceInfection:
    """Class to calculate the infectiousness and susceptibility
    parameters for the force of infection parameter, within places.
    """

    @staticmethod
    def place_susc(place: Place, infector: Person, infectee: Person,
                   timestep: int):
        """Calculate the susceptibility of a place.

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
        return 0.2

    @staticmethod
    def place_inf(place: Place, timestep: int):
        """Calculate the infectiousness of a place.
        Not dependent on the people in it.

        :param place: Place
        :type place: Place
        :param timestep: Current simulation timestep
        :type timestep: int
        :return: Infectiousness parameter of place
        :rtype: float
        """
        return 0.5

    @staticmethod
    def place_foi(place: Place, infector: Person, infectee: Person,
                  timestep: int):
        """Calculate the force of infection of a place, for a particular
        infector and infectee.

        :param infector: Infector
        :type infector: Person
        :param infectee: Infectee
        :type infectee: Person
        :param place: Place
        :type place: Place
        :param timestep: Current simulation timestep
        :type timestep: int
        :return: Force of infection parameter of place
        :rtype: float
        """
        infectiousness = PlaceInfection.place_inf(place, timestep)
        susceptibility = PlaceInfection.place_susc(place, infector, infectee,
                                                   timestep)
        return (infectiousness * susceptibility)
