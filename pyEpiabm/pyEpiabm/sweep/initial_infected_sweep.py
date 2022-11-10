#
# Seed infected individuals in population
#

import random

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

        params = Parameters.instance().carehome_params

        if params["carehome_allow_initial_infections"] > 0:
            if ("initial_infected_cell" not in sim_params
                    or not sim_params["initial_infected_cell"]):
                all_persons = [pers for cell in self._population.cells for pers
                               in cell.persons if pers.infection_status
                               == InfectionStatus.Susceptible]
            else:
                cell = random.choice(self._population.cells)
                all_persons = [pers for pers in cell.persons if pers
                               .infection_status == InfectionStatus.Susceptible]

        else:
            if ("initial_infected_cell" not in sim_params
                    or not sim_params["initial_infected_cell"]):
                all_persons = [pers for cell in self._population.cells for pers
                               in cell.persons if (pers.infection_status ==
                               InfectionStatus.Susceptible
                               and "CareHome" not in pers.place_types)]
            else:
                cell = random.choice(self._population.cells)
                all_persons = [pers for pers in cell.persons if
                (pers.infection_status == InfectionStatus.Susceptible and
                "CareHome" not in pers.place_types)]

        pers_to_infect = random.sample(all_persons,
                                       sim_params["initial_infected_number"])
        for person in pers_to_infect:
            person.update_status(InfectionStatus.InfectMild)
            person.next_infection_status = InfectionStatus.Recovered
            HostProgressionSweep.set_infectiousness(person, start_time)
            HostProgressionSweep().update_time_status_change(person,
                                                             start_time)
