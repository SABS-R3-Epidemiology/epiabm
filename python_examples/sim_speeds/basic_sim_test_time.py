import os
import logging
import pandas as pd
import matplotlib.pyplot as plt
import time

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

pop_sizes = [1000,2000,4000,8000,10000]
sim_times = []

number_sims = len(pop_sizes)

for i in range(len(pop_sizes)):

    # Pop_params are used to configure the population structure being used in this
    # simulation.
    pop_params = {"population_size": pop_sizes[i], "cell_number": 1,
              "microcell_number": 1, "household_number": 5,
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

    # Need to close the writer object at the end of each simulation.
    del sim.writer
    del sim





##Plotting graph code
x = pop_sizes
y = sim_times

plt.title("Simulation time for basic simulation over 60 days")
plt.xlabel('Population Size')
plt.xscale('linear')
plt.ylabel('time (s)')
plt.plot(x, y, marker = 'o', c = 'g')

plt.savefig("sim_speeds_plots/basic_sim_speed.png")


plt.show()