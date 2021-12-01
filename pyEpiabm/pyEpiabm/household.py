#
# Household Class
#
import typing


class Household:
    """Class representing a household.
    """
    def __init__(self, loc: typing.Tuple[float, float],
                 susceptibility=0, infectiveness=0):
        """Constructor Method.

        :param loc: Location of household.
        :type loc: Tuple[float, float]
        :param susceptibility: Household's
        """
        self.persons = []
        self.location = loc
        self.susceptibility = susceptibility
        self.infectiveness = infectiveness

    def __repr__(self):
        """String representation.

        :return: String representation of the household
        :rtype: str
        """
        return "Household at " \
            + f"({self.location[0]:.2f}, {self.location[1]:.2f}) "\
            + f"with {len(self.persons)} persons."
