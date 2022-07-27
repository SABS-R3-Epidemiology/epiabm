#
# Example simulation script with data output and visualisation
#

import os
import logging
import pandas as pd
import matplotlib.pyplot as plt
from age_stratified_plot import Plotter
import pyEpiabm as pe

# Setup output for logging file
logging.basicConfig(filename='sim.log', filemode='w+', level=logging.DEBUG,
                    format=('%(asctime)s - %(name)s'
                            + '- %(levelname)s - %(message)s'))

# Set config file for Parameters
dirname = os.path.dirname(os.path.abspath(__file__))
paramfile = (dirname.split(os.sep)[1:-1])
paramfile.append("spatial_example/spatial_parameters.json")
paramfile = os.path.join('C:\\', *paramfile)
pe.Parameters.set_file(paramfile)

# Method to set the seed at the start of the simulation, for reproducibility

pe.routine.Simulation.set_random_seed(seed=42)

# Pop_params are used to configure the population structure being used in this
# simulation.

pop_params = {
    "population_size": 10000,
    "cell_number": 200,
    "microcell_number": 2,
    "household_number": 5,
}

# Create a population framework based on the parameters given.
population = pe.routine.ToyPopulationFactory.make_pop(pop_params)
pe.routine.ToyPopulationFactory.assign_cell_locations(population,
                                                      'uniform_x')

# Configure population with input data
pe.routine.ToyPopulationFactory.add_places(population, 1)
file_loc = (dirname.split(os.sep)[1:-1])
file_loc.append("age_stratified_example/input.csv")
file_loc = os.path.join('C:\\', *file_loc)
pe.routine.FilePopulationFactory.print_population(population, file_loc)


# sim_ and file_params give details for the running of the simulations and
# where output should be written to.
sim_params = {"simulation_start_time": 0, "simulation_end_time": 50,
              "initial_infected_number": 1, "initial_infect_cell": True}

file_params = {"output_file": "output.csv",
               "output_dir": "age_stratified_example/sim_outputs",
               "spatial_output": True,
               "age_stratified": True}

# Create a simulation object, configure it with the parameters given, then
# run the simulation.
sim = pe.routine.Simulation()
sim.configure(
    population,
    [pe.sweep.InitialInfectedSweep(), pe.sweep.InitialisePlaceSweep()],
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

# Creation of a plot of results (without logging matplotlib info)
logging.getLogger("matplotlib").setLevel(logging.WARNING)
filename = os.path.join(os.path.dirname(__file__), "simulation_outputs",
                        "output.csv")

age_list = [str(10*i)+"-"+str(10*i+10) for i in range((17))]
p = Plotter(os.path.join(dirname, "sim_outputs/output.csv"),
            start_date='01-01-2020',
            age_list=age_list)
p.barchart(os.path.join(dirname, "age_stratify.png"))
#plt.show()
#df = pd.read_csv(filename)
#df.plot(x="time", y=["InfectionStatus.Susceptible",
 #                    "InfectionStatus.InfectMild",
  #                   "InfectionStatus.Recovered"])
#plt.savefig("python_examples/simulation_outputs/simulation_flow_SIR_plot.png")
