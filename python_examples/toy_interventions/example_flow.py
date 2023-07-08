#
# Example simulation script running with Gibraltar parameters
# Incorporates both age and spatial stratification.
#

import os
import logging

import pyEpiabm as pe

from toy_plotter import Plotter


def main():
    # set parameters
    repeats = 10
    grid_sizes = [4, 15]
    avplaces = 5
    input_folder = "uniform_inputs/av{}_places".format(avplaces)
    output_folder = 'simulation_outputs'

    # PARAMETERS TO STUDY
    # Note: always use age (use_age = 1, age_stratified = True)
    ##### CI
    # parameter_list = [{'case_isolation': {'isolation_probability': 0.0}},
    #                   {'case_isolation': {'isolation_probability': 0.5}},
    #                   {'case_isolation': {'isolation_probability': 1.0}}]
    # parameter_sets_labels = ['no_int', '0.5CI', 'CI']

    ##### HQ
    parameter_list = [{'household_quarantine': {'quarantine_house_compliant': 0}, 'case_isolation': {'isolation_probability': 0}},
                      {'household_quarantine': {'quarantine_house_compliant': 0}, 'case_isolation': {'isolation_probability': 1}},
                      {'household_quarantine': {'quarantine_house_compliant': 0.5}, 'case_isolation': {'isolation_probability': 1}},
                      {'household_quarantine': {'quarantine_house_compliant': 1.0}, 'case_isolation': {'isolation_probability': 1}}]
    parameter_sets_labels = ['no_int', 'CI', 'CI_0.5HQ', 'CI_HQ']
    
    #####  SD
    # parameter_list = [{'social_distancing': {'distancing_enhanced_prob': [0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0]}},
    #                   {'social_distancing': {'distancing_enhanced_prob': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 1.0, 1.0]}},
    #                   {'social_distancing': {'distancing_enhanced_prob': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]}}]
    # parameter_sets_labels = ['no_int', 'SD_eldery', 'SD']
    # # NOTE: set use_age to 1 and age_stratified to True

    ##### PC
    # parameter_list = [{'place_closure': {'closure_place_type': []}},
    #                   {'place_closure': {'closure_place_type': [1, 2, 3]}},
    #                   {'place_closure': {'closure_place_type': [1, 2, 3, 4, 5, 6]}}]
    # parameter_sets_labels = ['no_int', 'PC_schools', 'PC']
    # NOTE: set use_age to 1 and age_tratiefied to True

    ##### NZ
    # parameter_list = [{'case_isolation': {'start_time': 360}, 'place_closure': {'start_time': 360}, 'household_quarantine': {'start_time': 360}, 'social_distancing': {'start_time': 360}, 'travel_isolation': {'start_time': 360}},
    #               {'case_isolation': {'start_time': 0}, 'place_closure': {'start_time': 25}, 'household_quarantine': {'start_time': 0}, 'social_distancing': {'start_time': 49}, 'travel_isolation': {'start_time': 14}}]
    # parameter_sets_labels = ['no_int', 'NZ_int']
    # NOTE: set use_age to 1 and age_tratiefied to True
    # NOTE: read in the NZ parameters
    # NOTE: 90 days now instead of 120

    # Name output
    # name_plot_multiple = 'MP_4_15_5av_NZ_90d_csparam'
    # name_plot_bar = 'BP_4_15_5av_NZ_90d_csparam'
    name_plot_multiple = 'MP_4_15_5av_HQCI_90d'
    name_plot_bar = 'BP_4_15_5av_HQCI_90d'

    # Setup output for logging file
    logging.basicConfig(filename='sim.log', filemode='w+', level=logging.DEBUG,
                        format=('%(asctime)s - %(name)s'
                                + '- %(levelname)s - %(message)s'))

    # Set config file for Parameters
    pe.Parameters.set_file(os.path.join(os.path.dirname(__file__),
                           "Int_params.json"))

    for grid_size in grid_sizes:
        input_file_name = "toy_input_{}x{}_av{}_places.csv".format(
            grid_size, grid_size, avplaces)

        # Generate population from input file
        # (Input converted from CovidSim with `microcell_conversion.py`)
        file_loc = os.path.join(os.path.dirname(__file__), input_folder,
                                input_file_name)
        for i in range(repeats):
            print('Set seed to: {}'.format(i))

            if len(parameter_list) > 0:
                for j in range(len(parameter_list)):
                    output_file_name = "output_{}x{}_av{}_{}_{}.csv".\
                        format(grid_size, grid_size, avplaces,
                               parameter_sets_labels[j], i)
                # for parameter_value in parameter_values
                #     output_file_name = "output_{}x{}_av{}_{}_{}_{}_{}.csv".\
                #         format(grid_size, grid_size, avplaces, intervention,
                #                parameter, parameter_value, i)
                    for key_int in parameter_list[j].keys():
                        for key_param in parameter_list[j][key_int].keys():
                            pe.Parameters.instance().intervention_params[
                                key_int][key_param] = parameter_list[j][
                                    key_int][key_param]
                            print('set {} {} param to {}'.format(key_int,
                                  key_param,
                                  pe.Parameters.instance().intervention_params[
                                    key_int][key_param]))

                    # Run simulation
                    run_simulation(i, file_loc, output_folder,
                                   output_file_name)
            else:
                output_file_name = "output_{}x{}_av{}_{}.csv".\
                        format(grid_size, grid_size, avplaces, i)

                # Run simulation
                run_simulation(i, file_loc, output_folder,
                               output_file_name)

    # Plotting
    p = Plotter(output_folder, grid_sizes, avplaces, repeats,
                parameter_list, parameter_sets_labels)
    p._summarise_outputs()

    # p._plot_SIR('combined_{}x{}_av{}_{}_{}_{}.csv'.format(
    #     grid_sizes[0], grid_sizes[0], avplaces, intervention, parameter,
    #     parameter_values[0]))

    p._multiple_curve_plotter(name_plot_multiple)
    p._total_recovered_bars(name_plot_bar)


def run_simulation(seed, file_loc, output_folder, output_file_name):
    population = pe.routine.FilePopulationFactory.make_pop(
                file_loc, random_seed=seed)

    # Assign places
    pe.routine.ToyPopulationFactory.add_places(population, 1)

    # sim_ and file_params give details for the running of the
    # simulationsand where output should be written to.
    sim_params = {"simulation_start_time": 0,
                  "simulation_end_time": 90,
                  "initial_infected_number": 10,
                  "initial_infect_cell": True,
                  "simulation_seed": seed}

    file_params = {"output_file": output_file_name,
                   "output_dir": os.path.join(os.path.dirname(__file__),
                                              output_folder),
                   "spatial_output": True,
                   "age_stratified": True}

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


if __name__ == "__main__":
    main()
