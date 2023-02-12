#
# Example simulation script with social distancing intervention data output
# and visualisation
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
name_parameter_file = 'social_distancing_parameters.json'

# Set config file for Parameters
pe.Parameters.set_file(os.path.join(os.path.dirname(__file__),
                       name_parameter_file))

###############################
# Scale the spatial susceptibility by 0.1 for whole population
name_output_file = 'output_01spatial_susc.csv'

pe.Parameters.instance().intervention_params['social_distancing'][
    'distancing_spatial_susc'] = 0.1
print('Set distancing_spatial_susc to: {}'.format(
    pe.Parameters.instance().intervention_params['social_distancing'][
      'distancing_spatial_susc']))

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
    [pe.sweep.InitialInfectedSweep(), pe.sweep.InitialisePlaceSweep()],
    [
        pe.sweep.InterventionSweep(),
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
del sim.writer
del sim

###############################
# Scale the spatial susceptibility by 0.3 for whole population
name_output_file = 'output_03spatial_susc.csv'

pe.Parameters.instance().intervention_params['social_distancing'][
    'distancing_spatial_susc'] = 0.3
print('Set distancing_spatial_susc to: {}'.format(
    pe.Parameters.instance().intervention_params['social_distancing'][
      'distancing_spatial_susc']))

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
    [pe.sweep.InitialInfectedSweep(), pe.sweep.InitialisePlaceSweep()],
    [
        pe.sweep.InterventionSweep(),
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
del sim.writer
del sim

###############################
# Scale the spatial susceptibility by 0.9 for whole population
name_output_file = 'output_09spatial_susc.csv'

pe.Parameters.instance().intervention_params['social_distancing'][
    'distancing_spatial_susc'] = 0.9
print('Set distancing_spatial_susc to: {}'.format(
    pe.Parameters.instance().intervention_params['social_distancing'][
        'distancing_spatial_susc']))

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
    [pe.sweep.InitialInfectedSweep(), pe.sweep.InitialisePlaceSweep()],
    [
        pe.sweep.InterventionSweep(),
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
del sim.writer
del sim


###############################
# Creation of a plot of results
logging.getLogger("matplotlib").setLevel(logging.WARNING)

dict_filenames = {}
for i in ['01spatial_susc', '03spatial_susc',
          '09spatial_susc']:
    dict_filenames["filename_" + str(i)] =\
        os.path.join(os.path.dirname(__file__),
                     "intervention_outputs",
                     "output_{}.csv".format(i))


df_01spatial_susc = pd.read_csv(
    dict_filenames['filename_01spatial_susc'])
df_03spatial_susc = pd.read_csv(
    dict_filenames['filename_03spatial_susc'])
df_09spatial_susc = pd.read_csv(
    dict_filenames['filename_09spatial_susc'])


total_01spatial_susc = \
    df_01spatial_susc[list(df_01spatial_susc.filter(
        regex='InfectionStatus.Infect'))]
df_01spatial_susc["Infected"] = total_01spatial_susc.\
    sum(axis=1)
df_01spatial_susc = df_01spatial_susc.groupby(["time"]).\
    agg({"InfectionStatus.Susceptible": 'sum',
         "Infected": 'sum', "InfectionStatus.Recovered": 'sum',
         "InfectionStatus.Dead": 'sum'})
df_01spatial_susc = df_01spatial_susc.\
    reset_index(level=0)

total_03spatial_susc = \
    df_03spatial_susc[list(df_03spatial_susc.filter(
        regex='InfectionStatus.Infect'))]
df_03spatial_susc["Infected"] = total_03spatial_susc.\
    sum(axis=1)
df_03spatial_susc = df_03spatial_susc.groupby(["time"]).\
    agg({"InfectionStatus.Susceptible": 'sum',
         "Infected": 'sum', "InfectionStatus.Recovered": 'sum',
         "InfectionStatus.Dead": 'sum'})
df_03spatial_susc = df_03spatial_susc.\
    reset_index(level=0)

total_09spatial_susc = \
    df_09spatial_susc[list(df_09spatial_susc.filter(
        regex='InfectionStatus.Infect'))]
df_09spatial_susc["Infected"] = total_09spatial_susc.\
    sum(axis=1)
df_09spatial_susc = df_09spatial_susc.groupby(["time"]).\
    agg({"InfectionStatus.Susceptible": 'sum',
         "Infected": 'sum', "InfectionStatus.Recovered": 'sum',
         "InfectionStatus.Dead": 'sum'})
df_09spatial_susc = df_09spatial_susc.\
    reset_index(level=0)

plt.plot(df_01spatial_susc['time'],
         df_01spatial_susc['Infected'],
         label='spatial susceptibility scaled by 0.1')
plt.plot(df_03spatial_susc['time'],
         df_03spatial_susc['Infected'],
         label='spatial susceptibility scaled by 0.3')
plt.plot(df_09spatial_susc['time'],
         df_09spatial_susc['Infected'],
         label='spatial susceptibility scaled by 0.9')

plt.legend()
plt.title("Infection curves for different spatial susceptibility")
plt.ylabel("Infected Population")
plt.savefig(
    os.path.join(os.path.dirname(__file__),
                 "intervention_outputs",
                 "social_distancing_spatial_susc_Icurve_plot.png")
)
plt.clf()
