#
# Example simulation script with data output
#

import os
import logging

import pyEpiabm as pe

# Setup output for logging file
logging.basicConfig(filename='sim.log', filemode='w+', level=logging.DEBUG,
                    format=('%(asctime)s - %(name)s'
                            + '- %(levelname)s - %(message)s'))

# Set config file for Parameters
pe.Parameters.set_file(os.path.join(os.path.dirname(__file__),
                       "simple_parameters.json"))

# Method to set the seed at the start of the simulation, for reproducibility

pe.routine.Simulation.set_random_seed(seed=42)

# Pop_params are used to configure the population structure being used in this
# simulation.

pop_params = {"population_size": 100, "cell_number": 2,
              "microcell_number": 2, "household_number": 5,
              "place_number": 2}

# Create a population based on the parameters given.
population = pe.routine.ToyPopulationFactory().make_pop(pop_params)

# sim_ and file_params give details for the running of the simulations and
# where output should be written to.
sim_params = {"simulation_start_time": 0, "simulation_end_time": 60,
              "initial_infected_number": 10}

file_params = {"output_file": "output.csv",
               "output_dir": os.path.join(os.path.dirname(__file__),
                                          "simulation_outputs"),
               "spatial_output": False,
               "age_stratified": False}

ih_file_params = {"output_dir": os.path.join(os.path.dirname(__file__),
                                             "simulation_outputs"),
                  "status_output": True,
                  "infectiousness_output": True}

# Create a simulation object, configure it with the parameters given, then
# run the simulation.
sim = pe.routine.Simulation()
sim.configure(
    population,
    [pe.sweep.InitialInfectedSweep()],
    [pe.sweep.HouseholdSweep(), pe.sweep.QueueSweep(),
     pe.sweep.HostProgressionSweep(), pe.sweep.DemographicsSweep(file_params)],
    sim_params,
    file_params,
    ih_file_params)
sim.run_sweeps()

# Need to close the writer object at the end of each simulation.
del sim.writer
del sim
