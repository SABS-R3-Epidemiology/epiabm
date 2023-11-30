#
# Microcell Class
#

import typing
from numbers import Number
import logging
import re

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
        self.persons = []
        self.places = []
        self.households = []
        self.cell = cell
        self.location = cell.location
        self.id = self.cell.id + "." + str(len(self.cell.microcells))
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
        """Updates id of current microcell (i.e. for input from file).

        Parameters
        ----------
        id : str
            Identity of microcell

        """

        # Ensure id is a string
        if not isinstance(id, str):
            raise TypeError("Provided id must be a string")

        # This regex will match on any string which takes the form "i.j" where
        # i and j are integers
        if not re.match("^\\d+\\.\\d+$", id):
            raise ValueError(f"Invalid id: {id}. id must be of the form 'i.j' "
                             f"where i, j are integers")

        # Finally, check for duplicates
        microcell_ids = [microcell.id for microcell in self.cell.microcells]
        if id in microcell_ids:
            raise ValueError(f"Duplicate id: {id}.")

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

    def add_people(self, n, status=InfectionStatus.Susceptible,
                   age_group=None):
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
        for _ in range(n):
            p = Person(self, age_group)
            self.cell.persons.append(p)
            self.persons.append(p)
            p.infection_status = status
            self.compartment_counter._increment_compartment(
                1, p.infection_status, p.age_group)
            self.cell.compartment_counter._increment_compartment(
                1, p.infection_status, p.age_group)

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

    def add_household(self, people: list, change_id: bool = True):
        """Adds a default :class:`Household` to Microcell and fills it with
        a number of :class:`Person` s.

        Parameters
        ----------
        people : list
            List of :class:`People` to add to household
        change_id : bool
            Boolean representing whether we wish to set the id of the people
            of the household when the function is called or not

        """
        if len(people) != 0:
            household = Household(self, loc=self.location)
            for i, person in enumerate(people):
                household.add_person(person)

                # If the person already has a household, then do not change
                # their id
                if change_id:
                    if not re.match("^\\d+\\.\\d+\\.\\d+\\.\\d+$", person.id):
                        person.set_id(household.id + "." + str(i))
                    else:
                        logging.info(f"Person {person.id} has moved to "
                                     f"household {household.id}")

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
