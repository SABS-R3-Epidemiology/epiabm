#
# Class of Covidsim-style gravity kernels
#


class SpatialKernel:
    """Class to create the gravity kernel used throughout
    CovidSim in the spatial weighting.
    """
    @staticmethod
    def weighting(distance: float, scale: float = 1, shape: float = 1.0):
        r"""Returns the weighting given by the Covidsim distance
        weighting.
        The formula is given by

        .. math::
            \frac{1}{(1+\frac{\text{distance}}{\text{scale}})^\text{shape}}

        and is further detailed in the wiki:
        https://github.com/SABS-R3-Epidemiology/epiabm/wiki/Comparison-to-Ferguson-Model

        Parameters
        ----------
        distance : float
            Distance input as the main argument
        scale : float
            Parameter to scale the kernel function
        shape : float
            Parameter to change the shape of the kernel function

        Returns
        -------
        weight : float
            Float of the weight function

        """
        assert (scale > 0), "Spatial kernel scale must be positive."
        assert (shape > 0), "Spatial kernel shape must be positive."
        return 1 / (1 + distance / scale) ** shape
