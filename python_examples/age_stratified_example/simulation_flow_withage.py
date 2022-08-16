#
# Example simulation script with age stratification
#

import os
import logging
import pandas as pd
import matplotlib.pyplot as plt

import pyEpiabm as pe

from age_stratified_plot import Plotter  # noqa: E402

# Setup output for logging file
logging.basicConfig(filename='sim.log', filemode='w+', level=logging.DEBUG,
                    format=('%(asctime)s - %(name)s'
                            + '- %(levelname)s - %(message)s'))

# Set config file for Parameters
pe.Parameters.set_file(os.path.join(os.path.dirname(__file__),
                                    "simple_parameters_with_age.json"))

# Method to set the seed at the start of the simulation, for reproducibility

pe.routine.Simulation.set_random_seed(seed=42)

# Pop_params are used to configure the population structure being used in this
# simulation.

pop_params = {"population_size": 100, "cell_number": 1,
              "microcell_number": 1, "household_number": 5,
              "place_number": 2}

# Create a population based on the parameters given.
population = pe.routine.ToyPopulationFactory().make_pop(pop_params)

# sim_ and file_params give details for the running of the simulations and
# where output should be written to.
sim_params = {"simulation_start_time": 0, "simulation_end_time": 60,
              "initial_infected_number": 10}

file_params = {"output_file": "output_withage.csv",
               "output_dir": os.path.join(os.path.dirname(__file__),
                                          "simulation_outputs"),
               "spatial_output": False,
               "age_stratified": True}

# Create a simulation object, configure it with the parameters given, then
# run the simulation.
sim = pe.routine.Simulation()
sim.configure(
    population,
    [pe.sweep.InitialInfectedSweep()],
    [
        pe.sweep.HouseholdSweep(),
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
filename = os.path.join(os.path.dirname(__file__), "simulation_outputs",
                        "output_withage.csv")
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
            "simulation_outputs/simulation_flow_SIR_plot.png"))

# Creation of a plot of results with age stratification
p = Plotter(os.path.join(os.path.dirname(__file__),
            "simulation_outputs/output_withage.csv"),
            start_date='01-01-2020')
p.barchart(os.path.join(os.path.dirname(__file__),
           "simulation_outputs/age_stratify.png"),
           write_Df_toFile=os.path.join(os.path.dirname(__file__),
           "simulation_outputs/daily_cases.csv"))
