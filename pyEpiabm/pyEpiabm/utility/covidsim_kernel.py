#
# Class of Covidsim-style gravity kernels
#


class Kernel:
    """Class to create the gravity kernel used throughout
    CovidSim in the spatial weighting.
    """
    @staticmethod
    def weighting(distance: float, scale: float = 4, shape: float = 3.8):
        """Returns the weighting given by the Covidsim distance
        weighting. Default parameters use the Covidsim GB spatial data.

        Parameters
        ----------
        distance : Float
            Distance input as the main argument
        scale : Float
            Parameter to scale the kernel function
        shape : Float
            Parameter to change the shape of the kernel function

        Returns
        ----------
        weight : Float
            Float of the weight function

        """

        return 1/(1+distance/scale)**shape
