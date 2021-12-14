import sys
sys.path.append('../pyEpiabm')
import pyEpiabm as pe

pop_params = {"population_size": 100, "cell_number": 1,
              "microcell_number": 1, "household_number": 1,
              "if_households": True}

sim_params = {"simulation_start_time": 0, "simulation_end_time": 20}

file_params = {"output_file": "output.csv",
               "output_dir": "python_examples/simulation_outputs"}

pe.Parameters.instance().time_steps_per_day = 1

population = pe.ToyPopulationFactory().make_pop(**pop_params)

person1 = population.cells[0].persons[0]
person2 = population.cells[0].persons[1]
population.cells[0].persons[0].update_status(pe.InfectionStatus.InfectMild)
population.cells[0].persons[0].time_of_status_change = 10

# check everyone in one household - yes
# force of infection = 1 - yes
# everyone enqueued - yep, at each time step


print(person2.infection_status)
print(len(person1.household.persons))

sim = pe.Simulation()
sim.configure(
    population,
    [pe.HouseholdSweep(), pe.QueueSweep(), pe.HostProgressionSweep()],
    sim_params,
    file_params)

sim.run_sweeps()
