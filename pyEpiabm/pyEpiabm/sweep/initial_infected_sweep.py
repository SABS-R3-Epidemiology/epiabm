#
# Seed infected individuals in population
#

import random
import math
import logging

from pyEpiabm.property import InfectionStatus
from pyEpiabm.sweep.host_progression_sweep import HostProgressionSweep
from pyEpiabm.core import Parameters

from .abstract_sweep import AbstractSweep


class InitialInfectedSweep(AbstractSweep):
    """Class for sweeping through population at start
    of simulation and setting an initial number of infected people,
    with status InfectMild.

    """

    def __call__(self, sim_params: dict):
        """Method that randomly chooses a user-supplied number of people
        in the population, changes their infection status to InfectMild
        and sets their time of next status change.

        Parameters
        ----------
        sim_params : dict
            Dictionary of simulation parameters

        """

        pop_size = self._population.total_people()
        if pop_size < \
                sim_params["initial_infected_number"]:
            raise ValueError('Initial number of infected people needs to be'
                             + ' less than the total population')

        if math.floor(sim_params["initial_infected_number"]) < \
                sim_params["initial_infected_number"]:
            logging.warning("Initial number of infected people needs to be an"
                            + " integer so we use floor function to round"
                            + " down. Inputed value was"
                            + f" {sim_params['initial_infected_number']}")
            sim_params["initial_infected_number"] = \
                math.floor(sim_params["initial_infected_number"])

        start_time = sim_params["simulation_start_time"]
        if start_time < 0:
            raise ValueError('Simulation start time needs to be greater or'
                             + ' equal to 0')

        # Checks whether there are enough susceptible people to infect.
        status = InfectionStatus.Susceptible
        num_susceptible = 0
        for cell in self._population.cells:
            num_susceptible = num_susceptible + \
                sum(cell.compartment_counter.retrieve()[status])

        if num_susceptible < sim_params["initial_infected_number"]:
            raise ValueError('There are not enough susceptible people in the \
                                        population to infect')

        # set default to not treat carehome residents differently
        carehome_inf = 1
        if hasattr(Parameters.instance(), 'carehome_params'):
            care_param = Parameters.instance().carehome_params
            carehome_inf = care_param["carehome_allow_initial_infections"]

        if ("initial_infected_cell" not in sim_params
                or not sim_params["initial_infected_cell"]):
            all_persons = [pers for cell in self._population.cells for pers
                           in cell.persons if
                           (pers.infection_status ==
                            InfectionStatus.Susceptible)]
        else:
            cell = random.choice(self._population.cells)
            all_persons = [pers for pers in cell.persons if
                           (pers.infection_status ==
                            InfectionStatus.Susceptible)]

        if carehome_inf == 0:
            for person in all_persons:
                if person.care_home_resident:
                    all_persons.remove(person)

        if len(all_persons) < sim_params["initial_infected_number"]:
            raise ValueError('There are not enough susceptible people in the \
                                        population to infect due to excluding \
                                        care home residents')

        pers_to_infect = random.sample(all_persons,
                                       int(sim_params
                                           ["initial_infected_number"]))
        for person in pers_to_infect:
            person.update_status(InfectionStatus.InfectMild)
            person.next_infection_status = InfectionStatus.Recovered
            HostProgressionSweep.set_infectiousness(person, start_time)
            HostProgressionSweep().update_time_status_change(person,
                                                             start_time)
