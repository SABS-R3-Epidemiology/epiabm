#
# Example simulation script running with Gibraltar parameters
# Incorporates both age and spatial stratification.
#

import os
import sys
import logging
import pandas as pd
import matplotlib.pyplot as plt

import pyEpiabm as pe

sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir,
                "./age_stratified_example"))
from age_stratified_plot import Plotter  # noqa

# Setup output for logging file
logging.basicConfig(filename='sim.log', filemode='w+', level=logging.DEBUG,
                    format=('%(asctime)s - %(name)s'
                            + '- %(levelname)s - %(message)s'))

# Set config file for Parameters
pe.Parameters.set_file(os.path.join(os.path.dirname(__file__),
                                    "gibraltar_parameters.json"))

# Method to set the seed at the start of the simulation, for reproducibility

pe.routine.Simulation.set_random_seed(seed=42)

# Pop_params are used to configure the population structure being used in this
# simulation.

pop_params = {
    "population_size": 33078,
    "cell_number": 12,
    "microcell_number": 81,   # 9*9 microcells per cell
    "household_number": 14,  # Ave 2.5 people per household
    "place_number": 0.15,
}
# Create a population framework based on the parameters given.
population = pe.routine.ToyPopulationFactory.make_pop(pop_params)

# Alternatively, can generate population from input file
file_loc = os.path.join(os.path.dirname(__file__),
                        "gibraltar_inputs", "gib_input.csv")
# population = pe.routine.FilePopulationFactory.make_pop(file_loc,
#                                                       random_seed=42)

# Configure population with input data
pe.routine.ToyPopulationFactory.assign_cell_locations(population)
pe.routine.FilePopulationFactory.print_population(population, file_loc)


# sim_ and file_params give details for the running of the simulations and
# where output should be written to.
sim_params = {"simulation_start_time": 0, "simulation_end_time": 4,
              "initial_infected_number": 100, "initial_infect_cell": True}

file_params = {"output_file": "output_gibraltar.csv",
               "output_dir": os.path.join(os.path.dirname(__file__),
                                          "comparison_outputs"),
               "spatial_output": True,
               "age_stratified": False}

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
del (sim.writer)
del (sim)

# Creation of a plot of results (plotter from spatial_simulation_flow)
logging.getLogger("matplotlib").setLevel(logging.WARNING)
filename = os.path.join(os.path.dirname(__file__), "comparison_outputs",
                        "output_gibraltar.csv")
df_sum_age = pd.read_csv(filename)
df_sum_age = df_sum_age.drop(["InfectionStatus.Exposed",
                              "InfectionStatus.InfectASympt",
                              "InfectionStatus.InfectGP",
                              "InfectionStatus.InfectHosp",
                              "InfectionStatus.InfectICU",
                              "InfectionStatus.InfectICURecov",
                              "InfectionStatus.Dead"],
                             axis=1)
df_sum_age = df_sum_age.groupby(["time"]).agg(
                                {"InfectionStatus.Susceptible": 'sum',
                                 "InfectionStatus.InfectMild": 'sum',
                                 "InfectionStatus.Recovered": 'sum'})
# Create plot to show SIR curves against time
df_sum_age.plot(y=["InfectionStatus.Susceptible",
                   "InfectionStatus.InfectMild",
                   "InfectionStatus.Recovered"])
plt.savefig(os.path.join(os.path.dirname(__file__),
            "comparison_outputs/simulation_flow_SIR_plot.png"))

# Creation of a plot of results with age stratification
# if file_params["age_stratified"]:
p = Plotter(os.path.join(os.path.dirname(__file__),
            "comparison_outputs/output_gibraltar.csv"),
            start_date='01-01-2020')
p.barchart(os.path.join(os.path.dirname(__file__),
           "comparison_outputs/age_stratify.png"),
           write_Df_toFile=os.path.join(os.path.dirname(__file__),
           "comparison_outputs/gibraltar_daily_cases.csv"))
