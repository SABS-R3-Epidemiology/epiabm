#
# Calculate place force of infection based on Covidsim code
#

from pyEpiabm.core import Parameters

from .personal_foi import PersonalInfection


class PlaceInfection:
    """Class to calculate the infectiousness and susceptibility
    parameters for the force of infection parameter, within places.
    """

    @staticmethod
    def place_inf(place, infector, time: float):
        """Calculate the infectiousness of a place. Does not include
        interventions such as isolation, or whether individual is a
        carehome resident.

        Does not yet differentiate between places as we have not decided which
        places to implement, and what transmission to give them.

        Parameters
        ----------
        place : Place
            Place
        infector : Person
            Infectious person
        time : float
            Current simulation time

        Returns
        -------
        float
            Infectiousness parameter of place

        """
        params = Parameters.instance().place_params
        transmission = params["place_transmission"]
        place_idx = place.place_type.value - 1
        try:
            num_groups = params["mean_group_size"][place_idx]
        except IndexError:  # For place types not in parameters
            num_groups = 1
        # Use group-wise capacity not max_capacity once implemented
        return (transmission / num_groups
                * PersonalInfection.person_inf(infector, time))

    @staticmethod
    def place_susc(place, infector, infectee,
                   time: float):
        """Calculate the susceptibility of a place.
        Does not include interventions such as isolation,
        or whether individual is a carehome resident.

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
        return 1.0

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
        isolating = infector.microcell.cell.isolation_effectiveness\
            if infector.isolation_start_time is not None else 1
        infectiousness = (PlaceInfection.place_inf(place, infector, time)
                          * isolating)
        susceptibility = PlaceInfection.place_susc(place, infector, infectee,
                                                   time)
        return (infectiousness * susceptibility)
