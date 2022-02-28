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
        self.time_steps_per_day = pe.Parameters.instance().time_steps_per_day
        

    def icdf_choose_noexp(self) -> float:
        """Chooses a value from the input inverse cumulative distribution function,
        following what is done in CovidSim (without exponentialisation), and
        returns the value as a float.

        :returns: Mean scaled relative to given icdf
        :rtype: float
        """
        rand_num = random.random()
        q = rand_num * self.CDF_RES
        i = math.floor(q)
        q -= float(i)
        ti = (self.mean 
            * (q * self.icdf_array[i+1] + (1.0 - q) * self.icdf_array[i]))
        value = math.floor(0.5 + (ti * self.time_steps_per_day))
        return value

    def icdf_choose_exp(self) -> float:
        """Chooses a value from the input inverse cumulative distribution function,
        following what is done in CovidSim (with exponentiation), and
        returns the value as a float.

        :returns: Mean scaled relative to given icdf
        :rtype: float
        """
        exp_icdf_array = np.exp(-self.icdf_array)
        rand_num = random.random()
        q = rand_num * self.CDF_RES

        #We take the integer part of q because we require i to be an index.
        #By taking away the integer part of q we ae left with a random number i,
        #on the unit interval that is used for weighted average between icdf values.
        i = math.floor(q)
        q -= float(i)
        ti = -self.mean * \
            np.log((q * exp_icdf_array[i+1] + (1.0 - q) * exp_icdf_array[i]))
        value = math.floor(0.5 + (ti * self.time_steps_per_day))
        return value
