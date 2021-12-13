import sys
sys.path.append('../pyEpiabm')
import pyEpiabm as pe

pop_params = {"population_size": 1000, "cell_number": 5,
              "microcell_number": 5, "household_number": 5,
              "if_households": True}

sim_params = {"simulation_start_time": 0, "simulation_end_time": 100}

file_params = {"output_file": "output.csv",
               "output_dir": "./simulation_outputs"}

pe.Parameters.instance().time_steps_per_day = 1

population = pe.ToyPopulationFactory().make_pop(**pop_params)

### Never manually change infection_status
#sim.population.cells[0].persons[0].infection_status = \
#    pe.InfectionStatus.InfectMild
population.cells[0].persons[0].update_status(pe.InfectionStatus.InfectMild)
population.cells[0].persons[0].time_of_status_change = 10

sim = pe.Simulation()
sim.configure(population, sim_params, file_params)

sim.run_sweeps()
