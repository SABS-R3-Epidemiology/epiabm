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

        Parameters
        ----------
        identifier : str
            Identifier for this counter

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

        Parameters
        ----------
        old_status : InfectionStatus
            Person's previous infection state
        new_status : InfectionStatus
            Person's new infection state

        """
        if self._compartments[old_status] <= 0:
            raise ValueError("No people of this status in this cell.")
        self._compartments[old_status] -= 1
        self._compartments[new_status] += 1

    def _increment_compartment(self, n_persons: int,
                               infection_status: InfectionStatus) -> None:
        """Function to add a block of people with the same infection status
        to a compartment.

        Parameters
        ----------
        n_person : int
            Number of people being added to cell or microcell
        infection_status : InfectionStatus
            Status of people being added

        """
        self._compartments[infection_status] += n_persons

    def retrieve(self) -> typing.Dict[InfectionStatus, int]:
        """Get Compartment Counts.
        Returns dictionary of compartment counts.

        Returns
        -------
        dict
            Dictionary of compartments

        """
        return self._compartments
