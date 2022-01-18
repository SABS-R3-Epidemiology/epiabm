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
