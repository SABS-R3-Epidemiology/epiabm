#
# Place type Class
#

from enum import Enum


class PlaceType(Enum):
    """Enum representing a place's type.

    """
    PrimarySchool = 1
    SecondarySchool = 2
    SixthForm = 3
    Workplace = 4  # multiple groups represent different groups within the
    # company, all remain unchanged.
    CareHome = 5  # two groups, workers [0] and residents [1], both remain
    # unchanged, but interact differently.
    OutdoorSpace = 6  # one group, updated each timestep
