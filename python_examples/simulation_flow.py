import os
import pyEpiabm as pe
import pandas as pd
import matplotlib.pyplot as plt


pop_params = {"population_size": 100, "cell_number": 1,
              "microcell_number": 1, "household_number": 1,
              "if_households": True}

sim_params = {"simulation_start_time": 0, "simulation_end_time": 40}

file_params = {"output_file": "output.csv",
               "output_dir": "python_examples/simulation_outputs"}

pe.Parameters.instance().time_steps_per_day = 1

population = pe.ToyPopulationFactory().make_pop(**pop_params)
population.cells[0].persons[0].update_status(pe.InfectionStatus.InfectMild)
population.cells[0].persons[0].time_of_status_change = 10

sim = pe.Simulation()
sim.configure(
    population,
    [pe.HouseholdSweep(), pe.QueueSweep(), pe.HostProgressionSweep()],
    sim_params,
    file_params)
sim.run_sweeps()
del(sim.writer)
del(sim)

filename = os.path.join(os.path.dirname(__file__), "simulation_outputs",
                        "output.csv")
print(filename)
df = pd.read_csv(filename)
df.plot(x="time", y=["InfectionStatus.Susceptible", "InfectionStatus.InfectMild",
        "InfectionStatus.Recovered"])
plt.show()
