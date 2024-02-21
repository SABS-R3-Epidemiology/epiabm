#
# Class to produce rate multipliers to be used for waning individuals in the
# StateTransitionMatrix
#

import math
import typing


class RateMultiplier:
    """Class which produces a decaying exponential curve parameterised by time
    given two data points (default of 90 and 180 days). Note that p(t) = 0
    represents immunity having a maximal effect on the StateTransitionMatrix
    probabilities, and p(t) = 1 represents immunity having no effect.
    So p -> 1 as t -> inf. p will take the form p(t) = 1 - be^(-at) for some
    constants a and b (determined by the two data points).
    """
    def __init__(self, p_1: float, p_2: float,
                 t_1: float = 90.0, t_2: float = 180.0):
        """Constructor Method

        Parameters
        ----------
        p_1 : float
            Rate multiplier at t = t_1
        p_2 : float
            Rate multiplier at t = t_2
        t_1 : float
            First time data point (represents a Person's time since last
            recovery in days, default = 90.0)
        t_2 : float
            Second time data point (represents a Person's time since last
            recovery in days, default = 180.0)
        """
        # Parameter checks
        # We assume t_1 is the first value
        if not 0.0 <= t_1 < t_2:
            raise ValueError("t_1 must be smaller than t_2 and both must"
                             "be non-negative")
        # This means that p_1 < p_2 (as this curve will be increasing in t)
        if not 0.0 <= p_1 < p_2 <= 1.0:
            raise ValueError("p_1 must be smaller than p_2 and both must"
                             "lie between 0 and 1 inclusive")

        self.p_1 = p_1
        self.p_2 = p_2
        self.t_1 = t_1
        self.t_2 = t_2
        self.a, self.b = self._calculate_parameters()

    def _calculate_parameters(self) -> typing.Tuple:
        """Given the initial data points p(t_1) = p_1 and p(t_2) = p_2, this
        method determines the parameters a and b of the function.
        Note that p(t) = 1 - be^(-at).

        Returns
        -------
        tuple[float, float]
            The parameters (a, b)

        """
        # If either data point is 1, this means that this curve can only be
        # fit to the flat line p(t) = 1 (representing immunity having no
        # effect on the transition probabilities)
        if self.p_1 == 1.0 or self.p_2 == 1.0:
            return 0.0, 0.0

        a = - math.log((1.0 - self.p_1) / (1.0 - self.p_2)) / (self.t_1 -
                                                               self.t_2)
        b = (1.0 - self.p_1) * math.exp(a * self.t_1)
        return a, b

    def __call__(self, t: float) -> float:
        """Given a value t (representing days since a Person last recovered
        from the disease), calculates the rate multiplier for a waning
        individual moving to a specific compartment, using a decaying
        exponential

        Parameters
        ----------
        t : float
            Days since a Person last recovered from the disease

        Returns
        -------
        float
            The rate multiplier for the probability of them moving to
            a certain compartment in the StateTransitionMatrix
        """
        # Check for erroneous values
        if t < 0.0:
            raise ValueError("t must be non-negative")

        # If b = 0 (representing no effect from waning immunity) we return a
        # rate multiplier of 1. We check for a as well to avoid division by
        # zero (a should never be zero unless b is zero)
        if self.a == 0.0 or self.b == 0.0:
            return 1.0

        # If b > 1, then a section of the curve p(t) = 1 - be^(-at) will be
        # negative for some positive values of t. Hence, we will simply set
        # p = 0 for these values of t
        if t < math.log(self.b) / self.a:
            return 0.0

        return 1.0 - self.b * math.exp(-self.a * t)
