#
# Reads in existing simulation output and visualises
# the spatial distribution using Voronoi tesselation.
#

import os
import math
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy.spatial import Voronoi, voronoi_plot_2d


def find_value_for_region(current_df, point, name):
    """Extract value from given column for entry at given point.
    Requires a unique position (and so should only be passed data
    from a single point in time.
    """
    row = current_df.loc[(current_df['location_x'] == point[0])
                         & (current_df['location_y'] == point[1])]
    assert len(row[name]) == 1, "Multiple values found at point"
    assert name in current_df.columns.values, "Column name not in dataframe"
    return row[name].values[0]  # Change to plot other characteristic


def generate_colour_map(df, name, min_value=0, cmap=cm.Reds):
    """Generates a given colour map, with the max value determined by
    the max value in a given column of the provided dataframe.
    """
    max_inf = max(df[name])
    norm = matplotlib.colors.Normalize(vmin=min_value, vmax=max_inf, clip=True)
    return cm.ScalarMappable(norm=norm, cmap=cmap)


def find_time_points(time_series, num_times):
    """Returns a given number of time points from time series,
    with approximately equal spacing"""
    all_times = time_series.drop_duplicates()
    idx = np.round(np.linspace(0, len(all_times) - 1, num_times)).astype(int)
    return all_times.to_numpy()[idx]


def plot_time_point(df, vor, name, time, ax, mapper):
    """Returns figure object with a spatial plot of all cells in the Voroni
    tesselation, colour coded by their value in column 'name' at a given time.
    """
    current_data = df.loc[df['time'] == time]
    voronoi_plot_2d(vor, ax=ax, show_points=False, show_vertices=False)

    # Colourcode each region according to infection rate
    for r, region in enumerate(vor.regions):
        if -1 not in region:
            point = vor.points[r]
            value = find_value_for_region(current_data, point, name=name)
            polygon = [vor.vertices[i] for i in region]
            ax.fill(*zip(*polygon), color=mapper.to_rgba(value))


def plot_time_grid(df, vor, name, grid_dim, save_loc):
    """Plots a grid of spatial plot of all cells in the Voroni
    tesselation, colour coded by their value in column 'name',
    for numltiple times.
    """
    # Generate colour map to use
    mapper = generate_colour_map(df, name=name)

    # Configure subplot grid
    fig, axs = plt.subplots(grid_dim[0], grid_dim[1],
                            sharex=True, sharey=True)
    fig.subplots_adjust(hspace=0, wspace=.25)
    axs = axs.ravel()

    # Determine time points to use
    plot_num = math.prod(grid_dim)
    times = find_time_points(df["time"], plot_num)

    # Add each subplot
    for i, t in enumerate(times):
        plot_time_point(df, vor, name, t, axs[i], mapper)
        axs[i].set_aspect('equal')
        axs[i].set_title(f"t = {t:.2f}")
        axs[i].set_xlim(0, 1)
        axs[i].set_ylim(0, 1)

    cbar = plt.colorbar(mapper, ax=axs.tolist())
    cbar.set_label("Number of " + str(name))
    plt.savefig(save_loc)


# Read in the data from simulation output
filename = os.path.join(os.path.dirname(__file__), "spatial_outputs",
                        "output.csv")
df = pd.read_csv(filename)

locations = np.transpose(np.stack((df["location_x"], df["location_y"])))

# Add 4 distant dummy points to ensure all cells are finite
locations = np.append(locations, [[999, 999], [-999, 999],
                                  [999, -999], [-999, -999]], axis=0)

# Compute and plot Tesselation
vor = Voronoi(locations)

# Plot grid of time points
save_loc = ("python_examples/spatial_example/spatial_outputs/"
            + "voronoi_grid.png")
fig = plot_time_grid(df, vor, name="InfectionStatus.InfectMild",
                     grid_dim=(2, 3), save_loc=save_loc)
