#
# Example simulation script running with Gibraltar parameters
# Incorporates both age and spatial stratification.
#

import os
import logging

import pyEpiabm as pe

# Setup output for logging file
logging.basicConfig(filename='sim.log', filemode='w+', level=logging.DEBUG,
                    format=('%(asctime)s - %(name)s'
                            + '- %(levelname)s - %(message)s'))

# Set config file for Parameters
pe.Parameters.set_file(os.path.join(os.path.dirname(__file__),
                                    "Int_params.json"))

input_file_names = ["toy_input_15x15_av5_places.csv",
                    "toy_input_4x4_av5_places.csv"]
output_file_names = ["output_15x15_av5_{}.csv", "output_4x4_av5_{}.csv"]

for j in range(len(input_file_names)):
    input_file = input_file_names[j]
    output_file = output_file_names[j]

    # Generate population from input file
    # (Input converted from CovidSim with `microcell_conversion.py`)
    file_loc = os.path.join(os.path.dirname(__file__),
                            "uniform_inputs/av5_places",
                            input_file)
    for i in range(10):
        set_seed = i
        population = pe.routine.FilePopulationFactory.make_pop(file_loc,
                                                               random_seed=i)

        # sim_ and file_params give details for the running of the simulations
        # and where output should be written to.
        sim_params = {"simulation_start_time": 0, "simulation_end_time": 60,
                      "initial_infected_number": 10,
                      "initial_infect_cell": True,
                      "simulation_seed": i}

        file_params = {"output_file": output_file.format(i),
                       "output_dir": os.path.join(os.path.dirname(__file__),
                                                  "simulation_outputs"),
                       "spatial_output": True,
                       "age_stratified": False}

        # Create a simulation object, configure it with the parameters given,
        # then run the simulation.
        sim = pe.routine.Simulation()
        sim.configure(
            population,
            [pe.sweep.InitialHouseholdSweep(),
                pe.sweep.InitialInfectedSweep(),
                pe.sweep.InitialisePlaceSweep()],
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
        del (sim.writer)
        del (sim)
