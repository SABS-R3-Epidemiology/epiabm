#
# Cell Class
#

import typing
import numpy as np
from queue import Queue
from numbers import Number

from pyEpiabm.property import InfectionStatus
from pyEpiabm.utility import DistanceFunctions

from .microcell import Microcell
from .parameters import Parameters
from .person import Person
from ._compartment_counter import _CompartmentCounter


class Cell:
    """Class representing a Cell (Subset of Population).
    Collection of :class:`Microcell` s and :class:`Person` s.

    """
    def __init__(self, loc: typing.Tuple[float, float] = (0, 0)):
        """Constructor Method.

        Parameters
        ----------
        loc : Tuple(float, float)
            Location of the cell, as an (x,y) tuple

        """
        self.location = loc
        self.id = hash(self)
        self.microcells = []
        self.persons = []
        self.places = []
        self.households = []
        self.person_queue = Queue()
        self.PCR_queue = Queue()
        self.LFT_queue = Queue()
        self.compartment_counter = _CompartmentCounter(f"Cell {id(self)}")
        self.nearby_cell_distances = dict()

        if not (len(loc) == 2 and isinstance(loc[0], Number) and
                isinstance(loc[1], Number)):
            raise ValueError("Location must be a tuple of float-type")

    def __repr__(self):
        """Returns a string representation of the Cell.

        Returns
        -------
        str
            String representation of the Cell

        """
        return f"Cell with {len(self.microcells)} microcells " + \
            f"and {len(self.persons)} people at location {self.location}."

    def add_microcells(self, n):
        """Add n empty :class:`Microcell` s to Cell.

        Parameters
        ----------
        n : int
            Number of empty :class:`Microcell` s to add

        """
        for _ in range(n):
            self.microcells.append(Microcell(self))

    def set_id(self, id: float):
        """Updates ID of cell (i.e. for input from file).

        Parameters
        ----------
        id : float
            Identity of cell

        """
        self.id = id

    def enqueue_person(self, person: Person):
        """Add person to queue for processing at end of iteration, provided
        they are not already recovered (and so may be infected).

        Parameters
        ----------
        person : Person
            Person to enqueue

        """
        if person.infection_status != InfectionStatus.Recovered:
            self.person_queue.put(person)

    def enqueue_PCR_testing(self, person: Person):
        """Add person to PCR testing queue for processing in testing
         sweep.

        Detailed description of the implementation can be found in github wiki:
        https://github.com/SABS-R3-Epidemiology/epiabm/wiki/Interventions#testing

        Parameters
        ----------
        person : Person
            Person to enqueue.

        """
        self.PCR_queue.put(person)

    def enqueue_LFT_testing(self, person: Person):
        """Add person to LFT testing queue for processing in testing
         sweep.

        Detailed description of the implementation can be found in github wiki:
        https://github.com/SABS-R3-Epidemiology/epiabm/wiki/Interventions#testing

        Parameters
        ----------
        person : Person
            Person to enqueue.

        """
        self.LFT_queue.put(person)

    def notify_person_status_change(
            self,
            old_status: InfectionStatus,
            new_status: InfectionStatus,
            age_group) -> None:
        """Notify Cell that a person's status has changed.

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

    def number_infectious(self):
        """Returns the total number of infectious people in each
         cell, all ages combined.

        Returns
        -------
        int
            Total infectors in cell

        """
        cell_data = self.compartment_counter.retrieve()
        total_infectors = 0
        for status in InfectionStatus:
            if str(status).startswith('InfectionStatus.Infect'):
                total_infectors += np.sum(cell_data[status])

        return total_infectors

    def set_location(self, loc: typing.Tuple[float, float]):
        """Method to set or change the location of a cell.

        Parameters
        ----------
        loc : Tuple[float, float]
            (x,y) coordinates of the place

        """
        self.location = loc

    def find_nearby_cells(self, other_cells):
        '''
        Helper function which takes in a given cell and the list of all cells
        and generates a list of nearby cells which are
        closer than the cutoff for cross-cell infection.

        Populates: self.find_nearby_cells
        Dictionary of all cells with distance below cutoff.
        Dictionary stores cell.id and distance between the 2 cells
        These are stored in the form:
        cell.id: distance

        Parameters
        ----------
        other_cells : typing.List[Cell]
            List of all cells except cell

        '''
        cutoff = Parameters.instance().infection_radius

        for cell2 in other_cells:
            distance = DistanceFunctions.dist(self.location, cell2.location)
            if distance < cutoff:
                self.nearby_cell_distances[cell2.id] = distance
                # Dict of near neighbours, cells which are closer than the
                # cutoff for cross-cell infection
