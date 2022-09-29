#
# Example simulation script running with Gibraltar parameters
# Incorporates both age and spatial stratification.
#

import logging
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import sys
from scipy.spatial import Voronoi

import pyEpiabm as pe

# Add plotting functions to path
sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir,
                "./age_stratified_example"))
from age_stratified_plot import Plotter  # noqa

# Add spatial plotter functions to path
sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir,
                "./spatial_example"))
from voronoi_plotting_example import voronoiPlotter  # noqa



# Creation of a plot of results (plotter from spatial_simulation_flow)
logging.getLogger("matplotlib").setLevel(logging.WARNING)
filename = os.path.join(os.path.dirname(__file__), "simulation_outputs",
                        "output_gibraltar.csv")
SIRdf = pd.read_csv(filename)
total = SIRdf[list(SIRdf.filter(regex='InfectionStatus.Infect'))]
SIRdf["Infected"] = total.sum(axis=1)
SIRdf.rename(columns={"InfectionStatus.Susceptible": "Susceptible",
                      "InfectionStatus.Recovered": "Recovered",
                      "InfectionStatus.Dead": "Dead"},
             inplace=True)
df_voronoi = SIRdf.copy()
SIRdf = SIRdf.groupby(["time"]).agg(
                                {"Susceptible": 'sum',
                                 "Infected": 'sum',
                                 "Recovered": 'sum',
                                 "Dead": 'sum'})


# Create a spatial voronoi plot
# Read in the data from simulation output
df = df_voronoi
df = df.groupby(["time", "cell", "location_x", "location_y"]).agg(
                                {"Susceptible": 'sum',
                                 "Infected": 'sum',
                                 "Recovered": 'sum'})

df = df.reset_index()
locations = np.unique(
    np.transpose(np.stack((df["location_x"], df["location_y"]))), axis=0
)

max_x, max_y = np.ceil(50*np.amax(locations, axis=0))/50
min_x, min_y = np.floor(50*np.amin(locations, axis=0))/50
grid_limits = [[min_x, max_x], [min_y, max_y]]

boarder_filepath = os.path.join(os.path.dirname(__file__),
                                "gibraltar_boarder.csv")

# Add 4 distant dummy points to ensure all cells are finite
locations = np.append(
    locations, [[999, 999], [-999, 999], [999, -999], [-999, -999]], axis=0
)
# Compute and plot Tesselation
vor = Voronoi(locations)

# Plot grid of time points
fig_loc = os.path.join(os.path.dirname(__file__), "simulation_outputs",
                       "voronoi_grid_img.png")
v = voronoiPlotter(boarder_filepath)

v.plot_time_grid(
    df,
    vor,
    name="Infected",
    grid_dim=(3, 3),
    grid_lim=grid_limits,
    save_loc=fig_loc,
)

# Plot animation of simulation
animation_path = os.path.join(os.path.dirname(__file__), "simulation_outputs/")
anim = v.generate_animation(df, vor, name="Infected",
                            grid_lim=grid_limits, save_path=animation_path,
                            use_pillow=False)
