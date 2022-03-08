#
# Generate matrix with transition times
#
import pyEpiabm as pe
from pyEpiabm.utility import InverseCdf
from pyEpiabm.utility import StateTransitionMatrix


class TransitionTimeMatrix:
    """Class to generate the matrix with transition times
    """
    def __init__(self):
        """Initialises the transition time matrix the same way as for the
        state transition matrix, ie with the right labels for the rows and
        the columns and zeros as elements.
        """
        self.initial_matrix =\
            StateTransitionMatrix().create_empty_state_transition_matrix()

    def fill_transition_time(self):
        """Fills the transition time matrix with InverseCdf objects, where the
        times of transition are defined. For example, the element ij in the
        matrix is the InverseCdf object for defining the transition time of
        someone with current infection status associated with the row i to
        move to the infection status associated with the columns j.

        Returns
        -------
        pd.DataFrame
            Matrix in the form of a dataframe

        """
        matrix = self.initial_matrix
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
