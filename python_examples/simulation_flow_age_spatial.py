#
# Example simulation script with data output and visualisation
#

import os
import logging
import pandas as pd
import matplotlib.pyplot as plt

import pyEpiabm as pe

# Setup output for logging file
logging.basicConfig(filename='sim.log', filemode='w+', level=logging.DEBUG,
                    format=('%(asctime)s - %(name)s'
                            + '- %(levelname)s - %(message)s'))

# Set config file for Parameters
pe.Parameters.set_file("python_examples/spatial_parameters.json")

# Method to set the seed at the start of the simulation, for reproducibility

pe.routine.Simulation.set_random_seed(seed=42)

# Pop_params are used to configure the population structure being used in this
# simulation.

pop_params = {"population_size": 1000, "cell_number": 10,
              "microcell_number": 2, "household_number": 5}

# Create a population based on the parameters given.
population = pe.routine.ToyPopulationFactory().make_pop(pop_params)
pe.routine.ToyPopulationFactory.assign_cell_locations(population)
pe.routine.ToyPopulationFactory.add_places(population, 1)

# sim_ and file_params give details for the running of the simulations and
# where output should be written to.
sim_params = {"simulation_start_time": 0, "simulation_end_time": 60,
              "initial_infected_number": 10}

file_params = {"output_file": "output_age_spatial.csv",
               "output_dir": "python_examples/simulation_outputs",
               "spatial_output": True,
               "age_stratified": True}

# Create a simulation object, configure it with the parameters given, then
# run the simulation.
sim = pe.routine.Simulation()
sim.configure(
    population,
    [pe.sweep.InitialInfectedSweep(), pe.sweep.InitialisePlaceSweep()],
    [
        pe.sweep.UpdatePlaceSweep(),
        pe.sweep.HouseholdSweep(),
        pe.sweep.PlaceSweep(),
        pe.sweep.SpatialSweep(),
        pe.sweep.QueueSweep(),
        pe.sweep.HostProgressionSweep(),
    ],
    sim_params,
    file_params,
)
sim.run_sweeps()

# Need to close the writer object at the end of each simulation.
del(sim.writer)
del(sim)

# Creation of a plot of results (plotter from spatial_simulation_flow)
logging.getLogger("matplotlib").setLevel(logging.WARNING)
filename = os.path.join(os.path.dirname(__file__), "simulation_outputs",
                        "output_age_spatial.csv")
df = pd.read_csv(filename)
df_sum_age = df.copy()
df_sum_age = df_sum_age.drop(["InfectionStatus.Exposed",
                              "InfectionStatus.InfectASympt",
                              "InfectionStatus.InfectGP",
                              "InfectionStatus.InfectHosp",
                              "InfectionStatus.InfectICU",
                              "InfectionStatus.InfectICURecov",
                              "InfectionStatus.Dead"],
                             axis=1)
df_sum_age = df_sum_age.groupby(["time", "cell", "location_x",
                                 "location_y"]).agg(
                                {"InfectionStatus.Susceptible": 'sum',
                                 "InfectionStatus.InfectMild": 'sum',
                                 "InfectionStatus.Recovered": 'sum'})
df_sum_age = df_sum_age.reset_index(level=["cell", "location_x", "location_y"])

df_sum_age = df_sum_age.pivot(columns="cell",
                              values="InfectionStatus.InfectMild")
df_sum_age.plot()

plt.legend(labels=(range(len(df_sum_age.columns))), title="Cell")
plt.title("Infection curves for multiple cells")
plt.ylabel("Infected Population")
plt.savefig(
    "python_examples/simulation_outputs"
    + "/spatial_flow_Icurve_plot.png"
)
