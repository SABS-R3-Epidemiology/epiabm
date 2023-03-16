#
# Example simulation script running with Luxembourg parameters
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
                                    "luxembourg_parameters.json"))


# Parameter to change
diagonal_dist = 0.015
parameter_values = [2*diagonal_dist, 5*diagonal_dist,
                    10*diagonal_dist, 25*diagonal_dist]

for i in range(len(parameter_values)):
    name_output_file = 'output_{}.csv'.format(
        parameter_values[i])

    pe.Parameters.instance().infection_radius = parameter_values[i]
    print('Set radius to: {}'.format(pe.Parameters.instance(
                                    ).infection_radius))

    # Method to set the seed at the start of the simulation,
    # for reproducibility

    # Generate population from input file
    # (Input converted from CovidSim with `microcell_conversion.py`)
    file_loc = os.path.join(os.path.dirname(__file__),
                            "luxembourg_inputs", "luxembourg_adapted_input.csv")
    population = pe.routine.FilePopulationFactory.make_pop(file_loc,
                                                        random_seed=42)


    # sim_ and file_params give details for the running of the simulations and
    # where output should be written to.
    sim_params = {"simulation_start_time": 0, "simulation_end_time": 1,
                "initial_infected_number": 0, "initial_infect_cell": True,
                "simulation_seed": 42}

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
logging.getLogger("matplotlib").setLevel(logging.WARNING)

for i in range(len(parameter_values)):
    file_name = os.path.join(os.path.dirname(__file__),
                                "simulation_outputs/large_csv",
                                'output_{}.csv'.format(
                                parameter_values[i]))
    df = pd.read_csv(file_name)
    total_df = \
        df[list(df.filter(regex='InfectionStatus.Infect'))]
    df["Infected"] = total_df.sum(axis=1)
    df = df.groupby(["time"]).agg(
                {"InfectionStatus.Susceptible": 'sum',
                    "Infected": 'sum',
                    "InfectionStatus.Recovered": 'sum',
                    "InfectionStatus.Dead": 'sum'})
    df = df.reset_index(level=0)

    plt.plot(df['time'], df['Infected'], label='radius: {}'.format(parameter_values[i]))

plt.legend()
plt.title("Infection curves for different radii")
plt.ylabel("Infected Population")
plt.savefig(
    os.path.join(os.path.dirname(__file__),
                    "simulation_outputs",
                    "place_closure_radius_Icurve_plot.png"))
plt.clf()
