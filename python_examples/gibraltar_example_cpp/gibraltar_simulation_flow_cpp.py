#
# Example simulation script with spatial data output and visualisation
#

import os
import logging
import sys
sys.path.append(os.path.abspath('../../pyEpiabm'))
sys.path.append(os.path.abspath('../../build_dir/src'))
import pyEpiabm as pe  # noqa: E402
import epiabm as ce  # noqa: E402

# Setup output for logging file
logging.basicConfig(filename='sim.log', filemode='w+', level=logging.DEBUG,
                    format=('%(asctime)s - %(name)s'
                            + '- %(levelname)s - %(message)s'))

# Set config file for Parameters
pe.Parameters.set_file(os.path.join(os.path.dirname(__file__),
                                    "gibraltar_parameters_py.json"))

# Generate population from input file
# (Input converted from CovidSim with `microcell_conversion.py`)
file_loc = os.path.join(os.path.dirname(__file__), "..", "gibraltar_example",
                        "gibraltar_inputs", "gib_input.csv")
population = pe.routine.FilePopulationFactory.make_pop(file_loc,
                                                       random_seed=42)


# sim_ and file_params give details for the running of the simulations and
# where output should be written to.
sim_params = {"simulation_start_time": 0, "simulation_end_time": 90,
              "initial_infected_number": 100, "initial_infect_cell": True,
              "simulation_seed": 42}

file_params = {"output_file": "output_gibraltar.csv",
               "output_dir": os.path.join(os.path.dirname(__file__),
                                          "simulation_outputs"),
               "spatial_output": True,
               "age_stratified": True}

initial_infect_sweep = pe.sweep.InitialInfectedSweep()
initial_infect_sweep.bind_population(population)
initialise_place_sweep = pe.sweep.InitialisePlaceSweep()
initialise_place_sweep.bind_population(population)
initial_infect_sweep(sim_params)
initialise_place_sweep(sim_params)

ce.LogFile.Instance().configure(1, "output/log.log")
# Set logger to print warnings and above to console
# LogFile.Instance().set_level(0)

# Load parameters to a SimulationConfig
cfg = ce.JsonFactory().load_config("gibraltar_parameters_cpp.json")

# Create a simulation object, configure it with the parameters given, then
# run the simulation.
c_factory = ce.PopulationFactory()
c_status_map = {
    pe.property.InfectionStatus.Dead: ce.InfectionStatus.Dead,
    pe.property.InfectionStatus.Exposed: ce.InfectionStatus.Exposed,
    pe.property.InfectionStatus.InfectASympt: ce.InfectionStatus.InfectASympt,
    pe.property.InfectionStatus.InfectGP: ce.InfectionStatus.InfectGP,
    pe.property.InfectionStatus.InfectHosp: ce.InfectionStatus.InfectHosp,
    pe.property.InfectionStatus.InfectICU: ce.InfectionStatus.InfectICU,
    pe.property.InfectionStatus.InfectICURecov: ce.InfectICURecov,
    pe.property.InfectionStatus.InfectMild: ce.InfectionStatus.InfectMild,
    pe.property.InfectionStatus.Recovered: ce.InfectionStatus.Recovered,
    pe.property.InfectionStatus.Susceptible: ce.InfectionStatus.Susceptible
}
logging.info("Converting python population to cpp.")
c_population = pe.py2c.py2c_convert_population(population, c_factory,
                                               c_status_map)

logging.info("Configuring cpp simulation")
simulation = ce.BasicSimulation(c_population)
# Create a simulation acting on the population

# Configure which sweeps to run
simulation.add_sweep(ce.HouseholdSweep(cfg))
simulation.add_sweep(ce.PlaceSweep(cfg))
simulation.add_sweep(ce.SpatialSweep(cfg))
simulation.add_sweep(ce.NewInfectionSweep(cfg))
simulation.add_sweep(ce.HostProgressionSweep(cfg))

# Configure what data to output
simulation.add_timestep_reporter(
    ce.PopulationCompartmentReporter("output/population_results.csv"))
simulation.add_timestep_reporter(
    ce.NewCasesReporter("output/new_cases.csv"))
simulation.add_timestep_reporter(
    ce.AgeStratifiedNewCasesReporter("output/age_stratified_new_cases.csv"))
simulation.add_timestep_reporter(
    ce.AgeStratifiedPopulationReporter(
        "output/age_stratified_population_results.csv"))

logging.info("Started cpp simulation")
simulation.simulate(sim_params["simulation_end_time"])
logging.info("Completed cpp simulation")
