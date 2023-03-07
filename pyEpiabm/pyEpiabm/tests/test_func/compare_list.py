#
# Compare if the first element is larger or equal than the second element
#

import unittest

import pyEpiabm as pe
from pyEpiabm.property.infection_status import InfectionStatus


class CompareList(unittest.TestCase):
    """Class to calculate methods in a style similar to CovidSim.

    """

    def assert_greater_equal(self, small_pop, large_pop,
                             status=InfectionStatus.Susceptible,
                             method='greater'):
        """Reproduction of the ranf_mt method in the Rand.cpp from CovidSim.
        In covid-sim, they would use the thread number to generate the output.

        Returns
        -------
        float
            Returns random number between 0 and 1

        """
        for age_group in range(len(pe.Parameters.instance().age_proportions)):
            with self.subTest(age_group=age_group):
                if method == 'greater':
                    self.assertGreaterEqual(
                        large_pop[0].compartment_counter.retrieve()[
                            InfectionStatus.Susceptible][age_group],
                        small_pop[0].compartment_counter.retrieve()[
                            InfectionStatus.Susceptible][age_group])
                    self.assertGreaterEqual(
                        large_pop[1].compartment_counter.retrieve()[
                            InfectionStatus.Susceptible][age_group],
                        small_pop[1].compartment_counter.retrieve()[
                            InfectionStatus.Susceptible][age_group])
                elif method == 'equal':
                    self.assertEqual(
                        large_pop[0].compartment_counter.retrieve()[
                            InfectionStatus.Susceptible][age_group],
                        small_pop[0].compartment_counter.retrieve()[
                            InfectionStatus.Susceptible][age_group])
                    self.assertEqual(
                        large_pop[1].compartment_counter.retrieve()[
                            InfectionStatus.Susceptible][age_group],
                        small_pop[1].compartment_counter.retrieve()[
                            InfectionStatus.Susceptible][age_group])
