#
# Routine subpackage of the pyEpiabm module.
#

""" pyEpiabm.routine provides various methods to act upon or
create a population.

It includes many infection methods for houses, places and other spatial cells,
characterised by a force of infection exerted by each infected person.
This includes infectiousness and susceptibility components.

Infectiousness is (broadly) a function of 1 person (their age, places,
number of people in their household etc).
Susceptibility is (broadly) a function of 2 people (a person's susceptibility
to another person / potential infector).

"""

from .abstract_population_config import AbstractPopulationFactory
from .file_population_config import FilePopulationFactory
from .household_infection import HouseholdInfection
from .place_infection import PlaceInfection
from .spatial_infection import SpatialInfection
from .simulation import Simulation
from .toy_population_config import ToyPopulationFactory
