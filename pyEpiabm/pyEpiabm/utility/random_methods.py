#
# Calculate household force of infection based on Covidsim code
#

import numpy as np


class RandomMethods:
    """Class to calculate methods in a style similar to CovidSim
    """
    def __init__(self):
        self.prev_s1 = 0
        self.prev_s2 = 0

    @staticmethod
    def random_number():
        return np.random.random()

    def covid_sim_rand(self):
        """Reproduction of the ranf_mt method in the Rand.cpp class of covid-sim.
        In covid-sim, would use the thread number to generate the output.
        """
        # Set parameters:
        Xm1 = 2147483563
        Xm2 = 2147483399
        Xa1 = 40014
        Xa2 = 40692
        # Parameters that would vary on thread number in covid-sim:
        s1 = self.prev_s1
        s2 = self.prev_s2
        # Coming up with the randomness:
        k = s1 / 53668
        s1 = Xa1 * (s1 - k * 53668) - k * 12211
        if (s1 < 0):
            s1 += Xm1
        k = s2 / 52774
        s2 = Xa2 * (s2 - k * 52774) - k * 3791
        if (s2 < 0):
            s2 += Xm2
        self.prev_s1 = s1
        self.prev_s2 = s2
        z = s1 - s2
        if (z < 1):
            z += (Xm1 - 1)
        return z/Xm1
