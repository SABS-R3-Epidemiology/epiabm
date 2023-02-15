#
# Example simulation script with data output
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
name_parameter_file = 'household_quarantine_parameters.json'

# Set config file for Parameters
pe.Parameters.set_file(os.path.join(os.path.dirname(__file__),
                       name_parameter_file))

###############################
# 0% quarantine house compliant
name_output_file = 'output_0hcompliant.csv'

pe.Parameters.instance().intervention_params['household_quarantine'][
    'quarantine_house_compliant'] = 0.0
print('Set quarantine_house_compliant to: {}'.format(
      pe.Parameters.instance().intervention_params['household_quarantine'][
        'quarantine_house_compliant']))

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

################################
# 50% quarantine house compliant
name_output_file = 'output_50hcompliant.csv'

pe.Parameters.instance().intervention_params['household_quarantine'][
    'quarantine_house_compliant'] = 0.5
print('Set quarantine_house_compliance to: {}'.format(
      pe.Parameters.instance().intervention_params['household_quarantine'][
        'quarantine_house_compliant']))

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

#################################
# 100% quarantine house compliant
name_output_file = 'output_100hcompliant.csv'

pe.Parameters.instance().intervention_params['household_quarantine'][
    'quarantine_house_compliant'] = 1.0
print('Set quarantine_house_compliance to: {}'.format(
      pe.Parameters.instance().intervention_params['household_quarantine'][
        'quarantine_house_compliant']))


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
    dict_filenames["filename_" + str(i) + 'hquarantine'] =\
        os.path.join(os.path.dirname(__file__),
                     "intervention_outputs",
                     "output_{}hcompliant.csv".format(i))

df_0hquarantine = pd.read_csv(dict_filenames['filename_0hquarantine'])
df_50hquarantine = pd.read_csv(dict_filenames['filename_50hquarantine'])
df_100hquarantine = pd.read_csv(dict_filenames['filename_100hquarantine'])

total_0hquarantine = \
    df_0hquarantine[list(df_0hquarantine.filter(
        regex='InfectionStatus.Infect'))]
df_0hquarantine["Infected"] = total_0hquarantine.sum(axis=1)
df_0hquarantine = df_0hquarantine.groupby(["time"]).agg(
                                {"InfectionStatus.Susceptible": 'sum',
                                 "Infected": 'sum',
                                 "InfectionStatus.Recovered": 'sum',
                                 "InfectionStatus.Dead": 'sum'})
df_0hquarantine = df_0hquarantine.reset_index(level=0)

total_50hquarantine = \
    df_50hquarantine[list(df_50hquarantine.filter(
        regex='InfectionStatus.Infect'))]
df_50hquarantine["Infected"] = total_50hquarantine.sum(axis=1)
df_50hquarantine = df_50hquarantine.groupby(["time"]).agg(
                                {"InfectionStatus.Susceptible": 'sum',
                                 "Infected": 'sum',
                                 "InfectionStatus.Recovered": 'sum',
                                 "InfectionStatus.Dead": 'sum'})
df_50hquarantine = df_50hquarantine.reset_index(level=0)

total_100hquarantine = \
    df_100hquarantine[list(df_100hquarantine.filter(
        regex='InfectionStatus.Infect'))]
df_100hquarantine["Infected"] = total_100hquarantine.sum(axis=1)
df_100hquarantine = df_100hquarantine.groupby(["time"]).agg(
                                {"InfectionStatus.Susceptible": 'sum',
                                 "Infected": 'sum',
                                 "InfectionStatus.Recovered": 'sum',
                                 "InfectionStatus.Dead": 'sum'})
df_100hquarantine = df_100hquarantine.reset_index(level=0)

plt.plot(df_0hquarantine['time'], df_0hquarantine['Infected'],
         label='0% house compliance')
plt.plot(df_50hquarantine['time'], df_50hquarantine['Infected'],
         label='50% house compliance')
plt.plot(df_100hquarantine['time'], df_100hquarantine['Infected'],
         label='100% house compliance')

plt.legend()
plt.title("Infection curves for different house quarantine compliant")
plt.ylabel("Infected Population")
plt.savefig(
    os.path.join(os.path.dirname(__file__),
                 "intervention_outputs",
                 "household_quarantine_Icurve_plot.png")
)
