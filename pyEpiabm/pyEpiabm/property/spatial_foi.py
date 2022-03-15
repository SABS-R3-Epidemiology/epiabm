#
# Calculate spatial force of infection based on Covidsim code
#

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
    def space_inf(inf_cell, infector,
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
        space_inf = infector.infectiousness
        if pyEpiabm.core.Parameters.instance().use_ages:
            space_inf *= pyEpiabm.core.Parameters.instance().\
                age_proportions[infector.age_group]
        return space_inf

    @staticmethod
    def space_susc(susc_cell, infectee,
                   time: float):
        """Calculate the susceptibility of one cell towards its neighbouring cells.
        Does not include interventions such as isolation,
        or whether individual is a carehome resident.

        Parameters
        ----------
        susc_cell : Cell
            Cell receiving infections
        infectee : Person
            Infectee
        time : float
            Current simulation time

        Returns
        -------
        float
            Susceptibility parameter of cell

        """
        if pyEpiabm.core.Parameters.instance().use_ages:
            return pyEpiabm.core.Parameters.instance().\
                age_proportions[infectee.age_group]
        else:
            return 1.0

    @staticmethod
    def space_foi(inf_cell, susc_cell, infector,
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
        infectiousness = SpatialInfection.space_inf(inf_cell, infector,
                                                    time)
        susceptibility = SpatialInfection.space_susc(susc_cell, infectee,
                                                     time)
        return (infectiousness * susceptibility)
