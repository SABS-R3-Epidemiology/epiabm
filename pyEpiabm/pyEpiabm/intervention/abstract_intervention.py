#
# AbstractIntervention Class
#

from pyEpiabm.core import Population


class AbstractIntervention:
    """Abstract class for Interventions.

    """
    def __init__(self, start_time, policy_duration, population):
        """Set the parameters of the interventions

        Parameters
        ----------
        start_time : float
            Start time of intervention
        policy_duration : float
            Duration of the intervention
        is_active : boolean
            Whether intervention is active
        """
        self.start_time = start_time
        self.policy_duration = policy_duration
        self._population = population

    def is_active(self, time):
        return self.start_time <= time and self.start_time + self.policy_duration >= time

    def __call__(self, time: float):
        """Run intervention.

        Parameters
        ----------
        time : float
            Current simulation time

        """
        raise NotImplementedError
