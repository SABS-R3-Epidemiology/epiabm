#
# Generate state transmission matrix
#

import pandas as pd
import numpy as np
import typing

import pyEpiabm.core
from pyEpiabm.property import InfectionStatus


class StateTransitionMatrix:
    """Class to generate and edit the state transition matrix
    """
    def __init__(self, coefficients: typing.Dict[str, typing.List[float]],
                 use_ages=False):
        """Generate age independent transition matrix.

        Parameters
        ----------
        coefficients : typing.Dict[str, typing.List[float]]
            Dictionary of age-dependent lists for matrix coefficients
        use_ages : bool
            Whether to include age dependant lists in matrix
        """
        self.matrix = self.create_state_transition_matrix(coefficients)
        self.age_dependent = use_ages
        if not self.age_dependent:
            self.remove_age_dependence()

    @staticmethod
    def create_empty_state_transition_matrix():
        """Builds the structure of the state transition matrix that is used in
        the host progression sweep. Labels the rows and the columns with the
        infection status. Fill the rest of the dataframe with zero
        probabilities of transition.

        Returns
        -------
        pd.DataFrame
            Symmetric matrix in the form of a dataframe

        """
        nb_states = len(InfectionStatus)
        zero_trans = np.zeros((nb_states, nb_states))
        labels = [status.name for status in InfectionStatus]
        init_matrix = pd.DataFrame(zero_trans,
                                   columns=labels,
                                   index=labels,
                                   dtype='object')
        return init_matrix

    def create_state_transition_matrix(self, coeff: typing.
                                       Dict[str, typing.List[float]]):
        """Fill the state transition matrix with the non-zeros probabilities.
        The rows are associated to the current infection status, the
        columns to the next infection status, and the elements are the
        probabilities to go from one state to another. For example, the element
        ij in the matrix is the probability of someone with current infection
        status associated with the row i to move to the infection status
        associated with the column j.

        Parameters
        ----------
        coefficients : typing.Dict[str, typing.List[float]]
            Dictionary of age-dependent lists for matrix coefficients

        Returns
        -------
        pd.DataFrame
            Matrix in the form of a dataframe

        """
        matrix = StateTransitionMatrix.create_empty_state_transition_matrix()

        matrix.loc['Susceptible', 'Exposed'] = 1
        matrix.loc['Exposed', 'InfectASympt'] = coeff["prob_exposed_to_asympt"]
        matrix.loc['Exposed', 'InfectMild'] = coeff["prob_exposed_to_mild"]
        matrix.loc['Exposed', 'InfectGP'] = coeff["prob_exposed_to_gp"]
        matrix.loc['InfectASympt', 'Recovered'] = 1
        matrix.loc['InfectMild', 'Recovered'] = 1
        matrix.loc['InfectGP', 'Recovered'] = coeff["prob_gp_to_recov"]
        matrix.loc['InfectGP', 'InfectHosp'] = coeff["prob_gp_to_hosp"]
        matrix.loc['InfectHosp', 'Recovered'] = coeff["prob_hosp_to_recov"]
        matrix.loc['InfectHosp', 'InfectICU'] = coeff["prob_hosp_to_icu"]
        matrix.loc['InfectHosp', 'Dead'] = coeff["prob_hosp_to_death"]
        matrix.loc['InfectICU', 'InfectICURecov'] = coeff["prob_icu_" +
                                                          "to_icurecov"]
        matrix.loc['InfectICU', 'Dead'] = coeff["prob_icu_to_death"]
        matrix.loc['InfectICURecov', 'Recovered'] = 1
        matrix.loc['Recovered', 'Recovered'] = 1
        matrix.loc['Dead', 'Dead'] = 1
        matrix.loc['Vaccinated', 'Vaccinated'] = 1
        return matrix

    def update_probability(self, current_infection_status_row: InfectionStatus,
                           next_infection_status_column: InfectionStatus,
                           new_probability: float):
        """Method to manually update a transition probability in the
        transition state matrix.

        Parameters
        ----------
        current_infection_status_row : InfectionStatus
            Infection status corresponding to
            the row where the probability will be updated
        next_infection_status_column : InfectionStatus
            Infection status corresponding to
            the column where the probability will be updated
        new_probability : float
            Updated transition probability value

        """
        try:
            if (current_infection_status_row not in InfectionStatus) or \
                    (next_infection_status_column not in InfectionStatus):
                raise ValueError('Row and column inputs must be contained in' +
                                 ' the InfectionStatus enum')
        except TypeError:
            raise ValueError('Row and column inputs must be contained in' +
                             ' the InfectionStatus enum')

        if (new_probability < 0) or (new_probability > 1):
            raise ValueError('New probability must be a valid probability' +
                             ' larger than or equal to 0 and less than' +
                             ' or equal to 1')

        # Extract row and column names from enum and retrieve transition matrix
        row = current_infection_status_row.name
        column = next_infection_status_column.name
        self.matrix.loc[row, column] = new_probability

    def remove_age_dependence(self):
        """Conducts weighted average over age groups to remove age dependence
        in the state transition matrix.

        """
        weights = pyEpiabm.core.Parameters.instance().age_proportions
        self.matrix = self.matrix.applymap(
            lambda x: np.average(x, weights=weights)
            if isinstance(x, list) else x)
