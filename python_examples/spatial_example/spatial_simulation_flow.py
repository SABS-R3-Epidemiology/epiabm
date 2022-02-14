#
# Example simulation script with spatial data output and visualisation
#

import os
import pandas as pd
import matplotlib.pyplot as plt

import pyEpiabm as pe

# Method to set the seed at the start of the simulation, for reproducibility

pe.routine.Simulation.set_random_seed(seed=42)

# Pop_params are used to configure the population structure being used in this
# simulation.

pop_params = {"population_size": 1000, "cell_number": 10,
              "microcell_number": 1, "household_number": 2,
              "place_number": 2}

pe.Parameters.instance().time_steps_per_day = 1

# Create a population framework based on the parameters given.
population = pe.routine.ToyPopulationFactory.make_pop(pop_params)

# Alternatively, can generate population from input file
# file_loc = "python_examples/spatial_example/input.csv"
# population = pe.routine.FilePopulationFactory.make_pop(file_loc,
#                                                        random_seed=42)

# Configure population with input data
pe.routine.ToyPopulationFactory.assign_cell_locations(population)
# also run initial sweep here
cell = population.cells[0]  # do we need this?

# sim_ and file_params give details for the running of the simulations and
# where output should be written to.
sim_params = {"simulation_start_time": 0, "simulation_end_time": 20,
              "initial_infected_number": 20}

file_params = {"output_file": "output.csv",
               "output_dir": "python_examples/spatial_example/spatial_outputs",
               "spatial_output": True}

# Create a simulation object, configure it with the parameters given, then
# run the simulation.
sim = pe.routine.Simulation()
sim.configure(
    population,
    [pe.sweep.InitialInfectedSweep()],
    [pe.sweep.UpdatePlaceSweep(), pe.sweep.HouseholdSweep(),
     pe.sweep.PlaceSweep(), pe.sweep.QueueSweep(),
     pe.sweep.HostProgressionSweep()],
    sim_params,
    file_params)
sim.run_sweeps()

# Need to close the writer object at the end of each simulation.
del(sim.writer)
del(sim)

# Creation of a plot of results
filename = os.path.join(os.path.dirname(__file__), "spatial_outputs",
                        "output.csv")
df = pd.read_csv(filename)


df = df.pivot(index='time', columns='cell',
              values="InfectionStatus.InfectMild")
df.plot()

plt.legend(labels=(range(len(df.columns))), title='Cell')
plt.title("Infection curves for multiple cells")
plt.ylabel("Infected Population")
plt.savefig("python_examples/spatial_example/spatial_outputs/" +
            "spatial_flow_Icurve_plot.png")
