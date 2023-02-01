# Code to plot runtime from .txt file

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def get_seconds(time_str):
    """Converts a string for the time of a simulation of the form mm:ss
    into an integer value for the number of seconds that corresponds to

    Parameters
    ----------
    time_str : time string in form mm:ss

    Returns
    -------
    int
        Integer value of number of seconds for the given time string

    """
    mm, ss = time_str.split(':')  # split in  mm, ss
    return int(mm) * 60 + int(ss)


data_path = os.path.join(os.path.dirname(__file__), "Sim_Speeds.txt")

df = pd.read_csv(data_path, header=0, sep=r"\s\s+")
df['Seconds'] = df['Time'].apply(get_seconds)
print(df.head())

x = df['Pop size']
y = df['Seconds']

plt.plot(x, y, marker='o', c='g')
plt.title("Simulation time for basic simulation over 60 days")
plt.xlabel('Population Size')
plt.xscale('log')
plt.yscale('log')
plt.ylabel('time (s)')

slope, intercept = np.polyfit(np.log10(x), np.log10(y), 1)
print('The slope of the linear  regression line and so the big O power is: ',
      slope)
print(intercept)

plt.plot(x, 10**intercept*x**slope, c='b',
         label=("Regression gradient", slope))
plt.legend()

plt.savefig(os.path.join(os.path.dirname(__file__),
            "sim_speeds_plots/", "basic_sim_speed_from_file.png"))

plt.show()
