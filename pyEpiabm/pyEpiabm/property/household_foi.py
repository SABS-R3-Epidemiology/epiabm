#
# Calculate household force of infection based on Covidsim code
#
import pyEpiabm.core
from pyEpiabm.core import Parameters

from .personal_foi import PersonalInfection


class HouseholdInfection:
    """Class to calculate the infectiousness and susceptibility
    parameters for the force of infection parameter, within households.

    """
    @staticmethod
    def household_inf(infector, time: float):
        """Calculate the infectiousness of a person in a given
        household. Does not include interventions such as isolation,
        or whether individual is a carehome resident.

        Parameters
        ----------
        infector : Person
            Infector
        time : float
            Current simulation time

        Returns
        -------
        float
            Infectiousness parameter of household

        """
        closure_inf = Parameters.instance().\
            intervention_params['place_closure'][
                'closure_household_infectiousness'] \
            if (hasattr(infector.microcell, 'closure_start_time')) and (
                infector.is_place_closed(
                    Parameters.instance().intervention_params[
                        'place_closure']['closure_place_type'])) and (
                            infector.microcell.closure_start_time <= time
                        ) else 1
        household_infectiousness = infector.infectiousness * closure_inf
        return household_infectiousness

    @staticmethod
    def household_susc(infector, infectee, time: float):
        """Calculate the susceptibility of one person to another in a given
        household. Does not include interventions such as isolation,
        or whether individual is a carehome resident.

        Parameters
        ----------
        infector : Person
            Infector
        infectee : Person
            Infectee
        time : float
            Current simulation time

        Returns
        -------
        float
            Susceptibility parameter of household

        """
        household_susceptibility = PersonalInfection.person_susc(
            infector, infectee, time)
        if (hasattr(infector.microcell, 'distancing_start_time')) and (
                infector.microcell.distancing_start_time is not None) and (
                    infector.microcell.distancing_start_time <= time):
            if (hasattr(infector, 'distancing_enhanced')) and (
                        infector.distancing_enhanced is True):
                household_susceptibility *= Parameters.instance().\
                    intervention_params['social_distancing'][
                        'distancing_house_enhanced_susc']
            else:
                household_susceptibility *= Parameters.instance().\
                    intervention_params['social_distancing'][
                        'distancing_house_susc']
        return household_susceptibility

    @staticmethod
    def household_foi(infector, infectee, time: float):
        """Calculate the force of infection parameter of a household,
        for a particular infector and infectee.

        Parameters
        ----------
        infector : Person
            Infector
        infectee : Person
            Infectee
        time : float
            Current simulation time

        Returns
        -------
        float
            Force of infection parameter of household

        """
        carehome_scale_inf = 1
        if infector.care_home_resident:
            carehome_scale_inf = Parameters.instance()\
                .carehome_params["carehome_resident_household_scaling"]
        carehome_scale_susc = 1
        if infectee.care_home_resident:
            carehome_scale_susc = Parameters.instance()\
                .carehome_params["carehome_resident_household_scaling"]
        seasonality = 1.0  # Not yet implemented
        travel_isolation_scale = Parameters.instance().\
            intervention_params['travel_isolation']['isolation_house'
                                                    '_effectiveness'] \
            if (hasattr(infector, 'travel_isolation_start_time')) and (
                infector.travel_isolation_start_time is not None) and (
                    infector.travel_isolation_start_time <= time) else 1
        isolation_scale = Parameters.instance().\
            intervention_params['case_isolation']['isolation_house'
                                                  '_effectiveness'] \
            if (hasattr(infector, 'isolation_start_time')) and (
                infector.isolation_start_time is not None) and (
                    infector.isolation_start_time <= time) else 1
        quarantine_scale = Parameters.instance().\
            intervention_params['household_quarantine']['quarantine_house'
                                                        '_effectiveness'] \
            if (hasattr(infectee, 'quarantine_start_time')) and (
                infectee.quarantine_start_time is not None) and (
                    infectee.quarantine_start_time <= time) else 1
        vacc_inf_drop = 1
        if infector.is_vaccinated:
            vacc_params = Parameters.instance()\
                .intervention_params['vaccine_params']
            if time > (infector.date_vaccinated +
                       vacc_params['time_to_efficacy']):
                vacc_inf_drop *= (1 - vacc_params['vacc_inf_drop'])

        # Dominant interventions: 1) travel_isolate; 2) case_isolate
        isolation_scale_inf = 1
        if travel_isolation_scale != 1:
            isolation_scale_inf = travel_isolation_scale
        elif isolation_scale != 1:
            isolation_scale_inf = isolation_scale

        infectiousness = (HouseholdInfection.household_inf(infector, time)
                          * seasonality
                          * vacc_inf_drop
                          * pyEpiabm.core.Parameters.instance().
                          household_transmission
                          * carehome_scale_inf
                          * isolation_scale_inf * quarantine_scale)
        susceptibility = (HouseholdInfection.household_susc(infector,
                                                            infectee, time)
                          * carehome_scale_susc)
        return (infectiousness * susceptibility)
