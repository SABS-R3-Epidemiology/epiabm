import typing
from .infection_status import InfectionStatus


class CompartmentCounter:
    """Class Component which maintains count of people in each compartment
    """

    def __init__(self, identifier: str):
        """Constructor Method.

        :param identifier: Identifier for this counter
        :type identifier: string
        """
        # Identifier
        self._identifier = identifier
        # Internal datastore
        self._compartments = {status: 0 for status in InfectionStatus}

    @property
    def identifier(self):
        """Get identifier
        """
        return self._identifier

    def initialize(self, n_people) -> None:
        """Initialize Compartments with n_people susceptible and 0 in all the rest.

        :param n_people: Number of people CompartmentCounter
                         is keeping track of.
        :type n_people: int
        """
        self._compartments[InfectionStatus.Susceptible] = n_people

    def report(self, old_status: InfectionStatus,
               new_status: InfectionStatus) -> None:
        """Report Person has changed state.
        Update internal compartments state.

        :param old_status: Person's previous infection state.
        :type old_status: :enum-class:`InfectionStatus`
        :param new_status: Person's new infection state.
        :type new_status: :enum-class:`InfectionStatus`
        """
        self._compartments[old_status] -= 1
        self._compartments[new_status] += 1

    def retrieve(self) -> typing.Dict[InfectionStatus, int]:
        """Get Compartment Counts
        Returns dictionary of compartment counts

        :return: compartments
        :rtype: dict
        """
        return self._compartments
