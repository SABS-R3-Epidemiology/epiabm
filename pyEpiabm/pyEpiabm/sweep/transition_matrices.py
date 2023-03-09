#
# Transition matrices used by host progression sweep
#

import pandas as pd
import numpy as np
import typing

import pyEpiabm as pe
import pyEpiabm.core
from pyEpiabm.property import InfectionStatus
from pyEpiabm.utility import InverseCdf


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


class TransitionTimeMatrix:
    """Class to generate the matrix with transition times
    """
    def __init__(self):
        """Initialises the transition time matrix the same way as for the
        :class:`StateTransitionMatrix`, i.e. with the right labels for
        the rows and the columns, but with -1 as the default value.

        """
        nb_states = len(InfectionStatus)
        zero_trans = np.full((nb_states, nb_states), -1.0)
        labels = [status.name for status in InfectionStatus]
        self.matrix = pd.DataFrame(zero_trans,
                                   columns=labels,
                                   index=labels,
                                   dtype='object')

    def create_transition_time_matrix(self):
        """Fills the transition time matrix with :class:`InverseCdf` objects,
        where the distributions of times of transition are defined. For
        example, the element ij in the matrix is the :class:`InverseCdf`
        object for defining the transition time of someone with current
        infection status associated with the row i to move to the infection
        status associated with the columns j. Transitions that we do not
        expect to happen are assigned a value of -1.0 in the matrix, so it
        will not pass silently if these are accessed accidentally.

        Returns
        -------
        pd.DataFrame
            Matrix in the form of a dataframe

        """
        matrix = TransitionTimeMatrix().matrix
        matrix.loc['Exposed', 'InfectASympt'] =\
            InverseCdf(pe.Parameters.instance().latent_period,
                       pe.Parameters.instance().latent_period_iCDF)
        matrix.loc['Exposed', 'InfectMild'] =\
            InverseCdf(pe.Parameters.instance().latent_period,
                       pe.Parameters.instance().latent_period_iCDF)
        matrix.loc['Exposed', 'InfectGP'] =\
            InverseCdf(pe.Parameters.instance().latent_period,
                       pe.Parameters.instance().latent_period_iCDF)
        matrix.loc['InfectASympt', 'Recovered'] =\
            InverseCdf(pe.Parameters.instance().asympt_infect_period,
                       pe.Parameters.instance().asympt_infect_icdf)
        matrix.loc['InfectMild', 'Recovered'] =\
            InverseCdf(pe.Parameters.instance().mean_mild_to_recov,
                       pe.Parameters.instance().mild_to_recov_icdf)
        matrix.loc['InfectGP', 'Recovered'] =\
            InverseCdf(pe.Parameters.instance().mean_gp_to_recov,
                       pe.Parameters.instance().gp_to_recov_icdf)
        matrix.loc['InfectGP', 'InfectHosp'] =\
            InverseCdf(pe.Parameters.instance().mean_gp_to_hosp,
                       pe.Parameters.instance().gp_to_hosp_icdf)
        matrix.loc['InfectGP', 'Dead'] =\
            InverseCdf(pe.Parameters.instance().mean_gp_to_death,
                       pe.Parameters.instance().gp_to_death_icdf)
        matrix.loc['InfectHosp', 'Recovered'] =\
            InverseCdf(pe.Parameters.instance().mean_hosp_to_recov,
                       pe.Parameters.instance().hosp_to_recov_icdf)
        matrix.loc['InfectHosp', 'InfectICU'] =\
            InverseCdf(pe.Parameters.instance().mean_hosp_to_icu,
                       pe.Parameters.instance().hosp_to_icu_icdf)
        matrix.loc['InfectHosp', 'Dead'] =\
            InverseCdf(pe.Parameters.instance().mean_hosp_to_death,
                       pe.Parameters.instance().hosp_to_death_icdf)
        matrix.loc['InfectICU', 'InfectICURecov'] =\
            InverseCdf(pe.Parameters.instance().mean_icu_to_icurecov,
                       pe.Parameters.instance().icu_to_icurecov_icdf)
        matrix.loc['InfectICU', 'Dead'] =\
            InverseCdf(pe.Parameters.instance().mean_icu_to_death,
                       pe.Parameters.instance().icu_to_death_icdf)
        matrix.loc['InfectICURecov', 'Recovered'] =\
            InverseCdf(pe.Parameters.instance().mean_icurecov_to_recov,
                       pe.Parameters.instance().icurecov_to_recov)
        return matrix

    def update_transition_time_with_float(
                        self,
                        current_infection_status_row: InfectionStatus,
                        next_infection_status_column: InfectionStatus,
                        new_transition_time: float):
        """Method to manually update a transition time in the
        transition time matrix.

        Parameters
        ----------
        current_infection_status_row : InfectionStatus
            Infection status corresponding to
            the row where the probability will be updated
        next_infection_status_column : InfectionStatus
            Infection status corresponding to
            the column where the probability will be updated
        new_transition_time : float
            Updated transition time value

        """
        try:
            if (current_infection_status_row not in InfectionStatus) or \
                    (next_infection_status_column not in InfectionStatus):
                raise ValueError('Row and column inputs must be contained in' +
                                 ' the InfectionStatus enum')
        except TypeError:
            raise ValueError('Row and column inputs must be contained in' +
                             ' the InfectionStatus enum')

        if new_transition_time < 0:
            raise ValueError('New transition time must be larger than' +
                             ' or equal to 0')

        # Extract row and column names from enum and update
        # transition time matrix with single value
        row = current_infection_status_row.name
        column = next_infection_status_column.name
        self.matrix.loc[row, column] = new_transition_time

    def update_transition_time_with_icdf(
                           self,
                           current_infection_status_row: InfectionStatus,
                           next_infection_status_column: InfectionStatus,
                           new_transition_time_icdf: np.ndarray,
                           new_transition_time_icdf_mean: float):
        """Method to manually update a transition time in the
        transition time matrix.

        Parameters
        ----------
        current_infection_status_row : InfectionStatus
            Infection status corresponding to
            the row where the probability will be updated
        next_infection_status_column : InfectionStatus
            Infection status corresponding to
            the column where the probability will be updated
        new_transition_time_icdf : list
            The associated list of icdf values if wanting to
            specify a new distribution for a transition time
        new_transition_time_icdf_mean : float
            The mean of the icdf if specifying a new distribution
            for a transition time

        """
        try:
            if (current_infection_status_row not in InfectionStatus) or \
                    (next_infection_status_column not in InfectionStatus):
                raise ValueError('Row and column inputs must be contained in' +
                                 ' the InfectionStatus enum')
        except TypeError:
            raise ValueError('Row and column inputs must be contained in' +
                             ' the InfectionStatus enum')

        if new_transition_time_icdf_mean < 0:
            raise ValueError('New transition time mean must be larger than' +
                             ' or equal to 0')

        if len(new_transition_time_icdf) in [0, 1]:
            raise ValueError('List of icdf values must have at least two' +
                             ' elements')

        for elem in new_transition_time_icdf:
            if elem < 0:
                raise ValueError('List of icdf values must only contain' +
                                 ' non-negative numbers')

        # Extract row and column names from enum and update
        # transition time matrix with :class: `InverseCdf`
        # object
        row = current_infection_status_row.name
        column = next_infection_status_column.name
        icdf = InverseCdf(
            new_transition_time_icdf_mean,
            new_transition_time_icdf)
        self.matrix.loc[row, column] = icdf
