#
# Example simulation script with intervention data output and visualisation
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

# Set population input file
file_loc = os.path.join(os.path.dirname(__file__), "input.csv")

# sim_params give details for the running of the simulations
sim_params = {"simulation_start_time": 0, "simulation_end_time": 50,
              "initial_infected_number": 1, "initial_infect_cell": True}

# Set parameter file
name_parameter_file = 'vaccination_parameters.json'

# Set config file for Parameters
pe.Parameters.set_file(os.path.join(os.path.dirname(__file__),
                       name_parameter_file))

##########
# Vaccination drops infectiousness and susceptibility by 80%

# Set output file
name_output_file = 'output_vaccination.csv'

# Method to set the seed at the start of the simulation, for reproducibility
pe.routine.Simulation.set_random_seed(seed=30)

# Create population
population = pe.routine.FilePopulationFactory.make_pop(file_loc,
                                                       random_seed=42)

# Configure population with input data
pe.routine.ToyPopulationFactory.add_places(population, 1)

# file_params give details for where output should be written to.
file_params = {"output_file": name_output_file,
               "output_dir": os.path.join(os.path.dirname(__file__),
                                          "intervention_outputs"),
               "spatial_output": True}

# Create a simulation object, configure it with the parameters given, then
# run the simulation.
sim = pe.routine.Simulation()
sim.configure(
    population,
    [pe.sweep.InitialInfectedSweep(),
     pe.sweep.InitialisePlaceSweep(),
     pe.sweep.InitialVaccineQueue()
     ],
    [
        pe.sweep.InterventionSweep(),
        pe.sweep.UpdatePlaceSweep(),
        pe.sweep.HouseholdSweep(),
        pe.sweep.PlaceSweep(),
        pe.sweep.SpatialSweep(),
        pe.sweep.QueueSweep(),
        pe.sweep.HostProgressionSweep()
     ],
    sim_params,
    file_params,
)
sim.run_sweeps()

# Need to close the writer object at the end of each simulation.
del sim.writer
del sim

# Creation of a plot of results
logging.getLogger("matplotlib").setLevel(logging.WARNING)

filename = os.path.join(os.path.dirname(__file__), "intervention_outputs",
                        "output_vaccination.csv")
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
                                 "InfectionStatus.Recovered": 'sum',
                                 "InfectionStatus.Vaccinated": 'sum'})
# Create plot to show SIR curves against time
df_sum_age.plot(y=["InfectionStatus.Susceptible",
                   "InfectionStatus.InfectMild",
                   "InfectionStatus.Recovered",
                   "InfectionStatus.Vaccinated"])
plt.savefig(
    os.path.join(os.path.dirname(__file__),
                 "intervention_outputs", "SIR_with_vaccination.png")
)
