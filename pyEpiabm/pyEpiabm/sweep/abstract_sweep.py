#
# AbstractSweep Class
#
from pyEpiabm.core import Population


class AbstractSweep:
    """Abstract class for Population Sweeps.
    """
    def bind_population(self, population: Population):
        """Set the population which the sweep will act on.

        :param population: Population: :class:`Population` to bind
        :type population: Population
        """
        # Possibly add check to see if self._population has already been set
        self._population = population

    def __call__(self, time: float):
        """Run sweep over population.

        :param time: Current simulation time
        :type time: float
        """
        raise NotImplementedError
