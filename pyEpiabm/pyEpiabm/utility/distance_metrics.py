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
             loc2: typing.Tuple[float, float] = (0.0, 0.0)) -> float:
        """Calculate distance based on currently configured distance metric

        Parameters
        ----------
        loc1 : Tuple[float, float]
            (x,y) coordinates of the first place
        loc2 : Tuple[float, float]
            (x,y) coordinates of the second place

        Returns
        -------
        float
            Distance between the two locations

        """
        return DistanceFunctions.dist_euclid(loc1, loc2)

    @staticmethod
    def dist_euclid(loc1: typing.Tuple[float, float],
                    loc2: typing.Tuple[float, float] = (0.0, 0.0)):
        """Calculates distance based on the standard L2, Euclidean
        norm. This assumes the space is approximately planar, and
        so is a good approximation for smaller areas where the curvature
        of the Earth is not significant. Passing a single location
        argument will return the norm of this tuple.

        Parameters
        ----------
        loc1 : Tuple[float, float]
            (x,y) coordinates of the first place
        loc2 : Tuple[float, float]
            (x,y) coordinates of the second place

        Returns
        -------
        float
            Euclidean distance between the two locations

        """
        x1, y1 = loc1
        x2, y2 = loc2
        return ((x1-x2)**2+(y1-y2)**2)**(1/2)

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

        Parameters
        ----------
        loc1 : Tuple[int, int]
            Index location of the first place
        stride : int
            Number of indices in a row
        scales : Tuple[float, float]
            Conversion to global coordinates
        loc2 : Tuple[int, int]
            Index location of the second place

        Returns
        -------
        float
            Periodic distance between the two locations

        """
        # Convert indices to distance measures by dividing by
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
        for index in range(2):
            if diff[index] > 0.5 * scales[index]:
                diff[index] = scales[index] - diff[index]
        return np.linalg.norm(diff)

    def minimum_between_cells(cell1, cell2):
        """Function to find the minimum distance between microcells
        in two cells. Covidsim uses this to weight the spatial kernel.

        Parameters
        ----------
        cell1 : Cell
            First cell to find the minimum distance between

        cell2 : Cell
            Second cell to find the minimum distance between

        Returns
        -------
        float
            Minimum distance between the two cells
        """
        dist = np.inf
        for microcell1 in cell1.microcells:
            for microcell2 in cell2.microcells:
                microcell_dist = DistanceFunctions.dist(microcell1.location,
                                                        microcell2.location)
                if microcell_dist < dist:
                    dist = microcell_dist
        return dist
