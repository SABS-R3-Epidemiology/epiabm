import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Create R_t plots
filename = os.path.join(os.path.dirname(__file__), "simulation_outputs",
                        "secondary_infections.csv")
Rt_df = pd.read_csv(filename)
plt.plot(Rt_df["time"], Rt_df["R_t"])
plt.xlabel("Time")
plt.ylabel("R_t")
plt.title("R_t values over time with waning immunity")
# plt.show()
plt.savefig(os.path.join(os.path.dirname(__file__),
                         "simulation_outputs/simulation_flow_R_t.png"))
plt.clf()

# Create secondary infections histogram
plt.clf()
Rt_df.dropna()
secondary_infections_only = Rt_df.iloc[:, 2:-1].to_numpy()
secondary_infections_array = secondary_infections_only.flatten()
plt.hist(secondary_infections_array, range=(0, 10), log=True)
plt.ylabel("Number of secondary infections")
plt.title("Secondary infections per infectious period of a person")
# plt.show()
plt.savefig(os.path.join(os.path.dirname(__file__),
                         "simulation_outputs/"
                         "simulation_flow_secondary_infections.png"))
plt.clf()

# Create serial interval over time plot
serial_interval_df = pd.read_csv(
    "simulation_outputs/serial_intervals.csv",
    index_col=0)
plt.plot(np.arange(0.0, 90.0, 1.0),
         np.nanmean(serial_interval_df.to_numpy(), axis=0))
plt.xlabel("Time")
plt.ylabel("Mean serial interval")
plt.title("Mean serial interval over time")
# plt.show()
plt.savefig("simulation_outputs/simulation_flow_mean_serial_intervals.png")
plt.clf()

# Create serial interval histogram
serial_interval_df.dropna()
serial_interval_array = serial_interval_df.to_numpy().flatten()
plt.hist(serial_interval_array, range=(0, 30), log=True)
plt.ylabel("Number of serial intervals")
plt.title("Serial intervals")
# plt.show()
plt.savefig("simulation_outputs/"
            "simulation_flow_serial_intervals.png")
plt.clf()

# Create generation time over time plot
generation_time_df = pd.read_csv(
    "simulation_outputs/generation_times.csv",
    index_col=0)
plt.plot(np.arange(0.0, 90.0, 1.0),
         np.nanmean(generation_time_df.to_numpy(), axis=0))
plt.xlabel("Time")
plt.ylabel("Mean generation time")
plt.title("Mean generation time over time")
# plt.show()
plt.savefig("simulation_outputs/simulation_flow_mean_generation_times.png")
plt.clf()

# Create generation time histogram
generation_time_df.dropna()
generation_time_array = generation_time_df.to_numpy().flatten()
plt.hist(generation_time_array, range=(0, 30), log=True)
plt.ylabel("Number of generation times")
plt.title("Generation times")
# plt.show()
plt.savefig("simulation_outputs/"
            "simulation_flow_generation_times.png")
