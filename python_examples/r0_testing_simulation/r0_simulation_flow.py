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
             'stdev_infected': []}
for j in np.arange(0.0, 5.0, 0.5):
    pe.Parameters.instance().basic_reproduction_num  = j
    print('Set r0 to: {}'.format(
            pe.Parameters.instance().basic_reproduction_num))

    # Set population input file
    file_loc = os.path.join(os.path.dirname(__file__), "input.csv")

    number_deads = []
    for i in range(50):
        # Create a population based on the parameters given.
        population = pe.routine.FilePopulationFactory.make_pop(
                file_loc,  random_seed=i)


        # sim_params give details for the running of the simulations
        sim_params = {"simulation_start_time": 0, "simulation_end_time": 21,
                    "initial_infected_number": 1, "simulation_seed": i}

        file_params = {"output_file": "output_r0.csv",
                    "output_dir": os.path.join(os.path.dirname(__file__),
                                                "simulation_outputs"),
                    "spatial_output": True,
                    "age_stratified": True}

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

df = pd.DataFrame.from_dict(dict_info)
df.to_csv(os.path.join(os.path.dirname(__file__),
          f"simulation_outputs/R0_values.csv"))

##### plot
fig, ax = plt.subplots()
ax.errorbar(df['R0'], df['mean_infected'], yerr=df['stdev_infected'], fmt='o', capsize=5)

ax.set_xlabel('R0 input')
ax.set_ylabel('Number of infected individuals')
plt.savefig(os.path.join(os.path.dirname(__file__),
            f"simulation_outputs/R0_values.png"))



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