#
# Maintains a count of people in InfectionStatus compartments
#

import typing
import numpy as np

from pyEpiabm.property import InfectionStatus

import pyEpiabm.core


class _CompartmentCounter:
    """Class Component which maintains count of people in each compartment,
    according to their age group.

    """

    def __init__(self, identifier: str):
        """Constructor Method.

        Parameters
        ----------
        identifier : str
            Identifier for this counter

        """
        # Identifier
        self._identifier = identifier
        # Number of age groups
        if pyEpiabm.core.Parameters.instance().use_ages:
            self.nb_age_groups =\
                len(pyEpiabm.core.Parameters.instance().age_proportions)
        else:
            self.nb_age_groups = 1

        # Internal datastore, returns array with age group for each status
        # infection
        self._compartments = {status: np.zeros(self.nb_age_groups, dtype=int)
                              for status in InfectionStatus}

    @property
    def identifier(self):
        """Get identifier.

        """
        return self._identifier

    def report(self, old_status: InfectionStatus,
               new_status: InfectionStatus, age_group=0) -> None:
        """Report Person has changed state.
        Update internal compartments state.

        Parameters
        ----------
        old_status : InfectionStatus
            Person's previous infection state
        new_status : InfectionStatus
            Person's new infection state
        age_group : Age group index
            Person's associated age group, defaults to 0 if age not implemented

        """
        if self._compartments[old_status][age_group] <= 0:
            raise ValueError("No people of this status and of this age group \
                              in this cell.")
        # Initialisation of the age_counter array
        age_counter = np.zeros(self.nb_age_groups, dtype=int)
        age_counter[age_group] = 1
        self._compartments[old_status] -= age_counter
        self._compartments[new_status] += age_counter

    def _increment_compartment(self, n_persons: int,
                               infection_status: InfectionStatus,
                               age_group=0, add_or_remove=True) -> None:
        """Function to add a block of people with the same infection status
        and age group (if age is used) to a compartment.


        Parameters
        ----------
        n_person : int
            Number of people being added to cell or microcell
        infection_status : InfectionStatus
            Status of people being added
        age_group : Age group index
            Person's associated age group
        add_or_remove : bool
            True means adding, False will subtract

        """
        # Initialisation of the age_counter array
        age_counter = np.zeros(self.nb_age_groups, dtype=int)
        age_counter[age_group] = n_persons
        if add_or_remove:
            self._compartments[infection_status] += age_counter
        else:
            self._compartments[infection_status] -= age_counter

    def retrieve(self) -> typing.Dict[InfectionStatus, np.array]:
        """Get Compartment Counts.
        Returns dictionary of compartment counts, in which each entry is an
        array containing the number of people by age group. If age is not used
        then there is only one age group and the array length is 1.

        Returns
        -------
        dict
            Dictionary of compartments

        """
        return self._compartments

    def clear_counter(self):
        """ Method to clear and reset compartment counter to zero.
        """

        self._compartments = {status: np.zeros(self.nb_age_groups, dtype=int)
                              for status in InfectionStatus}
