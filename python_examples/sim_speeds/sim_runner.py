# Code to run simulations and plot runtime for populations of varying size
# but with constant number of population (10 individuals) initially infected.

import os
import logging
# import matplotlib.pyplot as plt
import time
import numpy as np

import pyEpiabm as pe

# Setup output for logging file
logging.basicConfig(filename='sim.log', filemode='w+', level=logging.DEBUG,
                    format=('%(asctime)s - %(name)s'
                            + '- %(levelname)s - %(message)s'))

# Set config file for Parameters
pe.Parameters.set_file(os.path.join(os.path.abspath(''),
                       "simple_parameters.json"))


# Method to set the seed at the start of the simulation, for reproducibility

pe.routine.Simulation.set_random_seed(seed=42)

pop_sizes = np.array([1000, 2000, 4000, 8000, 10000])
sim_times = []

for i in range(len(pop_sizes)):

    # Pop_params are used to configure the population structure being used in
    # this simulation.
    pop_params = {"population_size": pop_sizes[i], "cell_number": 1,
                  "microcell_number": 1, "household_number": 5,
                  "place_number": 2}

    # Create a population based on the parameters given.
    population = pe.routine.ToyPopulationFactory().make_pop(pop_params)

    # sim_ and file_params give details for the running of the simulations and
    # where output should be written to.
    sim_params = {"simulation_start_time": 0, "simulation_end_time": 60,
                  "initial_infected_number": int(pop_sizes[i]/1000)}

    file_params = {"output_file": "output.csv",
                   "output_dir": os.path.join(os.path.abspath('')),
                   "spatial_output": False, "age_stratified": False}

    # Store start time
    st = time.time()

    # Create a simulation object, configure it with the parameters given, then
    # run the simulation.
    sim = pe.routine.Simulation()
    sim.configure(
        population,
        [pe.sweep.InitialInfectedSweep()],
        [pe.sweep.HouseholdSweep(), pe.sweep.QueueSweep(),
         pe.sweep.HostProgressionSweep()],
        sim_params,
        file_params)
    sim.run_sweeps()

    # Store end time
    et = time.time()

    this_sim_time = et - st
    sim_times.append(this_sim_time)

    # Remove the output file
    if os.path.exists("output.csv"):
        os.remove("output.csv")

    # Need to close the writer object at the end of each simulation.
    del sim.writer
    del sim
