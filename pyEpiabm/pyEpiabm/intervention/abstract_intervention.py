#
# AbstractIntervention Class
#


class AbstractIntervention:
    """Abstract class for Interventions.

    """
    def __init__(self, start_time, policy_duration, case_threshold,
                 population, **kwargs):
        """Set the parameters of the interventions.

        Parameters
        ----------
        start_time : float
            Start time of intervention
        policy_duration : float
            Duration of the intervention
        case_threshold : float
            Number of cases required to trigger the intervention
        population : Population
            Population: :class:`Population` to bind

        """
        self.start_time = start_time
        self.policy_duration = policy_duration
        self.case_threshold = case_threshold
        self._population = population

    def is_active(self, time, num_cases):
        """Query if the intervention is currently active.

        Parameters
        ----------
        time : float
            Current simulation time
        num_cases : integer
            Number of cases

        Returns
        -------
        bool
            Whether the intervention is currently active

        """
        return (
            self.start_time <= time and
            self.start_time + self.policy_duration >= time and
            self.case_threshold <= num_cases
        )

    def __call__(self, time: float):
        """Run intervention.

        Parameters
        ----------
        time : float
            Current simulation time

        """
        raise NotImplementedError
