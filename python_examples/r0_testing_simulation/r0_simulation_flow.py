#
# r0 testing simulation
#

import os
import logging
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import pyEpiabm as pe


# Setup output for logging file
logging.basicConfig(filename='sim.log', filemode='w+', level=logging.DEBUG,
                    format=('%(asctime)s - %(name)s'
                            + '- %(levelname)s - %(message)s'))

# Set config file for Parameters
pe.Parameters.set_file(os.path.join(os.path.dirname(__file__),
                                    "simple_parameters_with_age.json"))

dict_info = {'R0': [],
             'mean_infected': [],
             'stdev_infected': [],
             'mean_house': [],
             'sd_house': [],
             'mean_place': [],
             'sd_place': [],
             'mean_space': [],
             'sd_space': []}
for j in np.arange(0.0, 21.0, 1):
    pe.Parameters.instance().basic_reproduction_num  = j
    print('Set r0 to: {}'.format(
            pe.Parameters.instance().basic_reproduction_num))

    # Set population input file
    file_loc = os.path.join(os.path.dirname(__file__), "input.csv")

    number_deads = []
    house = []
    place = []
    space = []
    for i in range(1):
        # Create a population based on the parameters given.
        population = pe.routine.FilePopulationFactory.make_pop(
                file_loc,  random_seed=i)
        
        pe.routine.ToyPopulationFactory.add_places(population, 1)


        # sim_params give details for the running of the simulations
        sim_params = {"simulation_start_time": 0, "simulation_end_time": 21,
                    "initial_infected_number": 1, "simulation_seed": i}

        file_params = {"output_file": "output_r0.csv",
                    "output_dir": os.path.join(os.path.dirname(__file__),
                                                "simulation_outputs"),
                    "spatial_output": True,
                    "age_stratified": True}
        
        dead_house = []
        dead_place = []
        dead_space = []

        # Create a simulation object, configure it with the parameters given, then
        # run the simulation.
        sim = pe.routine.Simulation()
        sim.configure(
            population,
            [pe.sweep.InitialInfectedSweep(),
            pe.sweep.InitialisePlaceSweep()],
            [   
                pe.sweep.UpdatePlaceSweep(),
                pe.sweep.HouseholdSweep(),
                pe.sweep.QueueSweep(dead_house),
                pe.sweep.PlaceSweep(),
                pe.sweep.QueueSweep(dead_place),
                pe.sweep.SpatialSweep(),
                pe.sweep.QueueSweep(dead_space),
                pe.sweep.HostProgressionSweep(),
            ],
            sim_params,
            file_params,
        )
        sim.run_sweeps()

        # Need to close the writer object at the end of each simulation.
        del sim.writer
        del sim

        house.append(sum(dead_house))
        place.append(sum(dead_place))
        space.append(sum(dead_space))

        # Creation of a plot of results (plotter from spatial_simulation_flow)
        # logging.getLogger("matplotlib").setLevel(logging.WARNING)
        filename = os.path.join(os.path.dirname(__file__), "simulation_outputs",
                                "output_r0.csv")
        df_sum_age = pd.read_csv(filename)
        df_sum_age = df_sum_age.drop(["InfectionStatus.Exposed",
                                    "InfectionStatus.InfectASympt",
                                    "InfectionStatus.InfectGP",
                                    "InfectionStatus.InfectHosp",
                                    "InfectionStatus.InfectICU",
                                    "InfectionStatus.InfectICURecov"],
                                    axis=1)
        df_sum_age = df_sum_age.groupby(["time"]).agg(
                                        {"InfectionStatus.Susceptible": 'sum',
                                        "InfectionStatus.InfectMild": 'sum',
                                        "InfectionStatus.Recovered": 'sum',
                                        "InfectionStatus.Dead": 'sum'})
        number_deads.append(df_sum_age["InfectionStatus.Dead"].iloc[-1])

    # print(f'mean: {np.mean(number_deads)}')
    # print(f'standard devition: {np.std(number_deads)}')
    dict_info['R0'].append(j)
    dict_info['mean_infected'].append(np.mean(number_deads))
    dict_info['stdev_infected'].append(np.std(number_deads))
    dict_info['mean_house'].append(np.mean(house))
    dict_info['sd_house'].append(np.std(house))
    dict_info['mean_place'].append(np.mean(place))
    dict_info['sd_place'].append(np.std(place))
    dict_info['mean_space'].append(np.mean(space))
    dict_info['sd_space'].append(np.std(space))

df_sum_age.to_csv('simulation_outputs/r10.csv')

# df = pd.DataFrame.from_dict(dict_info)
# df.to_csv(os.path.join(os.path.dirname(__file__),
#           f"simulation_outputs/R0_values_all_high.csv"))

# ##### plot
# fig, ax = plt.subplots()
# ax.errorbar(df['R0'], df['mean_infected'], yerr=df['stdev_infected'], fmt='o', capsize=5)

# ax.set_xlabel('R0 input')
# ax.set_ylabel('Number of infected individuals')
# plt.savefig(os.path.join(os.path.dirname(__file__),
#             f"simulation_outputs/R0_values_high.png"))

# fig, ax = plt.subplots()
# ax.errorbar(df['R0'], df['mean_house'], yerr=df['sd_house'], fmt='o', capsize=5)

# ax.set_xlabel('R0 input')
# ax.set_ylabel('Number of infected individuals')
# plt.savefig(os.path.join(os.path.dirname(__file__),
#             f"simulation_outputs/R0_house_high.png"))

# fig, ax = plt.subplots()
# ax.errorbar(df['R0'], df['mean_place'], yerr=df['sd_place'], fmt='o', capsize=5)

# ax.set_xlabel('R0 input')
# ax.set_ylabel('Number of infected individuals')
# plt.savefig(os.path.join(os.path.dirname(__file__),
#             f"simulation_outputs/R0_place_high.png"))

# fig, ax = plt.subplots()
# ax.errorbar(df['R0'], df['mean_space'], yerr=df['sd_space'], fmt='o', capsize=5)

# ax.set_xlabel('R0 input')
# ax.set_ylabel('Number of infected individuals')
# plt.savefig(os.path.join(os.path.dirname(__file__),
#             f"simulation_outputs/R0_space_high.png"))




    # Create plot to show SIR curves against time
    # df_sum_age.plot(y=["InfectionStatus.Susceptible",
    #                    "InfectionStatus.InfectMild",
    #                    "InfectionStatus.Recovered",
    #                    "InfectionStatus.Dead"])
    # df_sum_age.plot(y=["InfectionStatus.InfectMild",
    #                 "InfectionStatus.Recovered",
    #                 "InfectionStatus.Dead"])
    # plt.savefig(os.path.join(os.path.dirname(__file__),
    #             f"simulation_outputs/simulation_flow_SIRD_plot_{i}.png"))