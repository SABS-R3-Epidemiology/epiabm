from enum import Enum


class InfectionStatus(Enum):
    """Enum representing a person's current infection status.
    """
    Susceptible = 1
    Exposed = 2
    InfectASympt = 3
    InfectMild = 4
    InfectGP = 5
    InfectHosp = 6
    InfectICU = 7
    InfectICURecov = 8
    Recovered = 9
    Dead = 10
