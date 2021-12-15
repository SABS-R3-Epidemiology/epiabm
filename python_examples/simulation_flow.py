import os
import pyEpiabm as pe
import pandas as pd
import random
import matplotlib.pyplot as plt
from pyEpiabm.place_type import PlaceType


pop_params = {"population_size": 100, "cell_number": 1,
              "microcell_number": 1, "household_number": 20,
              "if_households": True}

sim_params = {"simulation_start_time": 0, "simulation_end_time": 60}

file_params = {"output_file": "output.csv",
               "output_dir": "python_examples/simulation_outputs"}

pe.Parameters.instance().time_steps_per_day = 1

population = pe.ToyPopulationFactory().make_pop(**pop_params)
cell = population.cells[0]
# Intitialises 5 people as infectious randomly across the households
for _ in range(5):
    i = random.randint(0, pop_params["population_size"]-1)
    cell.persons[i].update_status(pe.InfectionStatus.InfectMild)
    cell.persons[i].time_of_status_change = random.randint(1, 10)

# initialise a place everyone's in
cell.microcells[0].add_place(1, (1.0, 1.0), PlaceType.Hotel)

sim = pe.Simulation()
sim.configure(
    population,
    [pe.UpdatePlaceSweep(), pe.HouseholdSweep(), pe.PlaceSweep(),
     pe.InitialInfectedSweep(), pe.HostProgressionSweep()],
    sim_params,
    file_params)
sim.run_sweeps()
del(sim.writer)
del(sim)

filename = os.path.join(os.path.dirname(__file__), "simulation_outputs",
                        "output.csv")
print(filename)
df = pd.read_csv(filename)
df.plot(x="time", y=["InfectionStatus.Susceptible",
                     "InfectionStatus.InfectMild",
                     "InfectionStatus.Recovered"])
plt.show()
