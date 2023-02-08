#
# Household Class
#

import typing
from numbers import Number
from pyEpiabm.property import InfectionStatus


class Household:
    """Class representing a household,
    a group of people (family or otherwise) who live
    together and share living spaces. This group will
    have a combined susceptibility and infectiousness
    different to that of the individuals.
    """
    def __init__(self, microcell, loc: typing.Tuple[float, float],
                 susceptibility=0, infectiousness=0):
        """Constructor Method.

        Parameters
        ----------
        loc : Tuple[float, float]
            Location of household
        susceptibility : float
            Household's base susceptibility to infection events
        infectiousness : float
            Household's base infectiousness

        """
        self.persons = []
        self.susceptible_persons = []
        self.location = loc
        self.susceptibility = susceptibility
        self.infectiousness = infectiousness
        self.cell = microcell.cell
        self.microcell = microcell

        if not (len(loc) == 2 and isinstance(loc[0], Number) and
                isinstance(loc[1], Number)):
            raise ValueError("Location must be a tuple of float-type")

    def __repr__(self):
        """Returns a string representation of Household.

        Returns
        -------
        str
            String representation of the household

        """
        return "Household at " \
            + f"({self.location[0]:.2f}, {self.location[1]:.2f}) "\
            + f"with {len(self.persons)} people."

    def add_person(self, person):
        """Adds a person to this household.

        Parameters
        ----------
        person : Person
            Person to be added

        """
        self.persons.append(person)
        person.household = self
        if person.infection_status \
                in [InfectionStatus.Susceptible]:
            self.add_susceptible_person(person)

    def add_susceptible_person(self, susceptible_person):
        """Adds a person to the list of susceptible people in the household.

        Parameters
        ----------
        susceptible_person : Person
            Person to be added

        """
        if susceptible_person not in self.susceptible_persons:
            self.susceptible_persons.append(susceptible_person)
            susceptible_person.household = self

    def remove_susceptible_person(self, non_susceptible_person):
        """Removes an susceptible person from the list of susceptible people
        in the household.

        Parameters
        ----------
        non_susceptible_person : Person
            Person to be removed

        """
        self.susceptible_persons.remove(non_susceptible_person)
        non_susceptible_person.household = self
