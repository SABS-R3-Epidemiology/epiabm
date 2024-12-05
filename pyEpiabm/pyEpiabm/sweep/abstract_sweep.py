#
# AbstractSweep Class
#

from pyEpiabm.core import Population


class AbstractSweep:
    """Abstract class for Population Sweeps.

    """
    def bind_population(self, population: Population):
        """Set the population which the sweep will act on.

        Parameters
        ----------
        population : Population
            Population: :class:`Population` to bind

        """
        # Possibly add check to see if self._population has already been set
        self._population = population

    def __call__(self, time: float):
        """Run sweep over population.

        Parameters
        ----------
        time : float
            Current simulation time

        """
        raise NotImplementedError

    @staticmethod
    def store_infection_periods(infector, infectee, time):
        """Sets the exposure_period of the infectee (defined as the time
        between the infector having status I and the infectee having status
        E. Also sets stores the infector's latent period within the infectee
        (to be used in calculating the generation time). This is called during
        the daily sweeps.

        Parameters
        ----------
        infector : Person
            Current primary case
        infectee : Person
            Current secondary case
        time : float
            Current simulation time
        """
        inf_to_exposed = (time -
                          infector.infection_start_times[-1])
        infectee.set_exposure_period(inf_to_exposed)
        infectee.set_infector_latent_period(infector.latent_period)
