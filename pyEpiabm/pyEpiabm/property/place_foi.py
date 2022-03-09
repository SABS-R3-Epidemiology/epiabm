#
# Calculate place force of infection based on Covidsim code
#

import pyEpiabm.core


class PlaceInfection:
    """Class to calculate the infectiousness and susceptibility
    parameters for the force of infection parameter, within places.
    """

    @staticmethod
    def place_susc(place, infector, infectee,
                   time: float):
        """Calculate the susceptibility of a place.

        Parameters
        ----------
        infector : Person
            Infector
        infectee : Person
            Infectee
        place : Place
            Place
        time : float
            Current simulation time

        Returns
        -------
        float
            Susceptibility parameter of place

        """
        return 0.2

    @staticmethod
    def place_inf(place, time: float):
        """Calculate the infectiousness of a place.
        Not dependent on the people in it.

        Parameters
        ----------
        place : Place
            Place
        time : float
            Current simulation time

        Returns
        -------
        float
            Infectiousness parameter of place

        """
        pyEpiabm.core.Place
        return 0.5

    @staticmethod
    def place_foi(place, infector, infectee,
                  time: float):
        """Calculate the force of infection of a place, for a particular
        infector and infectee.

        Parameters
        ----------
        infector : Person
            Infector
        infectee : Person
            Infectee
        place : Place
            Place
        time : float
            Current simulation time

        Returns
        -------
        float
            Force of infection parameter of place

        """
        infectiousness = PlaceInfection.place_inf(place, time)
        susceptibility = PlaceInfection.place_susc(place, infector, infectee,
                                                   time)
        return (infectiousness * susceptibility)
