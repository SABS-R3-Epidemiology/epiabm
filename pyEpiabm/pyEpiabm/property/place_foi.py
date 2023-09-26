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
        place_inf = 0 if ((hasattr(infector.microcell, 'closure_start_time'))
                          ) and (infector.is_place_closed(
                            Parameters.instance().intervention_params[
                                'place_closure']['closure_place_type'])) and (
                                infector.microcell.closure_start_time <= time
                                ) else \
            (transmission / num_groups
                * PersonalInfection.person_inf(infector, time))
        return place_inf

    @staticmethod
    def place_susc(place, infectee,
                   time: float):
        """Calculate the susceptibility of a place.
        Does not include interventions such as isolation,
        or whether individual is a carehome resident.

        Parameters
        ----------
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
        place_susc = 1.0
        place_idx = place.place_type.value - 1
        if (hasattr(infectee.microcell, 'distancing_start_time')) and (
                infectee.microcell.distancing_start_time is not None) and (
                    infectee.microcell.distancing_start_time <= time):
            if (hasattr(infectee, 'distancing_enhanced')) and (
                        infectee.distancing_enhanced is True):
                place_susc *= Parameters.instance().\
                             intervention_params[
                             'social_distancing'][
                             'distancing_place_enhanced_susc'][place_idx]
            else:
                place_susc *= Parameters.instance().\
                             intervention_params[
                             'social_distancing'][
                             'distancing_place_susc'][place_idx]
        return place_susc

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

        carehome_scale_susc = 1
        if place.place_type.value == 5 and (infectee.key_worker
                                            or infector.key_worker):
            carehome_scale_susc = Parameters.instance()\
                .carehome_params["carehome_worker_group_scaling"]
        travel_isolation_scale = Parameters.instance().\
            intervention_params['travel_isolation']['isolation'
                                                    '_effectiveness'] \
            if (hasattr(infector, 'travel_isolation_start_time')) and (
                infector.travel_isolation_start_time is not None) and (
                    infector.travel_isolation_start_time <= time) else 1
        isolation_scale = Parameters.instance().\
            intervention_params['case_isolation']['isolation_effectiveness']\
            if (hasattr(infector, 'isolation_start_time')) and (
                infector.isolation_start_time is not None) and (
                    infector.isolation_start_time <= time) else 1
        place_idx = place.place_type.value - 1
        quarantine_scale = Parameters.instance().\
            intervention_params['household_quarantine'][
                'quarantine_place_effectiveness'][place_idx]\
            if (hasattr(infectee, 'quarantine_start_time')) and (
                infectee.quarantine_start_time is not None) and (
                    infectee.quarantine_start_time <= time) else 1

        # Dominant interventions: 1) travel_isolate; 2) case_isolate;
        isolation_scale_inf = 1
        if travel_isolation_scale != 1:
            isolation_scale_inf = travel_isolation_scale
        elif isolation_scale != 1:
            isolation_scale_inf = isolation_scale

        infectiousness = (PlaceInfection.place_inf(place, infector, time)
                          * isolation_scale_inf * quarantine_scale)
        susceptibility = (PlaceInfection.place_susc(place, infectee,
                          time) * carehome_scale_susc * quarantine_scale)
        return (infectiousness * susceptibility)
