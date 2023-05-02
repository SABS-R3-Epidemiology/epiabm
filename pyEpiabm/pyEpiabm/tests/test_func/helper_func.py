#
# Help to run functionl tests for interventions.
#

import unittest

import pyEpiabm as pe
from pyEpiabm.property.infection_status import InfectionStatus


class HelperFunc(unittest.TestCase):
    """Class to help running functional tests for interventions.

    """

    def assertNonZeroGreater(self, val_1, val_2):
        """Require groups with nonzero populations to increase
        in magnitude, but check for equality in groups with
        zero values.

        Parameters
        ----------
        val_1 : Numeric
            Expected to be the larger value in comparison
        val_2 : Numeric
            Expected to be the smaller value in comparison

        """
        if val_1 == 0:
            self.assertEqual(val_1, val_2)
        else:
            self.assertGreater(val_1, val_2)

    def compare_susceptible_groups(self, small_pop, large_pop,
                                   status=InfectionStatus.Susceptible,
                                   method='greater'):
        """Compare all elements in the list to verify if they are all
         larger or equal to elements in the other list.

        Parameters
        ----------
        small_pop : list
            The population with fewer individuals
        large_pop : list
            The population with more individuals
        status : InfectionStatus
            The infection status wants to be compared
        method : {'greater', 'equal'}
            Specify if the comparing is for greater or equal or only equal

        """
        for age_group in range(len(pe.Parameters.instance().age_proportions)):
            with self.subTest(age_group=age_group):
                if method == 'greater':
                    self.assertNonZeroGreater(
                        large_pop[0].compartment_counter.retrieve()[
                            status][age_group],
                        small_pop[0].compartment_counter.retrieve()[
                            status][age_group])
                    self.assertNonZeroGreater(
                        large_pop[1].compartment_counter.retrieve()[
                            status][age_group],
                        small_pop[1].compartment_counter.retrieve()[
                            status][age_group])
                elif method == 'equal':
                    self.assertEqual(
                        large_pop[0].compartment_counter.retrieve()[
                            status][age_group],
                        small_pop[0].compartment_counter.retrieve()[
                            status][age_group])
                    self.assertEqual(
                        large_pop[1].compartment_counter.retrieve()[
                            status][age_group],
                        small_pop[1].compartment_counter.retrieve()[
                            status][age_group])

    @classmethod
    def sweep_list_initialise(cls):
        """Initialise and return a sweep list for simulation.
        """
        return [
            pe.sweep.InterventionSweep(),
            pe.sweep.UpdatePlaceSweep(),
            pe.sweep.HouseholdSweep(),
            pe.sweep.PlaceSweep(),
            pe.sweep.SpatialSweep(),
            pe.sweep.QueueSweep(),
            pe.sweep.HostProgressionSweep(),
        ]

    @classmethod
    def intervention_conversion_list(cls, intervention_type):
        """If the intervention parameters is in the dictionary format,
        then convert it to list to make consistent with the
        original parameter file.
        """
        if isinstance(pe.Parameters.instance().intervention_params[
                      intervention_type], dict):
            pe.Parameters.instance().intervention_params[intervention_type] = \
                [pe.Parameters.instance().intervention_params[
                    intervention_type]]
