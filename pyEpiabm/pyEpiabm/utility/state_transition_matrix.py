#
# Generate state transmission matrix
#

import pandas as pd
import numpy as np
from pyEpiabm.property import InfectionStatus


class StateTransitionMatrix:
    """Class to generate the state transition matrix
    """
    def build_state_transition_matrix(self):
        """Builds the state transition matrix that is used in the host progression
        sweep. The rows are associated to the current infection status, the
        columns to the next infection status, and the elements are the
        probabilities to go from one state to another. For example, the element
        ij in the matrix is the probability of someone with current infection
        status associated with the row i to move to the infection status
        associated with the columns j.

        :returns: Matrix in the form of a dataframe
        :rtype: Pandas dataframe
        """
        nb_states = len(InfectionStatus)
        init_trans = {'current inf status': ['Susceptible', 'Exposed',
                                             'InfectAsympt', 'InfectMild',
                                             'InfectGP', 'InfectHosp',
                                             'InfectICU', 'InfectICURecov',
                                             'Recovered', 'Dead'],
                      'Susceptible': np.zeros(nb_states),
                      'Exposed': np.zeros(nb_states),
                      'InfectAsympt': np.zeros(nb_states),
                      'InfectMild': np.zeros(nb_states),
                      'InfectGP': np.zeros(nb_states),
                      'InfectHosp': np.zeros(nb_states),
                      'InfectICU': np.zeros(nb_states),
                      'InfectICURecov': np.zeros(nb_states),
                      'Recovered': np.zeros(nb_states),
                      'Dead': np.zeros(nb_states)}
        matrix = pd.DataFrame(init_trans)
        # We now need to add the non zeros probabilities
        return matrix
