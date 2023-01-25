# Code to plot runtime from .txt file

import os
import pandas as pd
import matplotlib.pyplot as plt


def get_seconds(time_str):
    print('Time in mm:ss:', time_str)
    # split in  mm, ss
    mm, ss = time_str.split(':')
    return int(mm) * 60 + int(ss)


data_path = os.path.join(os.path.dirname(__file__), "Sim_Speeds.txt")

df = pd.read_csv(data_path, header=0, sep=r"\s\s+")
df['Seconds'] = df['Time'].apply(get_seconds)
print(df.head())

x = []
y = []

x = df['Pop size']
y = df['Seconds']


plt.plot(x, y, marker='o', c='g')
plt.title("Simulation time for basic simulation over 60 days")
plt.xlabel('Population Size')
plt.xscale('log')
plt.yscale('log')
plt.ylabel('time (s)')


plt.savefig(os.path.join(os.path.dirname(__file__),
            "sim_speeds_plots/", "basic_sim_speed_from_file.png"))


plt.show()
