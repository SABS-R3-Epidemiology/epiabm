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

    def initialize(self, cell) -> None:
        """Initialize Compartments by a cell/microcell containing people.
        Assumes the counter is empty so should only be used in initialisation.

        :param cell: Cell or Microcell CompartmentCounter is tracking
        :type cell: `Cell` or `Microcell`
        """
        self._compartments = {status: 0 for status in InfectionStatus}
        for person in cell.persons:
            inf_status = person.infection_status
            self._compartments[inf_status] += 1

    def report(self, old_status: InfectionStatus,
               new_status: InfectionStatus, new_person=False) -> None:
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

    def report_new_person(self) -> None:
        """Separate to the initialise functionality, this adds a
        new susceptible person to the cell.
        """
        self._compartments[InfectionStatus.Susceptible] += 1

    def retrieve(self) -> typing.Dict[InfectionStatus, int]:
        """Get Compartment Counts.
        Returns dictionary of compartment counts.

        :return: Dictionary of compartments
        :rtype: dict
        """
        return self._compartments
