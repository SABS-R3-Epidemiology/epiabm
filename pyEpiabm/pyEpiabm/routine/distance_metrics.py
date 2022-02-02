#
# Calculates distance metrics between spatial points
#

import typing
import numpy as np


class DistanceFunctions:
    """Class which contains multiple distance functions
    for use when considering spatial infections,  either
    inter-place or inter-cell.
    """
    @staticmethod
    def dist_euclid(loc1: typing.Tuple[float, float],
                    loc2: typing.Tuple[float, float] = (0, 0)):
        """Calculates distance based on the standard L2, Euclidean
        norm. This assumes the space is appromiately planar, and
        so is a good approximation for smaller areas where the curvature
        of the Earth is not significant. Passing a single location
        argument will return the norm of this tuple.

        :param loc1: (x,y) coordinates of the first place
        :type loc1: Tuple[float, float]
        :param loc2: (x,y) coordinates of the second place
        :type loc2: Tuple[float, float]
        :return: Euclidean distance between the two tuples
        :rtype: float
        """
        return np.sqrt((loc1[0] - loc2[0])**2 + (loc1[1] - loc2[1])**2)

    def dist_covidsim(loc1: typing.Tuple[float, float],
                      loc2: typing.Tuple[float, float] = (0, 0)):
        """Calculates distance

        :param loc1: (x,y) coordinates of the first place
        :type loc1: Tuple[float, float]
        :param loc2: (x,y) coordinates of the second place
        :type loc2: Tuple[float, float]
        """
        pass
