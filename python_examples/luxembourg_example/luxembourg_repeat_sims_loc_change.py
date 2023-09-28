#
# Example simulation script running with Luxembourg parameters
# Incorporates both age and spatial stratification.
#

import os
import sys
import logging
import pandas as pd
import matplotlib.pyplot as plt
import random

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
                                    "luxembourg_parameters.json"))




# sim_ and file_params give details for the running of the simulations and
# where output should be written to.

# Parameter to change
seed_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


for i in range(len(seed_values)):
    # input = pd.read_csv('luxembourg_inputs/luxembourg_input_file.csv')
    # listofzeros = [0] * len(input['location_x'])
    # print(len(listofzeros))

    # # cell_number = 1664
    # cell_number = random.randint(1,22006)
    # print(cell_number)
    # index_list = input.index[(input['cell'] == cell_number) & (input['Susceptible']
    #                          != 0)].tolist()
    # print(index_list)
    # index = random.choice(index_list)
    # listofzeros[index] = 1
    # input['InfectMild'] = listofzeros
    # input.to_csv('luxembourg_adapted_input_current.csv', index=False)
    # # Generate population from input file
    # (Input converted from CovidSim with `microcell_conversion.py`)
    file_loc = os.path.join(os.path.dirname(__file__),
                            "luxembourg_inputs", "luxembourg_input_file.csv")

    population = pe.routine.FilePopulationFactory.make_pop(file_loc,
                                                           random_seed=42)

    name_output_file = 'population_output_simulation_loc_change_{}.csv'.format(
        seed_values[i])
    sim_params = {"simulation_start_time": 0, "simulation_end_time": 120,
                "initial_infected_number": 5, "initial_infect_cell": True,
                "simulation_seed": seed_values[i]}

    file_params = {"output_file": name_output_file,
                   "output_dir": os.path.join(os.path.dirname(__file__),
                                              "simulation_outputs/large_csv"),
                   "spatial_output": True,
                   "age_stratified": True}

# Create a simulation object, configure it with the parameters given, then
# run the simulation.
    sim = pe.routine.Simulation()
    sim.configure(
        population,
        [pe.sweep.InitialHouseholdSweep(),
         pe.sweep.InitialInfectedSweep(),
         pe.sweep.InitialisePlaceSweep()],
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
    # logging.getLogger("matplotlib").setLevel(logging.WARNING)
    # filename = os.path.join(os.path.dirname(__file__),
    #                         "simulation_outputs/large_csv",
    #                         "output_luxembourg.csv")
    # SIRdf = pd.read_csv(filename)
    # total = SIRdf[list(SIRdf.filter(regex='InfectionStatus.Infect'))]
    # SIRdf["Infected"] = total.sum(axis=1)
    # SIRdf = SIRdf.groupby(["time"]).agg(
    #                                 {"InfectionStatus.Susceptible": 'sum',
    #                                 "Infected": 'sum',
    #                                 "InfectionStatus.Recovered": 'sum',
    #                                 "InfectionStatus.Dead": 'sum'})
    # SIRdf.rename(columns={"InfectionStatus.Susceptible": "Susceptible",
    #                     "InfectionStatus.Recovered": "Recovered"},
    #             inplace=True)


# # Create plot to show SIR curves against time
# SIRdf.plot(y=["Susceptible", "Infected", "Recovered"])
# plt.savefig(os.path.join(os.path.dirname(__file__),
#             "simulation_outputs/simulation_flow_SIR_plot.png"))

# # Creation of a plot of results with age stratification
# # if file_params["age_stratified"]:
# p = Plotter(os.path.join(os.path.dirname(__file__),
#             "simulation_outputs/large_csv/output_luxembourg.csv"),
#             start_date='29-02-2020', sum_weekly=True)
# p.barchart(os.path.join(os.path.dirname(__file__),
#            "simulation_outputs/age_stratify.png"),
#            write_Df_toFile=os.path.join(os.path.dirname(__file__),
#            "simulation_outputs/luxembourg_weeky_cases.csv"),
#            param_file=os.path.join(os.path.dirname(__file__),
#            "luxembourg_parameters.json"))
