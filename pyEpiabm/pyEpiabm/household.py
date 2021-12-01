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
        self.people = []
        self.location = loc
        self.susceptibility = susceptibility
        self.infectiveness = infectiveness

    def __repr__(self):
        """String representation.

        :return: String representation of the household
        :rtype: str
        """
        return f"Household at "\
            "({self.location[0]:.2f}, {self.location[1]:.2f}) "\
            "with {len(self.people)} people."
