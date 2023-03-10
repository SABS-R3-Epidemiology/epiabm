#
# Calculate spatial force of infection based on Covidsim code
#
from pyEpiabm.core import Parameters

import pyEpiabm.core


class SpatialInfection:
    """Class to calculate the infectiousness and susceptibility
    parameters for the force of infection parameter, between cells.

    """
    @staticmethod
    def cell_inf(inf_cell, time: float):
        """Calculate the infectiousness of one cell
        towards its nearby cells. Does not include interventions such
        as isolation, or whether individual is a carehome resident.

        Parameters
        ----------
        inf_cell : Cell
            Cell causing the infection
        time : float
            Current simulation time

        Returns
        -------
        int
            Average number of infection events from the cell

        """
        R_0 = pyEpiabm.core.Parameters.instance().basic_reproduction_num
        total_infectors = inf_cell.number_infectious()

        average_number_to_infect = total_infectors * R_0
        # This gives the expected number of infection events
        # caused by people within this cell.
        return average_number_to_infect

    @staticmethod
    def spatial_inf(inf_cell, infector,
                    time: float):
        """Calculate the infectiousness between cells, dependent on the
        infectious people in it.

        Parameters
        ----------
        inf_cell : Cell
            Cell causing the infection
        infector : Person
            Infector
        time : float
            Current simulation time

        Returns
        -------
        float
            Infectiousness parameter of cell

        """
        age = pyEpiabm.core.Parameters.instance().\
            age_contact[infector.age_group] \
            if pyEpiabm.core.Parameters.instance().use_ages is True else 1
        closure_spatial = Parameters.instance().\
            intervention_params['place_closure']['closure_spatial_params'] \
            if ((hasattr(infector.microcell, 'closure_start_time'))) and (
                infector.is_place_closed(
                    Parameters.instance().intervention_params[
                        'place_closure']['closure_place_type'])) and (
                        infector.microcell.closure_start_time <= time) else 1
        return infector.infectiousness * age * closure_spatial

    @staticmethod
    def spatial_susc(susc_cell, infector, infectee, time: float):
        """Calculate the susceptibility of one cell towards its neighbouring
        cells.

        Parameters
        ----------
        susc_cell : Cell
            Cell receiving infections
        infector : Person
            Infector
        infectee : Person
            Infectee
        time : float
            Current simulation time

        Returns
        -------
        float
            Susceptibility parameter of cell

        """
        spatial_susc = 1.0
        if pyEpiabm.core.Parameters.instance().use_ages:
            spatial_susc = pyEpiabm.core.Parameters.instance().\
                age_contact[infectee.age_group]

        spatial_susc *= Parameters.instance().\
            intervention_params['place_closure']['closure_spatial_params'] \
            if ((hasattr(infector.microcell, 'closure_start_time'))) and (
                infector.is_place_closed(
                    Parameters.instance().intervention_params[
                        'place_closure']['closure_place_type'])) and (
                        infector.microcell.closure_start_time <= time) else 1

        if (hasattr(infector.microcell, 'distancing_start_time')) and (
                infector.microcell.distancing_start_time is not None) and (
                    infector.microcell.distancing_start_time <= time):
            if infector.distancing_enhanced is True:
                spatial_susc *= Parameters.instance().\
                    intervention_params['social_distancing'][
                        'distancing_spatial_enhanced_susc']
            else:
                spatial_susc *= Parameters.instance().\
                    intervention_params['social_distancing'][
                        'distancing_spatial_susc']
        return spatial_susc

    @staticmethod
    def spatial_foi(inf_cell, susc_cell, infector,
                    infectee, time: float):
        """Calculate the force of infection between cells, for a particular
        infector and infectee.

        Parameters
        ----------
        inf_cell : Cell
            Cell doing infecting
        susc_cell : Cell
            Cell receiving infections
        infector : Person
            Infector
        infectee : Person
            Infectee
        time : float
            Current simulation time

        Returns
        -------
        float
            Force of infection parameter of cell

        """
        carehome_scale_inf = 1
        if infector.care_home_resident:
            carehome_scale_inf = pyEpiabm.core.Parameters.instance()\
                .carehome_params["carehome_resident_spatial_scaling"]
        carehome_scale_susc = 1
        if infectee.care_home_resident or infector.care_home_resident:
            carehome_scale_susc = pyEpiabm.core.Parameters.instance()\
                .carehome_params["carehome_resident_spatial_scaling"]
        travel_isolating = Parameters.instance().\
            intervention_params['travel_isolation']['isolation_'
                                                    '_effectiveness'] \
            if (hasattr(infector, 'travel_isolation_start_time')) and (
                infector.travel_isolation_start_time is not None) and (
                    infector.travel_isolation_start_time <= time) else 1
        isolating = Parameters.instance().\
            intervention_params['case_isolation']['isolation_effectiveness']\
            if (hasattr(infector, 'isolation_start_time')) and (
                infector.isolation_start_time is not None) and (
                    infector.isolation_start_time <= time) else 1
        quarantine = Parameters.instance().\
            intervention_params['household_quarantine'][
                'quarantine_spatial_effectiveness']\
            if (hasattr(infectee, 'quarantine_start_time')) and (
                infectee.quarantine_start_time is not None) and (
                    infectee.quarantine_start_time <= time) else 1

        # Dominant interventions: 1) travel_isolate; 2) case_isolate
        isolation_scale_inf = 1
        if isolating != 1:
            isolation_scale_inf = isolating
        if travel_isolating != 1:
            isolation_scale_inf = travel_isolating

        infectiousness = (SpatialInfection.spatial_inf(
            inf_cell, infector, time) * carehome_scale_inf
            * isolation_scale_inf * quarantine)
        susceptibility = (SpatialInfection.spatial_susc(
            susc_cell, infector, infectee, time)
            * carehome_scale_susc * quarantine)
        return (infectiousness * susceptibility)
