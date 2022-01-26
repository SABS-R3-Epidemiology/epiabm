#
# Calculate spatial force of infection based on Covidsim code
#

from pyEpiabm.core import Person, Cell


class SpatialInfection:
    """Class to calculate the infectiousness and susceptibility
    parameters for the force of infection parameter, between cells.
    """
    @staticmethod
    def cell_inf(inf_cell: Cell, timestep: int):
        """Calculate the infectiveness of one cell
        towards its neighbouring cells.

        :param inf_cell: Cell doing infecting
        :type inf_cell: Cell
        :param timestep: Current simulation timestep
        :type timestep: int
        :return: Average number of infection events from the cell
        :rtype: int
        """
        R_value = 2  # R_value might be the wrong term
        total_infectors = inf_cell.infectious_number()
        # Add in other classes of people who are infectors
        number_to_infect = total_infectors * R_value
        return number_to_infect

    @staticmethod
    def space_susc(susc_cell: Cell, infectee: Person,
                   timestep: int):
        """Calculate the susceptibility of a one cell
        towards its neighbouring cells.

        :param susc_cell: Cell receiving infections
        :type susc_cell: Cell
        :param infectee: Infectee
        :type infectee: Person
        :param timestep: Current simulation timestep
        :type timestep: int
        :return: Susceptibility parameter of cell
        :rtype: float
        """
        return 0.2

    @staticmethod
    def space_inf(inf_cell: Cell, infector: Person,
                  timestep: int):
        """Calculate the infectiousness between cells.
        Dependent on the infectious people in it, and social
        distancing measures.

        :param inf_cell: Cell doing infecting
        :type inf_cell: Cell
        :param infector: Infector
        :type infector: Person
        :param timestep: Current simulation timestep
        :type timestep: int
        :return: Infectiousness parameter of cell
        :rtype: float
        """
        return 0.5

    @staticmethod
    def space_foi(inf_cell: Cell, susc_cell: Cell, infector: Person,
                  infectee: Person, timestep: int):
        """Calculate the force of infection between cells, for a particular
        infector and infectee.

        :param inf_cell: cell doing infecting
        :type inf_cell: Cell
        :param susc_cell: cell receiving infections
        :type susc_cell: Cell
        :param infector: Infector
        :type infector: Person
        :param infectee: Infectee
        :type infectee: Person
        :param timestep: Current simulation timestep
        :type timestep: int
        :return: Force of infection parameter of cell
        :rtype: float
        """
        infectiousness = SpatialInfection.space_inf(inf_cell, infector,
                                                    timestep)
        susceptibility = SpatialInfection.space_susc(susc_cell, infectee,
                                                     timestep)
        return (infectiousness * susceptibility)
