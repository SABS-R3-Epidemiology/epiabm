import pyEpiabm as pe
from pyEpiabm.parameters import Parameters
from pyEpiabm.simulation import Simulation


pop_params = {"population_size": 1000, "cell_number": 5,
              "microcell_number": 5, "household_number": 5,
              "if_households": True}

sim_params = {"simulation_start_time": 0, "simulation_end_time": 100}

file_params = {"output_file": "output.csv",
               "output_dir": "./simulation_outputs"}
Parameters.instance().time_steps_per_day = 1

run = Simulation()
run.configure(pop_params, sim_params, file_params)
run.population.cells[0].persons[0].infection_status = \
    pe.InfectionStatus.InfectMild
run.population.cells[0].persons[0].time_of_status_change = 10

run.run_sweeps()
