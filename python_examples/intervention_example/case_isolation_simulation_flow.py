#
# Example simulation script with case isolation intervention data output
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
name_parameter_file = 'case_isolation_parameters.json'

# Set config file for Parameters
pe.Parameters.set_file(os.path.join(os.path.dirname(__file__),
                       name_parameter_file))

##########################
# 0% isolating probability
name_output_file = 'output_0isolate.csv'

# Set parameter
pe.Parameters.instance().intervention_params['case_isolation'][
    'isolation_probability'] = 0.0
print('Set isolation_probability to: {}'.format(
      pe.Parameters.instance().intervention_params['case_isolation'][
        'isolation_probability']))

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

###########################
# 50% isolating probability
name_output_file = 'output_50isolate.csv'

# Set parameter
pe.Parameters.instance().intervention_params['case_isolation'][
    'isolation_probability'] = 0.5
print('Set isolation_probability to: {}'.format(
      pe.Parameters.instance().intervention_params['case_isolation'][
        'isolation_probability']))

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

############################
# 100% isolating probability
name_output_file = 'output_100isolate.csv'

# Set parameter
pe.Parameters.instance().intervention_params['case_isolation'][
    'isolation_probability'] = 1.0
print('Set isolation_probability to: {}'.format(
      pe.Parameters.instance().intervention_params['case_isolation'][
        'isolation_probability']))

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
for i in [0, 50, 100]:
    dict_filenames["filename_" + str(i) + 'isolate'] =\
        os.path.join(os.path.dirname(__file__),
                     "intervention_outputs",
                     "output_{}isolate.csv".format(i))

df_0isolate = pd.read_csv(dict_filenames['filename_0isolate'])
df_50isolate = pd.read_csv(dict_filenames['filename_50isolate'])
df_100isolate = pd.read_csv(dict_filenames['filename_100isolate'])

total_0isolate = \
    df_0isolate[list(df_0isolate.filter(regex='InfectionStatus.Infect'))]
df_0isolate["Infected"] = total_0isolate.sum(axis=1)
df_0isolate = df_0isolate.groupby(["time"]).agg(
                                {"InfectionStatus.Susceptible": 'sum',
                                 "Infected": 'sum',
                                 "InfectionStatus.Recovered": 'sum',
                                 "InfectionStatus.Dead": 'sum'})
df_0isolate = df_0isolate.reset_index(level=0)

total_50isolate = \
    df_50isolate[list(df_50isolate.filter(regex='InfectionStatus.Infect'))]
df_50isolate["Infected"] = total_50isolate.sum(axis=1)
df_50isolate = df_50isolate.groupby(["time"]).agg(
                                {"InfectionStatus.Susceptible": 'sum',
                                 "Infected": 'sum',
                                 "InfectionStatus.Recovered": 'sum',
                                 "InfectionStatus.Dead": 'sum'})
df_50isolate = df_50isolate.reset_index(level=0)

total_100isolate = \
    df_100isolate[list(df_100isolate.filter(regex='InfectionStatus.Infect'))]
df_100isolate["Infected"] = total_100isolate.sum(axis=1)
df_100isolate = df_100isolate.groupby(["time"]).agg(
                                {"InfectionStatus.Susceptible": 'sum',
                                 "Infected": 'sum',
                                 "InfectionStatus.Recovered": 'sum',
                                 "InfectionStatus.Dead": 'sum'})
df_100isolate = df_100isolate.reset_index(level=0)

plt.plot(df_0isolate['time'], df_0isolate['Infected'], label='0% isolating')
plt.plot(df_50isolate['time'], df_50isolate['Infected'],
         label='50% isolating')
plt.plot(df_100isolate['time'], df_100isolate['Infected'],
         label='100% isolating')

plt.legend()
plt.title("Infection curves for different isolating probabilities")
plt.ylabel("Infected Population")
plt.savefig(
    os.path.join(os.path.dirname(__file__),
                 "intervention_outputs", "case_isolation_Icurve_plot.png")
)
