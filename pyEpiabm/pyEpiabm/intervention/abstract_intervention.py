#
# AbstractIntervention Class
#

from pyEpiabm.core import Population


class AbstractIntervention:
    """Abstract class for Interventions.

    """
    def __init__(self, start_time, duration, population):
        """Set the parameters of the interventions

        Parameters
        ----------
        start_time : float
            Start time of intervention
        duration : float
            Duration of the intervention
        is_active : boolean
            Whether intervention is active
        """
        self.start_time = start_time
        self.duration = duration
        self._population = population

    def is_active(time):
        return self.start_time <= time and self.start_time + duration >= time

    def __call__(self, time: float):
        """Run intervention.

        Parameters
        ----------
        time : float
            Current simulation time

        """
        raise NotImplementedError
