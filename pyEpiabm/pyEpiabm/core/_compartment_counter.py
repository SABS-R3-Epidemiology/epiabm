#
# Maintains a count of people in InfectionStatus compartments
#

import typing

from pyEpiabm.property import InfectionStatus


class _CompartmentCounter:
    """Class Component which maintains count of people in each compartment.
    """

    def __init__(self, identifier: str):
        """Constructor Method.

        :param identifier: Identifier for this counter
        :type identifier: str
        """
        # Identifier
        self._identifier = identifier
        # Internal datastore
        self._compartments = {status: 0 for status in InfectionStatus}

    @property
    def identifier(self):
        """Get identifier.
        """
        return self._identifier

    def report(self, old_status: InfectionStatus,
               new_status: InfectionStatus) -> None:
        """Report Person has changed state.
        Update internal compartments state.

        :param old_status: Person's previous infection state
        :type old_status: InfectionStatus
        :param new_status: Person's new infection state
        :type new_status: InfectionStatus
        """
        if self._compartments[old_status] <= 0:
            raise ValueError("No people of this status in this cell.")
        self._compartments[old_status] -= 1
        self._compartments[new_status] += 1

    def increment_compartment(self, n_persons: int,
                              infection_status: InfectionStatus) -> None:
        """Funtion to add a block of people with the same infection status
        to a compartment.

        :param n_person: number of people being added to cell or microcell
        :type n_person: int
        :param infection_status: status of people being added
        :type infection_status: InfectionStatus
        """
        self._compartments[infection_status] += n_persons

    def retrieve(self) -> typing.Dict[InfectionStatus, int]:
        """Get Compartment Counts.
        Returns dictionary of compartment counts.

        :return: Dictionary of compartments
        :rtype: dict
        """
        return self._compartments
