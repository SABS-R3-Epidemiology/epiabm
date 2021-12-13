#
# Cell Class
#
from .microcell import Microcell
from .person import Person
from .infection_status import InfectionStatus
from .compartment_counter import CompartmentCounter
from queue import Queue
import random


class Cell:
    """Class representing a Cell (Subset of Population).
    Collection of :class:`Microcell` s and :class:`Person` s.
    """
    def __init__(self):
        """Constructor Method.
        """
        self.microcells = []
        self.persons = []
        self.person_queue = Queue()
        self.compartment_counter = CompartmentCounter(f"Cell {hash(self)}")

    def __repr__(self):
        """String representation of Cell.

        :return: String representation of Cell.
        :rtype: str
        """
        return f"Cell with {len(self.microcells)} microcells " + \
            f"and {len(self.persons)} people."

    def add_microcells(self, n):
        """Add n empty :class:`Microcell` s to Cell.

        :param n: Number of empty :class:`Microcell` s to add
        :type n: int
        """
        for i in range(n):
            self.microcells.append(Microcell(self))

    def enqueue_person(self, person: Person):
        """Add person to queue for processing at end of iteration.

        :param person: Person to enqueue
        :type person: Person
        """
        self.person_queue.put(person)

    def queue_sweep(self, time):
        """Function to run through the queue of exposed people
        """
        while not self.person_queue.empty():
            person = self.person_queue.get()
            # CovidSim has another random event to determined whether a person
            # who has been in contact with an infected becomes infected
            # themselves.
            r = random.uniform(0, 1)
            infection_event = person.susceptibility # Are we sure?
            if r < infection_event:
                #person.infection_status = InfectionStatus.InfectMild
                person.update_status(InfectionStatus.InfectMild)
                person.time_of_status_change = time
        # Clear the queue for the next timestep.

    def _setup(self) -> None:
        """Setup method. Should be called once Population has been setup.
        Called by population (DOESN'T NEED TO BE CALLED MANUALLY)
        """
        self.compartment_counter.initialize(len(self.persons))
        for mcell in self.microcells:
            mcell._setup()

    def notify_person_status_change(
            self,
            old_status: InfectionStatus,
            new_status: InfectionStatus) -> None:
        """Notify Cell that a person's status has changed.

        :param old_status: Person's old infection status.
        :type old_status: :class:`InfectionStatus`
        :param new_status: Person's new infection status.
        :type new_status: :class:`InfectionStatus`
        """
        self.compartment_counter.report(old_status, new_status)
