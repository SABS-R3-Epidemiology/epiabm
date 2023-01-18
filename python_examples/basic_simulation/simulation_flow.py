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
pe.Parameters.set_file(os.path.join(os.path.dirname(__file__),
                       "simple_parameters.json"))

# Method to set the seed at the start of the simulation, for reproducibility

pe.routine.Simulation.set_random_seed(seed=42)

# Pop_params are used to configure the population structure being used in this
# simulation.

pop_params = {"population_size": 1000, "cell_number": 1,
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

# Need to close the writer object at the end of each simulation.
del sim.writer
del sim

# Creation of a plot of results (without logging matplotlib info)
logging.getLogger("matplotlib").setLevel(logging.WARNING)
filename = os.path.join(os.path.dirname(__file__), "simulation_outputs",
                        "output.csv")
df = pd.read_csv(filename)
df.plot(x="time", y=["InfectionStatus.Susceptible",
                     "InfectionStatus.InfectMild",
                     "InfectionStatus.Recovered"])
plt.savefig(
            os.path.join(os.path.dirname(__file__),
                         "simulation_outputs",
                         "simulation_flow_SIR_plot.png")
)
