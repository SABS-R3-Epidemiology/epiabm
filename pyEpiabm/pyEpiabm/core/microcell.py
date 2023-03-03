#
# Microcell Class
#

import typing
from numbers import Number
import logging

from pyEpiabm.property import InfectionStatus

from .person import Person
from .place import Place
from .household import Household
from ._compartment_counter import _CompartmentCounter


class Microcell:
    """Class representing a Microcell (Group of people and places).
    Collection of :class:`Person` s.

    Parameters
    ----------
    cell : Cell
        An instance of :class:`Cell`

    """
    def __init__(self, cell):
        """Constructor Method.

        Parameters
        ----------
        cell: Cell
            Microcell's parent :class:`Cell` instance

        """
        self.id = hash(self)
        self.persons = []
        self.places = []
        self.households = []
        self.cell = cell
        self.location = cell.location
        self.compartment_counter = _CompartmentCounter(
            f"Microcell {id(self)}")

    def __repr__(self):
        """Returns a string representation of Microcell.

        Returns
        -------
        str
            String representation of Microcell

        """
        return f"Microcell with {len(self.persons)} people" + \
            f" at location {self.location}."

    def set_id(self, id):
        """Updates ID of microcell (i.e. for input from file).

        Parameters
        ----------
        id : float
            Identity of microcell

        """
        self.id = id

    def add_person(self, person):
        """Adds :class:`Person` with given :class:`InfectionStatus` and given
        age group to Microcell.

        Parameters
        ----------
        person : Person
            Newly instantiated person with InfectionStatus and associated age
            group

        """
        status = person.infection_status
        age_group = person.age_group
        self.compartment_counter._increment_compartment(1, status, age_group)
        self.cell.compartment_counter._increment_compartment(1, status,
                                                             age_group)
        self.cell.persons.append(person)
        self.persons.append(person)

    def add_people(self, n, status=InfectionStatus.Susceptible, age_group=0):
        """Adds n default :class:`Person` of given status to Microcell.

        Parameters
        ----------
        n : int
            Number of default :class:`Person` s to add
        status : InfectionStatus
            Status of persons to add to cell
        age_group : Age group index
            Person's associated age group

        """
        self.compartment_counter._increment_compartment(n, status, age_group)
        self.cell.compartment_counter._increment_compartment(n, status,
                                                             age_group)
        for _ in range(n):
            p = Person(self)
            self.cell.persons.append(p)
            self.persons.append(p)
            p.infection_status = status
            p.age_group = age_group

    def add_place(self, n: int, loc: typing.Tuple[float, float],
                  place_type):
        """Adds n default :class:`Place` to Microcell.

        Parameters
        ----------
        n : int
            Number of default :class:`Place` s to add

        """
        for _ in range(n):
            p = Place(loc, place_type, self.cell, self)
            self.cell.places.append(p)
            self.places.append(p)

    def add_household(self, people: list):
        """Adds a default :class:`Household` to Microcell and fills it with
        a number of :class:`Person` s.

        Parameters
        ----------
        people : list
            List of :class:`People` to add to household

        """
        if len(people) != 0:
            household = Household(self, loc=self.location)
            for person in people:
                household.add_person(person)
        else:
            logging.info("Cannot create an empty household")

    def notify_person_status_change(
            self,
            old_status: InfectionStatus,
            new_status: InfectionStatus,
            age_group) -> None:
        """Notify Microcell that a person's status has changed.

        Parameters
        ----------
        old_status : InfectionStatus
            Person's old infection status
        new_status : InfectionStatus
            Person's new infection status
        age_group : Age group index
            Person's associated age group

        """
        self.compartment_counter.report(old_status, new_status, age_group)
        self.cell.notify_person_status_change(old_status, new_status,
                                              age_group)

    def set_location(self, loc: typing.Tuple[float, float]):
        """Method to set or change the location of a microcell.

        Parameters
        ----------
        loc : Tuple[float, float]
            (x,y) coordinates of the microcell

        """
        if not (len(loc) == 2 and isinstance(loc[0], Number) and
                isinstance(loc[1], Number)):
            raise ValueError("Location must be a tuple of float-type")
        self.location = loc

    def count_icu(self):
        return sum(map(lambda person: person.infection_status ==
                   InfectionStatus.InfectICU, self.persons))

    def count_infectious(self):
        return sum(map(lambda person: person.is_infectious() is
                   True, self.persons))
