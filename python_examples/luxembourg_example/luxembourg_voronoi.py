#
# Reads in existing simulation output and visualises
# the spatial distribution using Voronoi tesselation.
#

import os
import math
import typing
import numpy as np
import pandas as pd
import matplotlib.animation
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy.spatial import Voronoi

import geopandas as gpd
from shapely import Polygon

import glob
from PIL import Image

import cartopy.crs as ccrs


def point_in_region(point: np.ndarray,
                    grid_lim: typing.List[typing.List[float]]):
    """Checks whether point is within grid limits specified.
    Used to exclude distant points from colouring.

    Parameters
    ----------
    point : np.ndarray
        Point to consider
    grid_lim : typing.List[typing.List[float]]
        Spatial extent of plots, in the form [[min_x, max_x], [min_y, max_y]]

    Returns
    -------
    bool
        Whether the point exists in the region

    """
    x_valid = (point[0] >= grid_lim[0][0]) & (point[0] <= grid_lim[0][1])
    y_valid = (point[1] >= grid_lim[1][0]) & (point[1] <= grid_lim[1][1])
    return x_valid & y_valid


def find_value_for_region(
    current_df: pd.DataFrame, point: typing.Tuple[float, float], name: str
):
    """Extract value from given column for entry at given point.
    Requires a unique position (and so should only be passed data
    from a single point in time).

    Parameters
    ----------
    current_df : pd.DataFrame
        DataFrame, for a single time point
    point : typing.Tuple[float, float]
        Location of given cell
    name : str
        Name of quantity to extract

    Returns
    -------
    float
        Named attribute of given cell

    """
    row = current_df.loc[
        (current_df["location_x"] == point[0])
        & (current_df["location_y"] == point[1])
    ]
    assert len(row[name]) > 0, "No value found for point"
    assert len(row[name]) == 1, "Multiple values found at point"
    assert name in current_df.columns.values, "Column name not in dataframe"
    return row[name].values[0]  # Change to plot other characteristic


def generate_colour_map(
    df: pd.DataFrame, name: str, min_value: float = 0.0, cmap: plt.cm = cm.Reds
):
    """Generates a given color map, with the max value determined by
    the max value in a given column of the provided dataframe.

    Parameters
    ----------
    df : pd.DataFrame
        Overall dataframe (from simulation output)
    name : str
        Name of quantity to extract
    min_value : float
        Minimum value of given quantity for colourmap
    cmap : colormap
        Colormap to use (default red)

    Returns
    -------
    ScalarMappable object
        Mappable object to colour cells

    """
    max_inf = max(df[name])
    norm = matplotlib.colors.Normalize(vmin=min_value, vmax=max_inf, clip=True)
    return cm.ScalarMappable(norm=norm, cmap=cmap)


def find_time_points(time_series: pd.Series, num_times: int):
    """Returns a given number of time points from time series,
    with approximately equal spacing.

    Parameters
    ----------
    time_series : pd.Series
        Time values from simulation output
    num_times : int
        Number of values to extract

    Returns
    -------
    np.ndarray
        Array of times where data should be plotted

    """
    all_times = time_series.drop_duplicates()
    idx = np.round(np.linspace(0, len(all_times) - 1, num_times)).astype(int)
    return all_times.to_numpy()[idx]


def plot_time_point(
    df: pd.DataFrame,
    vor: Voronoi,
    name: str,
    time: float,
    grid_lim: typing.List[typing.List[float]],
    ax: plt.Axes,
    mapper: plt.cm.ScalarMappable,
    country
):
    """Returns figure object with a spatial plot of all cells in the Voronoi
    tesselation, colour coded by their value in column 'name' at a given time.

    Parameters
    ----------
    df : pd.DataFrame
        Overall dataframe (from simulation output)
    vor : voronoi object
        Voronoi tesselation object
    name : str
        Name of quantity to extract
    time : float
        Time to plot spatial data from
    grid_lim : typing.List[typing.List[float]]
        Spatial extent of plots, in the form [[min_x, max_x], [min_y, max_y]]
    ax : Axes
        Axes object on which to plot data
    mapper : ScalarMappable object
        Mappable object to colour cells

    Returns
    -------
    Figure, Axes
        Figure and axes objects with plotted data

    """
    current_data = df.loc[df["time"] == time]
    fig = ax.figure
    ax.set_facecolor('lightgrey')

    finite_segments = []
    # Colourcode each region according to infection rate
    for r, region in enumerate(vor.regions):
        if r == 0:  # Vor.regions indexes from 1
            continue
        if -1 not in region:
            point_idx = np.where(vor.point_region == r)[0]
            if len(vor.points[point_idx]) == 0:
                continue
            point = vor.points[point_idx][0]
            if point_in_region(point, grid_lim):
                value = find_value_for_region(current_data, point, name=name)
                polygon = Polygon([vor.vertices[i] for i in region])
                intersect = polygon.intersection(country)[0]
                if isinstance(intersect, Polygon) is True:
                    polygon = intersect.exterior.coords
                    finite_segments.append(polygon)
                    ax.fill(*zip(*polygon), color=mapper.to_rgba(value))
                else:
                    for polygon in intersect.geoms:
                        polygon = polygon.exterior.coords
                        finite_segments.append(polygon)
                        ax.fill(*zip(*polygon), color=mapper.to_rgba(value))

    ax.set_aspect("equal")
    ax.set_title(f"t = {time:.2f}")
    ax.set_xlim(grid_lim[0][0], grid_lim[0][1])
    ax.set_ylim(grid_lim[1][0], grid_lim[1][1])
    return fig, ax


def plot_time_grid(
    df: pd.DataFrame,
    vor: Voronoi,
    name: str,
    grid_dim: typing.Tuple[float, float],
    grid_lim: typing.List[typing.List[float]],
    save_loc: str,
    country
):
    """Plots a grid of spatial plot of all cells in the Voronoi
    tesselation, colour coded by their value in column 'name',
    for multiple times.

    Parameters
    ----------
    df : pd.DataFrame
        Overall dataframe (from simulation output)
    vor : voronoi object
        Voronoi tesselation object
    name : str
        Name of quantity to extract
    grid_dim : typing.Tuple[float, float]
        Size of grid of spatial plots
    grid_lim : typing.List[typing.List[float]]
        Spatial extent of plots, in the form [[min_x, max_x], [min_y, max_y]]
    save_loc : str
        Path of saved image
    """
    # Generate colour map to use
    mapper = generate_colour_map(df, name=name)

    # Configure subplot grid
    fig, axs = plt.subplots(grid_dim[0], grid_dim[1], sharex=True, sharey=True)
    fig.subplots_adjust(hspace=0.3, wspace=0.15)
    axs = axs.ravel()

    # Determine time points to use
    plot_num = math.prod(grid_dim)
    times = find_time_points(df["time"], plot_num)

    # Add each subplot
    for i, t in enumerate(times):
        plot_time_point(df, vor, name, t, grid_lim, axs[i], mapper, country)

    cbar = plt.colorbar(mapper, ax=axs.tolist())
    cbar.set_label("Number of " + str(name))
    plt.xlim(grid_lim[0][0], grid_lim[0][1])
    plt.ylim(grid_lim[1][0], grid_lim[1][1])
    plt.savefig(save_loc)


def generate_animation(
    df: pd.DataFrame,
    vor: Voronoi,
    name: str,
    grid_lim: typing.List[typing.List[float]],
    save_path: str,
    country,
    use_pillow: bool = True,
):
    """Plots a grid of spatial plot of all cells in the Voronoi
    tesselation, colour coded by their value in column 'name',
    for multiple times.

    Has the option to use PillowWriter to generate the animation
    on the fly, or generate the images separately and then compile
    into an animation (recommended for older machines).


    Parameters
    ----------
    df : pd.DataFrame
        Overall dataframe (from simulation output)
    vor : voronoi object
        Voronoi tesselation object
    name : str
        Name of quantity to extract
    grid_lim : typing.List[typing.List[float]]
        Spatial extent of plots, in the form [[min_x, max_x], [min_y, max_y]]
    save_path : str
        Path to saved animation
    use_pillow : bool
        Whether to use pillow to generate animations on the fly,
        or from temporary images stored in memory
    """
    # Generate colour map to use
    mapper = generate_colour_map(df, name=name)

    times = df["time"].to_numpy()
    times = np.unique(times)

    fig = plt.figure()

    ax = plt.axes(projection=ccrs.PlateCarree())
    plt.title('Luxembourg Outline')

    ax.use_sticky_edges = False
    # set a margin around the data
    ax.set_xmargin(0.05)
    ax.set_ymargin(0.10)
    ax.set_extent([-65.2, -64.3, 31.9, 32.7], crs=ccrs.PlateCarree())

    def animate(i):
        temp_fig, temp_ax = plot_time_point(df, vor, name, i, grid_lim, ax,
                                            mapper, country)
        if i == 0:
            cbar = temp_fig.colorbar(mapper)
            cbar.set_label("Number of " + str(name))
        return temp_fig, temp_ax

    if use_pillow:
        ani = matplotlib.animation.FuncAnimation(
            fig, animate, frames=times, init_func=lambda *args: None
        )
        writer = matplotlib.animation.PillowWriter(fps=30)
        ani.save((save_path + str("voronoi_animation.gif")), writer=writer,
                 dpi=200)
    else:
        file_names = []
        for i, t in enumerate(times):
            t_fig, t_ax = plot_time_point(df, vor, name, t, grid_lim, ax,
                                          mapper, country)
            if t == times[0]:
                cbar = t_fig.colorbar(mapper)
                cbar.set_label("Number of " + str(name))
            t_ax.set_xlim(grid_lim[0][0], grid_lim[0][1])
            t_ax.set_ylim(grid_lim[1][0], grid_lim[1][1])
            file_name = ("image" + f'{i:03d}' + "d.png")
            file_names.append(file_name)
            t_fig.savefig(save_path + file_name)
            plt.close(t_fig)

        fp_in = save_path + "image" + "*d.png"
        fp_out = save_path + "voronoi_animation.gif"
        img, *imgs = [Image.open(f).convert("RGB")
                      for f in sorted(glob.glob(fp_in))]
        img.save(
            fp=fp_out,
            format="GIF",
            append_images=imgs,
            save_all=True,
            duration=50,
            loop=0,
            optimise=True,
        )
        for file in os.listdir(save_path):  # Delete images after use
            if file in file_names:
                os.remove(os.path.join(save_path, file))


df = gpd.read_file("ne_10m_admin_0_countries_lakes.zip")
lux = df.loc[df['ADMIN'] == 'Luxembourg'].geometry.to_list()

# Read in the data from simulation output
filename = os.path.join(os.path.dirname(__file__),
                        "simulation_outputs/large_csv",
                        "output_luxembourg.csv")
df_old = pd.read_csv(filename)
df = df_old.groupby(
    ['time', 'cell', 'location_x', 'location_y'], as_index=False).sum()

locations = np.unique(
    np.transpose(np.stack((df["location_x"], df["location_y"]))), axis=0
)

max_x, max_y = np.amax(locations, axis=0)
min_x, min_y = np.amin(locations, axis=0)
grid_limits = [[min_x, max_x], [min_y, max_y]]


# Add 4 distant dummy points to ensure all cells are finite
locations = np.append(
    locations, [[999, 999], [-999, 999], [999, -999], [-999, -999]], axis=0
)

# Compute and plot Tesselation
vor = Voronoi(locations)
# Plot grid of time points

fig_loc = ("simulation_outputs/"
           + "voronoi_grid_img.png")
plot_time_grid(
    df,
    vor,
    name="InfectionStatus.InfectMild",
    grid_dim=(3, 3),
    grid_lim=grid_limits,
    save_loc=fig_loc,
    country=lux
)

# Plot animation of simulation
animation_path = ("simulation_outputs/")
anim = generate_animation(df, vor, name="InfectionStatus.InfectMild",
                          grid_lim=grid_limits, save_path=animation_path,
                          country=lux, use_pillow=False)
