#
# Statistical methods used in Covid-Sim.
#

import numpy as np


class StatisticalMethods:
    """Class containing statistical methods in a style similar to CovidSim.
    """

    def latent_icdf():
        # Set of default, see if we can have access to param file:
        start_value = 1e10
        CDF_RES = 20
        cdf_values = np.zeros(CDF_RES + 1)
        cdf_values[CDF_RES] = start_value
        i = 0
        while i < CDF_RES:
            cdf_values[i] = -np.log(1 - i/CDF_RES)
            i = i + 1

        # Get inverse cdf:
        quantile = 0
        while quantile <= CDF_RES:
            cdf_values[quantile] = np.exp(-cdf_values[quantile])
            quantile = quantile + 1

        inverse_cdf = cdf_values
        latent_icdf = inverse_cdf
        return latent_icdf
