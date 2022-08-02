#
# Converts gibraltar population data from covidsim into compatible input file
#

import math
import os
import numpy as np
import pandas as pd

import pyEpiabm as pe


def min_separation(x_loc, y_loc):
    """Returns minimum separation between any pair of locations"""
    assert len(x_loc) == len(y_loc), "Mismatched coordinates"
    sep = np.inf

    for x1, y1 in zip(x_loc, y_loc):
        for x2, y2 in zip(x_loc, y_loc):
            if (x1 == x2) and (y1 == y2):
                continue
            if np.linalg.norm([x2-x1, y2-y1]) < sep:
                sep = np.linalg.norm([x2-x1, y2-y1])
    return sep


pe.Parameters.set_file(os.path.join(os.path.dirname(__file__), os.pardir,
                                    "gibraltar_parameters.json"))


mcell_num = 81
file_path = os.path.dirname(__file__)
columns = ["cell", "microcell", "location_x", "location_y",
           "household_number", "Susceptible"]

df = pd.read_csv(os.path.join(file_path, "wpop_gib.txt"),
                 skiprows=0,  delim_whitespace=True, header=0)

mcell_df = pd.DataFrame(columns=columns)
delta = min_separation(df['longitude'], df['latitude'])

for cell_index, row in df.iterrows():
    grid_len = math.ceil(math.sqrt(mcell_num))
    m_pos = np.linspace(0, 1, grid_len)

    # Multinomial population distribution
    mcell_pop = int(row["population"] / mcell_num)
    p = [1 / mcell_num] * mcell_num
    mcell_split = np.random.multinomial(row["population"], p, size=1)[0]

    # Household count - based on average household size
    hh_freq = pe.Parameters.instance().household_size_distribution
    ave_size = np.sum(np.multiply(np.array(range(1, len(hh_freq) + 1)),
                                  hh_freq))

    for n in range(mcell_num):
        x = (row["longitude"]
             + (m_pos[n % grid_len] - 0.5) * delta / grid_len)
        y = (row["latitude"]
             + (m_pos[n // grid_len] - 0.5) * delta / grid_len)

        data_dict = {"cell": cell_index,
                     "microcell": n,
                     "location_x": x,
                     "location_y": y,
                     "Susceptible": mcell_split[n],
                     "household_number": math.ceil(mcell_split[n] / ave_size)}

        new_row = pd.DataFrame(data=data_dict, columns=columns, index=[0])
        mcell_df = pd.concat([mcell_df, new_row], ignore_index=True, axis=0)

mcell_df.to_csv(os.path.join(file_path, "gib_input.csv"),
                header=True, index=False)
