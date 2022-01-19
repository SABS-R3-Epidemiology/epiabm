#
# Root of the pyEpiabm module.
# Provides access to all shared functionality (classes, simulation, etc.).
#

"""pyEpiabm is the python backend for epiabm - an Epidemiological
Agent Based Modelling software package.
It contains functionality for setting up a population, and tracking the
evolution of a virus across it, with various visualisation methods.
"""


from . import core
from . import output
from . import property
from . import routine
from . import sweep

# Expose modules in core within pyEpiabm namespace

from .core._compartment_counter import _CompartmentCounter
from .core.cell import Cell
from .core.household import Household
from .core.microcell import Microcell
from .core.parameters import Parameters
from .core.person import Person
from .core.place import Place
from .core.population import Population
