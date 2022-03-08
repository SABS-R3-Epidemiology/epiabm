#
# Calculates distance metrics between spatial points
#

import typing
import numpy as np


class DistanceFunctions:
    """Class which contains multiple distance functions
    for use when considering spatial infections, either
    inter-place or inter-cell.
    """
    @staticmethod
    def dist(loc1: typing.Tuple[float, float],
             loc2: typing.Tuple[float, float] = (0, 0)) -> float:
        """Calculate distance based on currently configured distance metric

        :param loc1: (x,y) coordinates of the first place
        :type loc1: Tuple[float, float]
        :param loc2: (x,y) coordinates of the second place
        :type loc2: Tuple[float, float]
        :return: Distance between the two tuples
        :rtype: float
        """
        return DistanceFunctions.dist_euclid(loc1, loc2)

    @staticmethod
    def dist_euclid(loc1: typing.Tuple[float, float],
                    loc2: typing.Tuple[float, float] = (0, 0)):
        """Calculates distance based on the standard L2, Euclidean
        norm. This assumes the space is approximately planar, and
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
        return np.linalg.norm(np.abs(np.asarray(loc1) - np.asarray(loc2)))

    @staticmethod
    def dist_periodic(loc1: typing.Tuple[int, int],
                      stride: int,
                      scales: typing.Tuple[float, float],
                      loc2: typing.Tuple[int, int] = (0, 0)):
        """One of the function for calculating distances implemented in
        CovidSim. Locations are integer points on a grid, which can be
        mapped to the whole globe. Periodic conditions at the boundary
        mean this only applies to a global grid. Scales should be
        (Earth perimeter, vertical range)

        :param loc1: index location of the first place
        :type loc1: Tuple[int, int]
        :param stride: number of indices in a row
        :type stride: int
        :param scales: conversion to global coordinates
        :type scales: Tuple[float, float]
        :param loc2: index location of the second place
        :type loc2: Tuple[int, int]
        :return: Euclidean distance between the two tuples
        :rtype: float
        """
        # Convert indices to distance mesures by dividing by
        # total number of indices in each row.
        # These points are still on a rectangular grid
        scales = np.asarray(scales)
        stride = np.asarray(stride)
        global1 = (scales*np.asarray(loc1)) / stride
        global2 = (scales*np.asarray(loc2)) / stride
        for loc in [global1, global2]:
            if loc[1] < 0:
                loc[1] = scales[1] + loc[1] + (scales/stride)[1]
        diff = np.abs(global1 - global2)
        # Enforce periodicity of the map from the grid to the Earth.
        # If the distance between points is more than half the total length,
        # it would be quicker to "go round the back" of the Earth
        for index in range(1):
            if diff[index] > 0.5*scales[index]:
                diff[index] = scales[index] - diff[index]
        return np.linalg.norm(diff)
