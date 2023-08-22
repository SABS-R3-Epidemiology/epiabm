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
    for i in range(100):
        # Create a population based on the parameters given.
        population = pe.routine.FilePopulationFactory.make_pop(
                file_loc,  random_seed=i)
        
        # Assign places
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

        # Creation of a plot of results (plotter from spatial_simulation_flow)
        # logging.getLogger("matplotlib").setLevel(logging.WARNING)
        filename = os.path.join(os.path.dirname(__file__), "simulation_outputs",
                                "output_r0.csv")
        df_sum = pd.read_csv(filename)
        df_sum = df_sum.drop(["InfectionStatus.Exposed",
                              "InfectionStatus.InfectASympt",
                              "InfectionStatus.InfectGP",
                              "InfectionStatus.InfectHosp",
                              "InfectionStatus.InfectICU",
                              "InfectionStatus.InfectICURecov"],
                                    axis=1)
        df_sum = df_sum.groupby(["time"]).agg(
                                        {"InfectionStatus.Susceptible": 'sum',
                                        "InfectionStatus.InfectMild": 'sum',
                                        "InfectionStatus.Recovered": 'sum',
                                        "InfectionStatus.Dead": 'sum'})
        number_deads.append(df_sum["InfectionStatus.Dead"].iloc[-1])

        # Add total number of infections caused by one perso per category
        house.append(sum(dead_house))
        place.append(sum(dead_place))
        space.append(sum(dead_space))

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

df_sum.to_csv(os.path.join(os.path.dirname(__file__), 'simulation_outputs/spatial_infections_tuning_new.csv'))

df = pd.DataFrame.from_dict(dict_info)
df.to_csv(os.path.join(os.path.dirname(__file__),
          f"simulation_outputs/R0_values_all_new.csv"))

# Read in dataframe (for plotting)
# df = pd.read_csv(os.path.join(os.path.dirname(__file__),
#                  "simulation_outputs/spatial_infectiousness_output_all_R20_100rep.csv"))

# plot
def plot_infections(data, infected_columns_mean: list,
                    infected_columns_stdev: list, labels: list, colors: list,
                    file_name: str):
    fig, ax = plt.subplots()
    for k in range(len(infected_columns_mean)):
        ax.errorbar(data['R0'], data[infected_columns_mean[k]],
                    yerr=data[infected_columns_stdev[k]], fmt='o-', capsize=5,
                    label=labels[k], color=colors[k])
    ax.set_xlabel('Spatial infectiousness')
    ax.set_ylabel('Number of infected individuals')
    ax.grid(axis='y')
    plt.legend()

    # specify axis tick step sizes
    plt.xticks(np.arange(min(data['R0']), max(data['R0'])+1, 1))
    plt.savefig(os.path.join(os.path.dirname(__file__),
                    f"simulation_outputs/{file_name}.png"))

def plot_infections_mean_fit(data, infected_columns_mean: list,
                    infected_columns_stdev: list, labels: list, colors: list,
                    file_name: str):
    fig, ax = plt.subplots()
    for k in range(len(infected_columns_mean)):
        # if labels[k] in ['Total', 'Spatial']:
        slope, inter = np.polyfit(data['R0'], data[infected_columns_mean[k]], 1)
        ax.errorbar(data['R0'], slope*data['R0'] + inter, fmt='.-', color=colors[k])
        ax.errorbar(data['R0'], data[infected_columns_mean[k]],
                    fmt='o', capsize=5,
                    label=f'{labels[k]} ({np.round(slope,2)})', color=colors[k])
        # else: 
        #     ax.errorbar(data['R0'], data[infected_columns_mean[k]],
        #                 fmt='o', capsize=5,
        #                 label=labels[k], color=colors[k])
    ax.set_xlabel('Spatial infectiousness')
    ax.set_ylabel('Number of infected individuals')
    ax.grid(axis='both')
    plt.legend()

    # specify axis tick step sizes
    plt.xticks(np.arange(min(data['R0']), max(data['R0'])+1, 1))
    plt.savefig(os.path.join(os.path.dirname(__file__),
                    f"simulation_outputs/{file_name}.png"))


# Plots
# plot_infections(df, ['mean_infected'], ['stdev_infected'], ['Total'],
#                 ['midnightblue'], 'spatial_infectiousness_total')
# plot_infections(df, ['mean_house'], ['sd_house'], ['House'],
#                 ['slateblue'], 'spatial_infectiousness_house')
# plot_infections(df, ['mean_place'], ['sd_place'], ['Place'], ['cyan'],
#                 'spatial_infectiousness_place')
# plot_infections(df, ['mean_space'], ['sd_space'], ['Spatial'], ['mediumblue'],
#                 'spatial_infectiousness_spatial')
# plot_infections(df,
#                 ['mean_infected', 'mean_house', 'mean_place', 'mean_space'],
#                 ['stdev_infected', 'sd_house', 'sd_place', 'sd_space'],
#                 ['Total', 'House', 'Place', 'Spatial'],
#                 ['midnightblue', 'slateblue', 'cyan', 'mediumblue'],
#                 'spatial_infectiousness_all')

plot_infections_mean_fit(df,
                         ['mean_infected', 'mean_house', 'mean_place', 'mean_space'],
                         ['stdev_infected', 'sd_house', 'sd_place', 'sd_space'],
                         ['Total', 'House', 'Place', 'Spatial'],
                         ['midnightblue', 'slateblue', 'cyan', 'mediumblue'],
                         'spatial_infectiousness_all_withoutstdev_slope')