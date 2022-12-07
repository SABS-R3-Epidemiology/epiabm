import pyEpiabm as pe
import matplotlib.pyplot as plt
import numpy as np
import os

# Set config file for Parameters
pe.Parameters.set_file(os.path.join(os.path.dirname(__file__), os.pardir,
                       "simple_parameters_with_age.json"))

# Set population parameters
pop_params = {"population_size": 100000, "cell_number": 1,
              "microcell_number": 1, "household_number": 5,
              "place_number": 2}

# Create a population based on the parameters given.
population = pe.routine.ToyPopulationFactory().make_pop(pop_params)

xlist = []
# Create array of density of population by age
for cell in population.cells:
    for person in cell.persons:
        xlist.append(person.age)

x = np.array(xlist)

# Plot and save histogram
plt.figure(1)
plt.hist(x, density=False, rwidth=0.6, bins=17)
plt.ylabel('Count')
plt.xlabel('Age')
plt.title('Histogram of toy population')
plt.savefig('python_examples/age_stratified_example/age_hist/Withoutsim.png')

# Set simulation parameters
sim_params = {"simulation_start_time": 0, "simulation_end_time": 90,
              "initial_infected_number": 100, "initial_infect_cell": True,
              "simulation_seed": 42}

file_params = {"output_file": "output_gibraltar.csv",
               "output_dir": os.path.join(os.path.dirname(__file__),
                                          "simulation_outputs"),
               "spatial_output": True,
               "age_stratified": True}

# Run the simulation sweeps
sim = pe.routine.Simulation()
sim.configure(
    population,
    [pe.sweep.InitialHouseholdSweep()], [],
    sim_params,
    file_params,
)
sim.run_sweeps()

ylist = []
# Create array of density of population by age
for cell in population.cells:
    for person in cell.persons:
        ylist.append(person.age)

y = np.array(xlist)

# Plot and save histogram
plt.figure(2)
plt.hist(y, density=False, rwidth=0.6, bins=17)
plt.ylabel('Count')
plt.xlabel('Age')
plt.title('Histogram of toy population after simulation')
plt.savefig('python_examples/age_stratified_example/age_hist/Withsim.png')
plt.show()
