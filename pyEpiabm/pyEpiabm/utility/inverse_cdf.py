#
# Class of inverse CDF as is done in Covidsim code.
#

import random
import pyEpiabm as pe
import math
import numpy as np


class InverseCdf:
    """Class of inverse cumulative distribution functions and their associated
    methods, in a style similar to CovidSim.
    """

    def __init__(self, mean, icdf_array):
        """Constructor Method.

        :param mean: Mean of the icdf
        :type mean: float
        :param icdf_array: Array of quantiles of the icdf_array
        :type icdf_array: numpy array
        """
        self.mean = mean
        self.icdf_array = icdf_array
        self.CDF_RES = pe.Parameters.instance().CDF_RES

    def icdf_choose_noexp(self) -> float:
        """Chooses a value from the input inverse cumulative distribution function,
        following what is done in CovidSim (without exponentialisation), and
        returns the value as a float.

        :returns: chosen value among the quantiles
        :rtype: float
        """
        time_steps_per_day = pe.Parameters.instance().time_steps_per_day
        rand_num = random.random()
        q = rand_num*self.CDF_RES
        i = math.floor(q)
        q -= float(i)
        ti = self.mean \
            * (q * self.icdf_array[i+1] + (1.0 - q) * self.icdf_array[i])
        value = math.floor(0.5 + (ti * time_steps_per_day))
        return value

    def icdf_choose_exp(self) -> float:
        """Chooses a value from the input inverse cumulative distribution function,
        following what is done in CovidSim (with exponentialisation), and
        returns the value as a float.

        :returns: chosen value among the quantiles
        :rtype: float
        """
        exp_icdf_array = np.exp(-self.icdf_array)
        time_steps_per_day = pe.Parameters.instance().time_steps_per_day
        rand_num = random.random()
        q = rand_num*self.CDF_RES
        i = math.floor(q)
        q -= float(i)
        ti = -self.mean * \
            np.log((q * exp_icdf_array[i+1] + (1.0 - q) * exp_icdf_array[i]))
        value = math.floor(0.5 + (ti * time_steps_per_day))
        return value
