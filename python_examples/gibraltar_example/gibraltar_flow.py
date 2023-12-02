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

# Add plotting functions to path
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

# Generate population from input file
# (Input converted from CovidSim with `microcell_conversion.py`)
file_loc = os.path.join(os.path.dirname(__file__),
                        "gibraltar_inputs", "gib_input.csv")
population = pe.routine.FilePopulationFactory.make_pop(file_loc,
                                                       random_seed=42)


# sim_ and file_params give details for the running of the simulations and
# where output should be written to.
sim_params = {"simulation_start_time": 0, "simulation_end_time": 90,
              "initial_infected_number": 100, "initial_infect_cell": True,
              "simulation_seed": 42}

file_params = {"output_file": "output_gibraltar.csv",
               "output_dir": os.path.join(os.path.dirname(__file__),
                                          "simulation_outputs"),
               "spatial_output": True,
               "age_stratified": True}

ih_file_params = {"output_dir": os.path.join(os.path.dirname(__file__),
                                             "simulation_outputs"),
                  "status_output": True,
                  "infectiousness_output": True}

# Create a simulation object, configure it with the parameters given, then
# run the simulation.
sim = pe.routine.Simulation()
sim.configure(
    population,
    [pe.sweep.InitialHouseholdSweep(),
     pe.sweep.InitialInfectedSweep(),
     pe.sweep.InitialisePlaceSweep(),
     pe.sweep.InitialDemographicsSweep(file_params)],
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
    ih_file_params
)
sim.run_sweeps()

# Need to close the writer object at the end of each simulation.
del (sim.writer)
del (sim)

# Creation of a plot of results (plotter from spatial_simulation_flow)
logging.getLogger("matplotlib").setLevel(logging.WARNING)
filename = os.path.join(os.path.dirname(__file__), "simulation_outputs",
                        "output_gibraltar.csv")
SIRdf = pd.read_csv(filename)
total = SIRdf[list(SIRdf.filter(regex='InfectionStatus.Infect'))]
SIRdf["Infected"] = total.sum(axis=1)
SIRdf = SIRdf.groupby(["time"]).agg(
                                {"InfectionStatus.Susceptible": 'sum',
                                 "Infected": 'sum',
                                 "InfectionStatus.Recovered": 'sum',
                                 "InfectionStatus.Dead": 'sum'})
SIRdf.rename(columns={"InfectionStatus.Susceptible": "Susceptible",
                      "InfectionStatus.Recovered": "Recovered"},
             inplace=True)

# Create plot to show SIR curves against time
SIRdf.plot(y=["Susceptible", "Infected", "Recovered"])
plt.savefig(os.path.join(os.path.dirname(__file__),
            "simulation_outputs/simulation_flow_SIR_plot.png"))

# Creation of a plot of results with age stratification
# if file_params["age_stratified"]:
p = Plotter(os.path.join(os.path.dirname(__file__),
            "simulation_outputs/output_gibraltar.csv"),
            start_date='18-03-2022', sum_weekly=True)
p.barchart(os.path.join(os.path.dirname(__file__),
           "simulation_outputs/age_stratify.png"),
           write_Df_toFile=os.path.join(os.path.dirname(__file__),
           "simulation_outputs/gibraltar_weeky_cases.csv"),
           param_file=os.path.join(os.path.dirname(__file__),
           "gibraltar_parameters.json"))
