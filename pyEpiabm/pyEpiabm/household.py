#
# Household Class
#
import typing


class Household:
    """Class representing a household,
    a group of people (family or otherwise) who live
    together and share living spaces. This group will
    have a combined susceptability and infectiousness
    different to that of the individuals.
    """
    def __init__(self, loc: typing.Tuple[float, float],
                 susceptibility=0, infectiveness=0):
        """Constructor Method.

        :param loc: Location of household.
        :type loc: Tuple[float, float]
        :param susceptibility: Household's base susceptibility
            to infection events.
        :type susceptibility: float
        :param infectiveness: Household's base infectiveness.
        :type infectiveness: float
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
