#
# Calculate spatial force of infection based on Covidsim code
#

from pyEpiabm.core import Person, Cell, Parameters


class SpatialInfection:
    """Class to calculate the infectiousness and susceptibility
    parameters for the force of infection parameter, between cells.

    """
    @staticmethod
    def cell_inf(inf_cell: Cell, timestep: int):
        """Calculate the infectiousness of one cell
        towards its neighbouring cells.

        Parameters
        ----------
        inf_cell : Cell
            Cell causing the infection
        timestep : int
            Current simulation timestep

        Returns
        -------
        int
            Average number of infection events from the cell

        """
        R_0 = Parameters.instance().basic_reproduction_num
        total_infectors = inf_cell.number_infectious()

        average_number_to_infect = total_infectors * R_0
        # This gives the expected number of infection events
        # caused by people within this cell.
        return (average_number_to_infect)

    @staticmethod
    def space_susc(susc_cell: Cell, infectee: Person,
                   timestep: int):
        """Calculate the susceptibility of one cell
        towards its neighbouring cells.

        Parameters
        ----------
        susc_cell : Cell
            Cell receiving infections
        infectee : Person
            Infectee
        timestep : int
            Current simulation timestep

        Returns
        -------
        float
            Susceptibility parameter of cell

        """
        return 0.2

    @staticmethod
    def space_inf(inf_cell: Cell, infector: Person,
                  timestep: int):
        """Calculate the infectiousness between cells.
        Dependent on the infectious people in it.

        Parameters
        ----------
        inf_cell : Cell
            Cell causing the infection
        infector : Person
            Infector
        timestep : int
            Current simulation timestep

        Returns
        -------
        float
            Infectiousness parameter of cell

        """
        return 0.5

    @staticmethod
    def space_foi(inf_cell: Cell, susc_cell: Cell, infector: Person,
                  infectee: Person, timestep: int):
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
        timestep : int
            Current simulation timestep

        Returns
        -------
        float
            Force of infection parameter of cell

        """
        infectiousness = SpatialInfection.space_inf(inf_cell, infector,
                                                    timestep)
        susceptibility = SpatialInfection.space_susc(susc_cell, infectee,
                                                     timestep)
        return (infectiousness * susceptibility)
