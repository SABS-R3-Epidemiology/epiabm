#
# AbstractIntervention Class
#

from pyEpiabm.core import Population


class AbstractIntervention:
    """Abstract class for Interventions.

    """
    def __init__(self, start_time, duration):
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
        self.is_active = False

    def __call__(self, time: float):
        """Run intervention.

        Parameters
        ----------
        time : float
            Current simulation time

        """
        raise NotImplementedError