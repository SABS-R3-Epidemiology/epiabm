#
# Calculate household force of infection based on Covidsim code
#

import numpy as np


class RandomMethods:
    """Class to calculate methods in a style similar to CovidSim
    """
    @staticmethod
    def random_number():
        return np.random.random()
