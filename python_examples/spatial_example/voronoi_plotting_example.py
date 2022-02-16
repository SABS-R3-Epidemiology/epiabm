#
# Reads in existing simulation output and visualises
# the spatial distribution using Voronoi tesselation.
#

import os
import math
import numpy as np
import pandas as pd
import matplotlib.animation
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy.spatial import Voronoi, voronoi_plot_2d

import glob
from PIL import Image


def find_value_for_region(current_df, point, name):
    """Extract value from given column for entry at given point.
    Requires a unique position (and so should only be passed data
    from a single point in time).

    :param current_df: Dataframe, for a single time point
    :type current_df: pd.Dataframe
    :param point: Location of given cell
    :type point: Tuple(float, float)
    :param name: Name of quantity to extract
    :type name: str
    :return: Named attribute of given cell
    :rtype: float
    """
    row = current_df.loc[(current_df['location_x'] == point[0])
                         & (current_df['location_y'] == point[1])]
    assert len(row[name]) == 1, "Multiple values found at point"
    assert name in current_df.columns.values, "Column name not in dataframe"
    return row[name].values[0]  # Change to plot other characteristic


def generate_colour_map(df, name, min_value=0.0, cmap=cm.Reds):
    """Generates a given color map, with the max value determined by
    the max value in a given column of the provided dataframe.

    :param df: Overall dataframe (from simulation output)
    :type df: pd.Dataframe
    :param name: Name of quantity to extract
    :type name: str
    :param min_value: Minimum value for colourmap
    :type min_value: float
    :param cmap: Colormap to use (default red)
    :type cmap: colormap
    :return: Mappable object to colour cells
    :rtype: ScalarMappable object

    """
    max_inf = max(df[name])
    norm = matplotlib.colors.Normalize(vmin=min_value, vmax=max_inf, clip=True)
    return cm.ScalarMappable(norm=norm, cmap=cmap)


def find_time_points(time_series, num_times):
    """Returns a given number of time points from time series,
    with approximately equal spacing.

    :param time_series: Time values from simulation output
    :type time_series: pd.Series
    :param num_times: Number of values to extract
    :type num_times: int
    :return: Array of times to plot data at
    :rtype: ndarray
    """
    all_times = time_series.drop_duplicates()
    idx = np.round(np.linspace(0, len(all_times) - 1, num_times)).astype(int)
    return all_times.to_numpy()[idx]


def plot_time_point(df, vor, name, time, grid_lim, ax, mapper):
    """Returns figure object with a spatial plot of all cells in the Voronoi
    tesselation, colour coded by their value in column 'name' at a given time.

    :param df: Overall dataframe (from simulation output)
    :type df: pd.Dataframe
    :param vor: Voronoi tesselation object
    :type vor: voronoi object
    :param name: Name of quantity to extract
    :type name: str
    :param time: Time to plot spatial data from
    :type time: float
    :param grid_lim: Spatial extent of plots, in the form
        [[min_x, max_x], [min_y, max_y]]
    :type grid_lim: List
    :param ax: Axes object on which to plot data
    :type ax: Axes
    :param mapper: Mappable object to colour cells
    :type mapper: ScalarMappable object
    :return: Figure and axes objects with plotted data
    :rtype: Figure, Axes
    """
    current_data = df.loc[df['time'] == time]
    fig = voronoi_plot_2d(vor, ax=ax, show_points=False, show_vertices=False)

    # Colourcode each region according to infection rate
    for r, region in enumerate(vor.regions):
        if -1 not in region:
            point = vor.points[r]
            value = find_value_for_region(current_data, point, name=name)
            polygon = [vor.vertices[i] for i in region]
            ax.fill(*zip(*polygon), color=mapper.to_rgba(value))

    ax.set_aspect('equal')
    ax.set_title(f"t = {time:.2f}")
    ax.set_xlim(grid_lim[0][0], grid_lim[0][1])
    ax.set_ylim(grid_lim[1][0], grid_lim[1][1])
    return fig, ax


def plot_time_grid(df, vor, name, grid_dim, grid_lim, save_loc):
    """Plots a grid of spatial plot of all cells in the Voronoi
    tesselation, colour coded by their value in column 'name',
    for multiple times.

    :param df: Overall dataframe (from simulation output)
    :type df: pd.Dataframe
    :param vor: Voronoi tesselation object
    :type vor: voronoi object
    :param name: Name of quantity to extract
    :type name: str
    :param grid_dim: Size of grid of spatial plots
    :type grid_dim: Tuple(int, int)
    :param grid_lim: Spatial extent of plots, in the form
        [[min_x, max_x], [min_y, max_y]]
    :type grid_lim: List
    :param save_loc: Path of saved image
    :type save_loc: str
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
        plot_time_point(df, vor, name, t, grid_lim, axs[i], mapper)

    cbar = plt.colorbar(mapper, ax=axs.tolist())
    cbar.set_label("Number of " + str(name))
    plt.xlim(grid_lim[0][0], grid_lim[0][1])
    plt.ylim(grid_lim[1][0], grid_lim[1][1])
    plt.savefig(save_loc)


def generate_animation(df, vor, name, grid_lim, save_path, use_pillow=True):
    """Plots a grid of spatial plot of all cells in the Voronoi
    tesselation, colour coded by their value in column 'name',
    for numltiple times.

    Has the option to use PillowWriter to generate the animation
    on the fly, or generate the images separately and then compile
    into an animation (recommended for older machines).


    :param df: Overall dataframe (from simulation output)
    :type df: pd.Dataframe
    :param vor: Voronoi tesselation object
    :type vor: voronoi object
    :param name: Name of quantity to extract
    :type name: str
    :param grid_lim: Spatial extent of plots, in the form
        [[min_x, max_x], [min_y, max_y]]
    :type grid_lim: List
    :param save_path: Path to saved animation
    :type save_path: str
    :param use_pillow: Whether to use pillow to generate animations
        on the fly, or from temporary images stored in memory
    :type use_pillow: bool
    """
    # Generate colour map to use
    mapper = generate_colour_map(df, name=name)

    times = df["time"].to_numpy()
    times = np.unique(times)

    fig = plt.figure()
    ax = plt.axes(xlim=(grid_lim[0][0], grid_lim[0][1]),
                  ylim=(grid_lim[1][0], grid_lim[1][1]))

    def animate(i):
        temp_fig, temp_ax = plot_time_point(df, vor, name, i, grid_lim, ax,
                                            mapper)
        if i == 0:
            cbar = temp_fig.colorbar(mapper)
            cbar.set_label("Number of " + str(name))
        return temp_fig, temp_ax

    if use_pillow:
        ani = matplotlib.animation.FuncAnimation(fig, animate, frames=times,
                                                 init_func=lambda *args: None)
        writer = matplotlib.animation.PillowWriter(fps=4)
        ani.save((save_path + str("voronoi_animation.gif")), writer=writer)
    else:
        for t in times:
            t_fig, t_ax = plot_time_point(df, vor, name, t, grid_lim, ax,
                                          mapper)
            if t == times[0]:
                cbar = t_fig.colorbar(mapper)
                cbar.set_label("Number of " + str(name))
            t_ax.set_xlim(grid_lim[0][0], grid_lim[0][1])
            t_ax.set_ylim(grid_lim[1][0], grid_lim[1][1])
            t_fig.savefig(save_path + "image" + f'{t:03d}' + "d.png")

        fp_in = save_path + "image" + "*d.png"
        fp_out = save_path + "voronoi_animation.gif"
        img, *imgs = [Image.open(f) for f in sorted(glob.glob(fp_in))]
        img.save(fp=fp_out, format='GIF', append_images=imgs,
                 save_all=True, duration=200, loop=0)
        for file in os.listdir(save_path):  # Delete images after use
            if file.endswith('d.png'):
                os.remove(os.path.join(save_path, file))


# Read in the data from simulation output
filename = os.path.join(os.path.dirname(__file__), "spatial_outputs",
                        "output.csv")
df = pd.read_csv(filename)

locations = np.transpose(np.stack((df["location_x"], df["location_y"])))

max_x, max_y = np.ceil(np.amax(locations, axis=0))
min_x, min_y = np.floor(np.amin(locations, axis=0))
grid_limits = [[min_x, max_x], [min_y, max_y]]


# Add 4 distant dummy points to ensure all cells are finite
locations = np.append(locations, [[999, 999], [-999, 999],
                                  [999, -999], [-999, -999]], axis=0)

# Compute and plot Tesselation
vor = Voronoi(locations)

# Plot grid of time points
fig_loc = ("python_examples/spatial_example/spatial_outputs/"
           + "voronoi_grid_img.png")
plot_time_grid(df, vor, name="InfectionStatus.InfectMild",
               grid_dim=(2, 3), grid_lim=grid_limits, save_loc=fig_loc)

# Plot animation of simulation
animation_path = ("python_examples/spatial_example/spatial_outputs/")
anim = generate_animation(df, vor, name="InfectionStatus.InfectMild",
                          grid_lim=grid_limits, save_path=animation_path,
                          use_pillow=True)
