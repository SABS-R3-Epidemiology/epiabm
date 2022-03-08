#
# Place type Class
#

from enum import Enum


class PlaceType(Enum):
    """Enum representing a place"s type.

    """
    Hotel = 1  # specific to travelling persons
    CareHome = 2  # two groups, workers [0] and residents [1], both remain
    # unchanged, but interact differently.
    Restaurant = 3  # two groups, workers [0] and visitors [1], workers remain
    # unchanged, visitors updated on each timestep
    OutdoorSpace = 4  # one group, updated each timestep
    Workplace = 5  # multiple groups represent different groups within the
    # company, all remain unchanged.
