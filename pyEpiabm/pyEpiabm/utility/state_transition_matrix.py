#
# Generate state transmission matrix
#

import pandas as pd
import numpy as np

import pyEpiabm as pe
from pyEpiabm.property import InfectionStatus


class StateTransitionMatrix:
    """Class to generate and edit the state transition matrix
    """
    def build_state_transition_matrix(self):
        """Builds the structure of the state transition matrix that is used in
        the host progression sweep. Labels the rows and the columns with the
        infection status. Fill the rest of the dataframe with zero
        probabilities of transition.

        :returns: Symmetric matrix in the form of a dataframe
        :rtype: Pandas dataframe
        """
        # Currently, method very rigid. Can add flexibility later.
        nb_states = len(InfectionStatus)
        zero_trans = np.zeros((nb_states, nb_states))
        labels = [status.name for status in InfectionStatus]
        init_matrix = pd.DataFrame(zero_trans,
                                   columns=labels,
                                   index=labels)
        return init_matrix

    def fill_state_transition_matrix(self, matrix):
        """Fill the state transition matrix with the non-zeros probabilities.
        The rows are associated to the current infection status, the
        columns to the next infection status, and the elements are the
        probabilities to go from one state to another. For example, the element
        ij in the matrix is the probability of someone with current infection
        status associated with the row i to move to the infection status
        associated with the columns j.

        :param matrix: Initialised state transition matrix, with right column
        and row names. The first column contains the current infection status
        and all the transition probabilities are set to zero.
        :type matrix: Pandas dataframe
        :returns: Matrix in the form of a dataframe
        :rtype: Pandas dataframe
        """
        matrix.loc['Susceptible', 'Exposed'] = 1
        matrix.loc['Exposed', 'InfectASympt'] = 0.34
        matrix.loc['Exposed', 'InfectMild'] = 0.410061048258529
        matrix.loc['Exposed', 'InfectGP'] = 0.249938951741471
        matrix.loc['InfectASympt', 'Recovered'] = 1
        matrix.loc['InfectMild', 'Recovered'] = 1
        matrix.loc['InfectGP', 'Recovered'] = 0.837111575271931
        matrix.loc['InfectGP', 'InfectHosp'] = 0.162888424728069
        matrix.loc['InfectHosp', 'Recovered'] = 0.44166691836952
        matrix.loc['InfectHosp', 'InfectICU'] = 0.3969284544
        matrix.loc['InfectHosp', 'Dead'] = 0.161404627229571
        matrix.loc['InfectICU', 'InfectICURecov'] = 0.4765104
        matrix.loc['InfectICU', 'Dead'] = 0.5234896
        matrix.loc['InfectICURecov', 'Recovered'] = 1
        matrix.loc['Recovered', 'Recovered'] = 1
        matrix.loc['Dead', 'Dead'] = 1
        return matrix

    def update_probability(self, current_infection_status_row,
                           next_infection_status_column, new_probability):
        """Method to manually update a transition probability in the
        transition state matrix.

        :param current_infection_status_row: infection status corresponding to
        the row where the probability will be updated
        :param next_infection_status_column: infection status corresponding to
        the column where the probability will be updated
        :type next_infection_status_column: enum
        :param new_probability: updated transition probability value
        :type new_probability: float
        """
        try:
            (current_infection_status_row not in InfectionStatus) or\
                    (next_infection_status_column not in InfectionStatus)
        except TypeError:
            raise ValueError('row and column inputs must be contained in\
                                the InfectionStatus enum')

        if (new_probability < 0) or (new_probability > 1):
            raise ValueError('new probability must be a valid probability between\
                            0 and 1')

        # Extract row and column names from enum and retrieve trasition matrix
        matrix = pe.Parameters.instance().state_transition_matrix
        row = current_infection_status_row.name
        column = next_infection_status_column.name
        matrix.loc[row, column] = new_probability