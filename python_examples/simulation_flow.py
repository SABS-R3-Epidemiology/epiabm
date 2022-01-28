#
# Example simulation script with data output and visualisation
#

import os
import pandas as pd
import matplotlib.pyplot as plt

import pyEpiabm as pe

# Method to set the seed at the start of the simulation, for reproducibility

pe.routine.Simulation.set_random_seed(seed=42)

# Pop_params are used to configure the population structure being used in this
# simulation.

pop_params = {"population_size": 100, "cell_number": 1,
              "microcell_number": 1, "household_number": 20,
              "place_number": 2}

pe.Parameters.instance().time_steps_per_day = 1

# Create a population based on the parameters given.
population = pe.routine.ToyPopulationFactory().make_pop(pop_params)
cell = population.cells[0]

# sim_ and file_params give details for the running of the simulations and
# where output should be written to.
sim_params = {"simulation_start_time": 0, "simulation_end_time": 60,
              "initial_infected_number": 5}

file_params = {"output_file": "output.csv",
               "output_dir": "python_examples/simulation_outputs",
               "spatial_output": False}

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
filename = os.path.join(os.path.dirname(__file__), "simulation_outputs",
                        "output.csv")
df = pd.read_csv(filename)
df.plot(x="time", y=["InfectionStatus.Susceptible",
                     "InfectionStatus.InfectMild",
                     "InfectionStatus.Recovered"])
plt.savefig("python_examples/simulation_outputs/simulation_flow_SIR_plot.png")
