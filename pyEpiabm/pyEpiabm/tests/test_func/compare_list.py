#
# Compare if the first element is larger or equal than the second element
#

import unittest

import pyEpiabm as pe
from pyEpiabm.property.infection_status import InfectionStatus


class CompareList(unittest.TestCase):
    """Class to compare each element in the list.

    """

    def assert_greater_equal(self, small_pop, large_pop,
                             status=InfectionStatus.Susceptible,
                             method='greater'):
        """Compare all elements in the list to verify if they are all
         larger or equal to elements in the other list.

        Parameters
        ----------
        small_pop : list
            The population with fewer individuals
        large_pop: list
            The population with more individuals
        status: InfectionStatus
            The infection status wants to be compared
        method: string
            Specify if the comparing is for greater or equal or only equal

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
