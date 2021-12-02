#
# Place type Class
#
from enum import Enum


class PlaceType(Enum):
    """Enum representing a place's type."""
    Hotel = 1
    CareHome = 2
    Restaurant = 3
    OutdoorSpace = 4

# Can we add associated lists for infectiousness and susceptibility? So a
# restaurant always has a
# baseline infectiousness of .8 say and thts carried with the object?
