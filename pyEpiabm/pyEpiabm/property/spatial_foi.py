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
        towards its neighbouring cells. Does not include interventions such
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
        infectious people in it. Does not include interventions such as
        isolation, whether individual is a carehome resident.

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
            if infector.close_place(
                Parameters.instance().intervention_params['place_closure'][
                    'closure_place_type']) is True else 1
        return infector.infectiousness * age * closure_spatial

    @staticmethod
    def spatial_susc(susc_cell, infector, infectee, time: float):
        """Calculate the susceptibility of one cell towards its neighbouring
        cells. Does not include interventions such as isolation,
        or whether individual is a carehome resident.

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
            if infector.close_place(
                Parameters.instance().intervention_params['place_closure'][
                    'closure_place_type']) is True else 1

        if (hasattr(infector.microcell, 'distancing_start_time') is True) and (
                infector.microcell.distancing_start_time is not None):
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
        isolating = Parameters.instance().\
            intervention_params['case_isolation']['isolation_effectiveness']\
            if (hasattr(infector, 'isolation_start_time') is True) and (
                infector.isolation_start_time is not None) else 1
        quarantine = Parameters.instance().\
            intervention_params['household_quarantine'][
                'quarantine_spatial_effectiveness']\
            if (hasattr(infector, 'quarantine_start_time') is True) and (
                infector.quarantine_start_time is not None) else 1
        infectiousness = (SpatialInfection.spatial_inf(
            inf_cell, infector, time) * isolating * quarantine)
        susceptibility = (SpatialInfection.spatial_susc(
            susc_cell, infector, infectee, time) * quarantine)
        return (infectiousness * susceptibility)
