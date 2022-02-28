#
# Parameters
#

import numpy as np


class Parameters:
    """Class for global parameters.

    Following a singleton Pattern.
    """
    class __Parameters:
        """Singleton Parameters Object.
        """
        def __init__(self):
            self.latent_period = 4.59
            self.latent_period_iCDF = np.array([0, 0.098616903, 0.171170649,
                                                0.239705594, 0.307516598,
                                                0.376194441, 0.446827262,
                                                0.520343677, 0.597665592,
                                                0.679808341, 0.767974922,
                                                0.863671993, 0.968878064,
                                                1.086313899, 1.219915022,
                                                1.37573215, 1.563841395,
                                                1.803041398, 2.135346254,
                                                2.694118208, 3.964172493])
            self.CDF_RES = 20
            self.time_steps_per_day = 1
            pass

    _instance = None  # Singleton instance

    @staticmethod
    def instance():
        """Creates singleton instance of __Parameters under
        _instance if one doesn't already exist.

        :return: An instance of the __Parameters class
        :rtype: __Parameters
        """
        if not Parameters._instance:
            Parameters._instance = Parameters.__Parameters()
        return Parameters._instance
