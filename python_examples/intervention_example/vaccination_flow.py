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
name_output_file = 'output_vaccination_comp.csv'

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

# ##########
# # Vaccination drops infectiousness and susceptibility by 50%

# # Set output file
# name_output_file = 'output_vaccination_50.csv'

# pe.Parameters.instance().intervention_params['vaccine_params'][
#     'vacc_inf_drop'] = 0.5
# pe.Parameters.instance().intervention_params['vaccine_params'][
#     'vacc_susc_drop'] = 0.5
# print('Set vaccine infectiousness & susceptibility scaling to: {}'.format(
#       pe.Parameters.instance().intervention_params['vaccine_params'][
#         'vacc_inf_drop']))

# # Method to set the seed at the start of the simulation, for reproducibility
# pe.routine.Simulation.set_random_seed(seed=30)

# # Create population
# population = pe.routine.FilePopulationFactory.make_pop(file_loc,
#                                                        random_seed=42)

# # Configure population with input data
# pe.routine.ToyPopulationFactory.add_places(population, 1)

# # file_params give details for where output should be written to.
# file_params = {"output_file": name_output_file,
#                "output_dir": os.path.join(os.path.dirname(__file__),
#                                           "intervention_outputs"),
#                "spatial_output": True}

# # Create a simulation object, configure it with the parameters given, then
# # run the simulation.
# sim = pe.routine.Simulation()
# sim.configure(
#     population,
#     [pe.sweep.InitialInfectedSweep(),
#      pe.sweep.InitialisePlaceSweep(),
#      pe.sweep.InitialVaccineQueue()
#      ],
#     [
#         pe.sweep.InterventionSweep(),
#         pe.sweep.UpdatePlaceSweep(),
#         pe.sweep.HouseholdSweep(),
#         pe.sweep.PlaceSweep(),
#         pe.sweep.SpatialSweep(),
#         pe.sweep.QueueSweep(),
#         pe.sweep.HostProgressionSweep()
#      ],
#     sim_params,
#     file_params,
# )
# sim.run_sweeps()

# # Need to close the writer object at the end of each simulation.
# del sim.writer
# del sim

# ##########
# # Vaccination drops infectiousness and susceptibility by 20%

# # Set output file
# name_output_file = 'output_vaccination_20.csv'

# pe.Parameters.instance().intervention_params['vaccine_params'][
#     'vacc_inf_drop'] = 0.2
# pe.Parameters.instance().intervention_params['vaccine_params'][
#     'vacc_susc_drop'] = 0.2
# print('Set vaccine infectiousness & susceptibility scaling to: {}'.format(
#       pe.Parameters.instance().intervention_params['vaccine_params'][
#         'vacc_inf_drop']))

# # Method to set the seed at the start of the simulation, for reproducibility
# pe.routine.Simulation.set_random_seed(seed=30)

# # Create population
# population = pe.routine.FilePopulationFactory.make_pop(file_loc,
#                                                        random_seed=42)

# # Configure population with input data
# pe.routine.ToyPopulationFactory.add_places(population, 1)

# # file_params give details for where output should be written to.
# file_params = {"output_file": name_output_file,
#                "output_dir": os.path.join(os.path.dirname(__file__),
#                                           "intervention_outputs"),
#                "spatial_output": True}

# # Create a simulation object, configure it with the parameters given, then
# # run the simulation.
# sim = pe.routine.Simulation()
# sim.configure(
#     population,
#     [pe.sweep.InitialInfectedSweep(),
#      pe.sweep.InitialisePlaceSweep(),
#      pe.sweep.InitialVaccineQueue()
#      ],
#     [
#         pe.sweep.InterventionSweep(),
#         pe.sweep.UpdatePlaceSweep(),
#         pe.sweep.HouseholdSweep(),
#         pe.sweep.PlaceSweep(),
#         pe.sweep.SpatialSweep(),
#         pe.sweep.QueueSweep(),
#         pe.sweep.HostProgressionSweep()
#      ],
#     sim_params,
#     file_params,
# )
# sim.run_sweeps()

# # Need to close the writer object at the end of each simulation.
# del sim.writer
# del sim

# Creation of a plot of results
logging.getLogger("matplotlib").setLevel(logging.WARNING)

filename = os.path.join(os.path.dirname(__file__), "intervention_outputs",
                        "output_vaccination_comp.csv")
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
#plt.savefig(os.path.join(os.path.dirname(__file__),
#            "simulation_outputs/simulation_flow_SIR_plot.png"))
#plt.legend(labels=(range(len(df.columns))), title="Cell")
#plt.title("Infection curves for multiple cells")
#plt.ylabel("Infected Population")
plt.savefig(
    os.path.join(os.path.dirname(__file__),
                 "intervention_outputs", "vacc_comp.png")
)

# dict_filenames = {}
# for i in [80, 50, 20]:
#     dict_filenames["filename_" + str(i) + 'vaccination'] =\
#         os.path.join(os.path.dirname(__file__),
#                      "intervention_outputs",
#                      "output_vaccination_{}.csv".format(i))

# df_80vacc = pd.read_csv(dict_filenames['filename_80vaccination'])
# df_50vacc = pd.read_csv(dict_filenames['filename_50vaccination'])
# df_20vacc = pd.read_csv(dict_filenames['filename_20vaccination'])

# print(len(df_20vacc), len(df_50vacc), len(df_80vacc))

# total_vacc80 = \
#     df_80vacc[list(df_80vacc.filter(
#         regex='InfectionStatus.Infect'))]
# df_80vacc["Infected"] = total_vacc80.sum(axis=1)
# df_80vacc = df_80vacc.groupby(["time"]).agg(
#                                 {"InfectionStatus.Susceptible": 'sum',
#                                  "Infected": 'sum',
#                                  "InfectionStatus.Recovered": 'sum',
#                                  "InfectionStatus.Dead": 'sum'})
# df_80vacc = df_80vacc.reset_index(level=0)

# total_vacc50 = \
#     df_50vacc[list(df_50vacc.filter(
#         regex='InfectionStatus.Infect'))]
# df_50vacc["Infected"] = total_vacc50.sum(axis=1)
# df_50vacc = df_50vacc.groupby(["time"]).agg(
#                                 {"InfectionStatus.Susceptible": 'sum',
#                                  "Infected": 'sum',
#                                  "InfectionStatus.Recovered": 'sum',
#                                  "InfectionStatus.Dead": 'sum'})
# df_50vacc = df_50vacc.reset_index(level=0)

# total_vacc20 = \
#     df_20vacc[list(df_20vacc.filter(
#         regex='InfectionStatus.Infect'))]
# df_20vacc["Infected"] = total_vacc20.sum(axis=1)
# df_20vacc = df_20vacc.groupby(["time"]).agg(
#                                 {"InfectionStatus.Susceptible": 'sum',
#                                  "Infected": 'sum',
#                                  "InfectionStatus.Recovered": 'sum',
#                                  "InfectionStatus.Dead": 'sum'})
# df_20vacc = df_20vacc.reset_index(level=0)

# plt.plot(df_80vacc['time'], df_80vacc['Infected'],
#          label='80% vaccine effectiveness')
# plt.plot(df_50vacc['time'], df_50vacc['Infected'],
#          label='50% vaccine effectiveness')
# plt.plot(df_20vacc['time'], df_20vacc['Infected'],
#          label='20% vaccine effectiveness')

# plt.legend()
# plt.title("Infection curves for vaccination effectiveness")
# plt.ylabel("Infected Population")
# plt.savefig(
#     os.path.join(os.path.dirname(__file__),
#                  "intervention_outputs",
#                  "vaccination_Icurve_plot.png")
# )
