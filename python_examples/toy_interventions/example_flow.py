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
    intervention = 'case_isolation'
    parameter = 'isolation_probability'
    parameter_values = [0.0, 0.5, 1.0]
    input_folder = "uniform_inputs/av{}_places".format(avplaces)
    output_folder = 'simulation_outputs'
    name_plot_multiple = 'MP_4_15_5av_CI_IP'

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

            if parameter is not None:
                for parameter_value in parameter_values:
                    output_file_name = "output_{}x{}_av{}_{}_{}_{}_{}.csv".\
                        format(grid_size, grid_size, avplaces, intervention,
                               parameter, parameter_value, i)

                    pe.Parameters.instance().intervention_params[
                        intervention][parameter] = parameter_value
                    print('set intervention param to {}'.format(
                        pe.Parameters.instance().intervention_params[
                            'case_isolation']['isolation_probability']))

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
    p = Plotter(output_folder, grid_sizes, avplaces, repeats, intervention,
                parameter, parameter_values)
    p._summarise_outputs()
    # p._plot_SIR('combined_{}x{}_av{}_{}_{}_{}.csv'.format(
    #     grid_sizes[0], grid_sizes[0], avplaces, intervention, parameter,
    #     parameter_values[0]))
    p._multiple_curve_plotter(name_plot_multiple)


def run_simulation(seed, file_loc, output_folder, output_file_name):
    population = pe.routine.FilePopulationFactory.make_pop(
                file_loc, random_seed=seed)

    # sim_ and file_params give details for the running of the
    # simulationsand where output should be written to.
    sim_params = {"simulation_start_time": 0,
                  "simulation_end_time": 60,
                  "initial_infected_number": 10,
                  "initial_infect_cell": True,
                  "simulation_seed": seed}

    file_params = {"output_file": output_file_name,
                   "output_dir": os.path.join(os.path.dirname(__file__),
                                              output_folder),
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


if __name__ == "__main__":
    main()
