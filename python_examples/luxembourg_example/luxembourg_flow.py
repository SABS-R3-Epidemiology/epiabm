#
# Example simulation script running with Luxembourg parameters
# Runs with initial infections seeded at the same starting location
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
# Parameter files are provided for no interventions and the interventions used
# in the Jupyter Notebook
# Parameter file for no interventions
pe.Parameters.set_file(os.path.join(os.path.dirname(__file__),
                                    "luxembourg_parameters.json"))
# Parameter file for intervenitons used in rural_v_urban.ipynb
# pe.Parameters.set_file(os.path.join(os.path.dirname(__file__),
#                                     "luxembourg_intervention_parameters.json"))

# sim_ and file_params give details for the running of the simulations and
# where output should be written to.
# Parameter to change
seed_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


# Input files are provided for both 0 and 5 initial infections at a
# specific location.
# For the case with 0 initial infections at a known location the
# commented out code will seed a single random infection at an
# unknown starting location
for i in range(len(seed_values)):
    # File for 5 initial infections in cell 1664
    file_loc = os.path.join(os.path.dirname(__file__),
                            "luxembourg_inputs",
                            "luxembourg_adapted_5_in_cell_input.csv")


# "initial_infected_number" gives the number of random initial infections at
# unknown locations
    sim_params = {"simulation_start_time": 0, "simulation_end_time": 120,
                  "initial_infected_number": 0, "initial_infect_cell": True,
                  "simulation_seed": seed_values[i]}


# # Case for single initial infection at unknown location
    # file_loc = os.path.join(os.path.dirname(__file__),
    #                         "luxembourg_inputs", "luxembourg_input_file.csv")
# # "initial_infected_number" gives the number of random initial infections at
# # unknown locations
    # sim_params = {"simulation_start_time": 0, "simulation_end_time": 120,
    #               "initial_infected_number": 1, "initial_infect_cell": True,
    #               "simulation_seed": seed_values[i]}

    population = pe.routine.FilePopulationFactory.make_pop(file_loc,
                                                           random_seed=42)

    name_output_file = 'population_output_simulation_{}.csv'.format(
        seed_values[i])

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
