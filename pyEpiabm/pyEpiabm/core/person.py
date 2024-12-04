#
# Person Class
#

import random
import re

from pyEpiabm.property import InfectionStatus

from .parameters import Parameters


class Person:
    """Class to represent each person in a population.

    Parameters
    ----------
    microcell : Microcell
        An instance of an :class:`Microcell`

    Attributes
    ----------
    infection_status : InfectionStatus
        Person's current infection status
    next_infection_status : InfectionStatus
        Person's next infection status after current one
    time_of_status_change: int
        Time when person's infection status is updated

    """

    def __init__(self, microcell, age_group=None):
        """Constructor Method.

        Parameters
        ----------
        microcell : Microcell
            Person's parent :class:`Microcell` instance
        age_group : int or None
            Integer identifying persons age group or None if random age should
            be assigned

        """
        self.initial_infectiousness = 0
        self.infectiousness = 0
        self.microcell = microcell
        self.infection_status = InfectionStatus.Susceptible
        self.household = None
        self.places = []
        self.place_types = []
        self.next_infection_status = None
        self.time_of_status_change = None
        self.infection_start_times = []
        self.secondary_infections_counts = []
        self.time_of_recovery = None
        self.num_times_infected = 0
        self.latent_period = None
        self.exposure_period = None
        self.infector_latent_period = None
        self.serial_interval_dict = {}
        self.generation_time_dict = {}
        self.care_home_resident = False
        self.key_worker = False
        self.date_positive = None
        self.is_vaccinated = False
        self.id = self.microcell.id + "." + "." + \
            str(len(self.microcell.persons))

        self.set_random_age(age_group)

    def set_random_age(self, age_group=None):
        """Set random age of person, and save index of their age group.
        Note that the max age in the 80+ group is 84 here, however the precise
        age of 80+ people is never used (exact ages are only used to assign
        school/workplaces) so this does not cause any issues.

        """
        if Parameters.instance().use_ages:
            if age_group is None:
                group_probs = Parameters.instance().age_proportions
                self.age_group = random.choices(range(len(group_probs)),
                                                weights=group_probs)[0]
            else:
                self.age_group = age_group
            self.age = random.randint(0, 4) + 5 * self.age_group
        else:
            self.age = None
            # If age is not used in the model, then every person is in the
            # same age group (to conserve same output structure)
            self.age_group = 0

    def is_symptomatic(self):
        """Query if the person is currently symptomatic.

        Returns
        -------
        bool
            Whether person is currently symptomatic

        """
        return Person.is_infectious(self) and self.infection_status != \
            InfectionStatus.InfectASympt

    def is_infectious(self):
        """Query if the person is currently infectious.

        Returns
        -------
        bool
            Whether person is currently infectious

        """
        return str(self.infection_status).startswith('InfectionStatus.Infect')

    def is_susceptible(self):
        """Query if the person is currently susceptible.

        Returns
        -------
        bool
            Whether person is currently susceptible

        """
        return self.infection_status == InfectionStatus. \
            Susceptible

    def __repr__(self):
        """Returns a string representation of Person.

        Returns
        -------
        str
            String representation of person

        """
        return f"Person ({self.id}), " \
               f"Age = {self.age}, Status = {self.infection_status}."

    def update_status(self,
                      new_status: InfectionStatus) -> None:
        """Update Person's Infection Status.

        Parameters
        ----------
        new_status : InfectionStatus
            Person's new status

        """
        self.microcell.notify_person_status_change(
            self.infection_status, new_status, self.age_group)
        self.infection_status = new_status

        if self.infection_status == InfectionStatus.Susceptible and \
                self.household is not None:
            self.household.add_susceptible_person(self)
        if self.infection_status == InfectionStatus.Exposed:
            if self.household is not None:
                self.household.remove_susceptible_person(self)

    def add_place(self, place, person_group: int = 0):
        """Method adds a place to the place list if the person visits
        or is associated with this place. Places are saved as a tuple
        with the place as the first entry and the group the person is
        associated with as the second.

        Parameters
        ----------
        place: Place
            Place person should be added to
        person_group : int
            Key for the person group dictionary

        """
        if place.cell != self.microcell.cell:
            raise AttributeError("Place and person are not in the same\
                                 cell")
        self.places.append((place, person_group))
        self.place_types.append(place.place_type)

    def remove_place(self, place):
        """Method to remove person for each associated place, to be
        used when updating places.

        Parameters
        ----------
        place: Place
            Place person should be removed from

        """
        place_list = [i[0] for i in self.places]
        if place not in place_list:
            raise KeyError("Person not found in this place")
        else:
            ind = place_list.index(place)
            self.places.pop(ind)
            self.place_types.pop(ind)

    def is_place_closed(self, closure_place_type):
        """Method to check if any of the place in the person's place list
        will be closed based on the place type, to be
        used when place closure intervention is active.

        Parameters
        ----------
        closure_place_type: a list of PlaceType
            PlaceType should be closed if in place closure intervention

        """
        if (hasattr(self.microcell, 'closure_start_time')) and (
                self.microcell.closure_start_time is not None):
            for place_type in self.place_types:
                if place_type.value in closure_place_type:
                    return True
        return False

    def vaccinate(self, time):
        """Used to set a persons vaccination status to vaccinated
        if they are drawn from the vaccine queue.

        """
        self.is_vaccinated = True
        self.date_vaccinated = time

    def remove_person(self):
        """Method to remove Person object from population.
        Used to remove travellers from the population.

        """
        self.microcell.cell.compartment_counter. \
            _increment_compartment(-1, self.infection_status,
                                   self.age_group)
        self.microcell.compartment_counter. \
            _increment_compartment(-1, self.infection_status,
                                   self.age_group)
        self.microcell.cell.persons.remove(self)
        self.microcell.persons.remove(self)
        self.household.persons.remove(self)

    def set_id(self, id: str):
        """Updates id of current person (i.e. for input from file).
        id format: 4.3.2.1 represents cell 4, microcell 3 within this cell,
        household 2 within this microcell, and person 1 within this
        household. The id will only be changed if it is of the correct format.

        Parameters
        ----------
        id : str
            Identity of person

        """

        # Ensure id is a string
        if not isinstance(id, str):
            raise TypeError("Provided id must be a string")

        # This regex will match on any string which takes the form "i.j.k.l"
        # where i, j, k and l are integers (k can be empty)
        if not re.match("^-?\\d+\\.-?\\d+\\.-?\\d*\\.-?\\d+$", id):
            raise ValueError(f"Invalid id: {id}. id must be of the form "
                             f"'i.j.k.l' where i, j, k, l are integers (k"
                             f"can be empty)")

        # Finally, check for duplicates
        person_ids = [person.id for person in self.microcell.persons]
        if id in person_ids:
            raise ValueError(f"Duplicate id: {id}.")

        self.id = id

    def set_time_of_recovery(self, time: float):
        """Records the time at which a person enters the Recovered compartment.

        Parameters
        ----------
        time : float
            Current simulation time

        """
        self.time_of_recovery = time

    def increment_num_times_infected(self):
        """Increments the number of times the person has been Infected as a
        useful parameter to keep track of.
        """
        self.num_times_infected += 1

    def increment_secondary_infections(self):
        """Increments the number of secondary infections the given person has
        for this specific infection period (i.e. if the given person has been
        infected multiple times, then we only increment the current secondary
        infection count).
        """
        try:
            self.secondary_infections_counts[-1] += 1
        except IndexError:
            raise RuntimeError("Cannot call increment_secondary_infections "
                               "while secondary_infections_counts is empty")

    def set_latent_period(self, latent_period: float):
        """Sets the latent period of the current Person.

        Parameters
        ----------
        latent_period : float
            The time between the exposure and infection onset of the current
            Person.
        """
        self.latent_period = latent_period

    def set_exposure_period(self, exposure_period: float):
        """Sets the exposure period (we define here as the time between a
        primary case infection and a secondary case exposure, with the current
        `Person` being the secondary case). We store this to be added to the
        latent period of the infection to give a serial interval.

        Parameters
        ----------
        exposure_period : float
            The time between the infector's time of infection and the time
            of exposure to the current Person
        """
        self.exposure_period = exposure_period

    def set_infector_latent_period(self, latent_period: float):
        """Sets the latent period of the primary infector of this Person. We
        store this in order to calculate the generation_time of the interaction
        between infector and infectee.

        Parameters
        ----------
        latent_period : float
            The latency period of the primary infector (the individual who
            infected the current Person).
        """
        self.infector_latent_period = latent_period

    def store_serial_interval(self):
        """Adds the `latent_period` to the current `exposure_period` to give
        a `serial_interval`, which will be stored in the
        `serial_interval_dict`. The serial interval is the time between a
        primary case infection and a secondary case infection. This method
        is called immediately after a person becomes exposed.
        """
        # This method has been called erroneously if the latent period or
        # exposure period is None
        if self.exposure_period is None:
            raise RuntimeError("Cannot call store_serial_interval while the"
                               " exposure_period is None")
        elif self.latent_period is None:
            raise RuntimeError("Cannot call store_serial_interval while the"
                               " latent_period is None")

        serial_interval = self.exposure_period + self.latent_period
        # The reference day is the day the primary case was first infected
        # This is what we will store in the dictionary
        reference_day = self.time_of_status_change - serial_interval
        try:
            (self.serial_interval_dict[reference_day]
             .append(serial_interval))
        except KeyError:
            self.serial_interval_dict[reference_day] = [serial_interval]

        # Reset the exposure period for the next infection
        self.exposure_period = None

    def store_generation_time(self):
        """Adds the `infector_latent_period` to the current
        `exposure_period` to give a `generation_time`, which will be stored
        in the `generation_time_dict`. The generation time is the time between
        a primary case exposure and a secondary case exposure. This method
        is called immediately after the infectee becomes exposed.
        """
        # This method has been called erroneously if the exposure period is
        # None or if the latent period of primary infector is None
        if self.exposure_period is None:
            raise RuntimeError("Cannot call store_generation_time while the"
                               " exposure_period is None")
        elif self.latent_period is None:
            raise RuntimeError("Cannot call store_generation_time while the"
                               " latent_period is None")
        elif self.infector_latent_period is None:
            if self.time_of_status_change - self.latent_period - \
                    self.exposure_period <= 0.0:
                # We do not record the generation time if the infector has
                # no latent period (if their time of infection was day 0)
                return
            raise RuntimeError("Cannot call store_generation_time while the"
                               " infector_latent_period is None")

        generation_time = self.exposure_period + self.infector_latent_period
        # The reference day is the day the primary case was first exposed
        # This is what we will store in the dictionary
        reference_day = (self.time_of_status_change - self.latent_period
                         - generation_time)
        try:
            (self.generation_time_dict[reference_day]
             .append(generation_time))
        except KeyError:
            self.generation_time_dict[reference_day] = [generation_time]

        # Reset the latency period of the infector for the next infection
        self.infector_latent_period = None
