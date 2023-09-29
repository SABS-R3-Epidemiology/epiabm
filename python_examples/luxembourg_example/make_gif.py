import math
import glob
import os
from PIL import Image

import pandas as pd
import matplotlib.animation
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

sim_file = 'simulation_outputs/large_csv/population_output_simulation_1.csv'

delta = 0.008333

df = pd.read_csv(sim_file)
x_locs = sorted(list(set(df['location_x'])))
y_locs = sorted(list(set(df['location_y'])))

# Ensure that the grid is regular and contains all x and y values
# Note: this may fail if there is a discontinuity (i.e. a group of islands)

for i in range(len(x_locs) - 1):
    diff = x_locs[i+1] - x_locs[i]
    assert round(diff, 6) == delta

for i in range(len(y_locs) - 1):
    diff = y_locs[i+1] - y_locs[i]
    assert round(diff, 6) == delta

# Map geo coordinates to pixel indices

coord_map = {}

for i in range(len(x_locs)):
    x = x_locs[i]
    for j in range(len(y_locs)):
        y = y_locs[j]
        coord_map[f'{y}-{x}'] = (len(y_locs) - j - 1, i)


def generate_colour_map(df, name, min_value=0.0, cmap=cm.Reds):
    """Generates a given color map, with the max value determined by
    the max value in a given column of the provided dataframe.
    """
    max_inf = math.log(max(df[name])+1)
    cmap.set_under('lightgrey')
    norm = matplotlib.colors.Normalize(vmin=min_value, vmax=max_inf,
                                       clip=False)
    return cm.ScalarMappable(norm=norm, cmap=cmap)


def add_colorbar(im, width=None, pad=None, **kwargs):
    # From https://stackoverflow.com/a/76378778
    l, b, w, h = im.axes.get_position().bounds    # get boundaries
    width = width or 0.1 * w                      # get width of the colorbar
    pad = pad or width                            # get pad between im and cbar
    fig = im.axes.figure                          # get figure of image
    cax = fig.add_axes([l + w + pad, b, width, h])   # define cbar Axes
    # return fig.colorbar(im, cax=cax, **kwargs)       # draw cbar
    return fig.colorbar(cax=cax, **kwargs)       # draw cbar


def render_frame(ax, df, i, time, name, mapper, save_path='.'):
    print(f'Generating frame {i}')
    rows = df[df['time'] == time]
    img_grid = [[-1] * len(x_locs)] * len(y_locs)
    img_grid = np.array(img_grid)
    rows = zip(
        rows['location_x'],
        rows['location_y'],
        rows[name]
        # df['InfectionStatus.Recovered']
    )
    for row in rows:
        coords = f'{row[1]}-{row[0]}'
        idx = coord_map[coords]
        img_grid[idx] = math.log(row[2]+1)
    ax.set_title(f'Time = {time}')
    im = ax.imshow(img_grid, norm=mapper.norm, cmap=mapper.get_cmap())
    if i == 0:
        add_colorbar(im, mappable=mapper)
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # plt.show()
    # print('Saving')
    plt.savefig(f'{save_path}/frame-{i:03d}.png', bbox_inches='tight')


def make_gif(
        df,
        times,
        name='InfectionStatus.InfectMild',
        save_path='animation'
        ):
    # file_names = []

    mapper = generate_colour_map(df, name=name)
    ax = plt.axes()

    plt.axis('off')
    for i, t in enumerate(times):
        render_frame(ax, df, i, t, name, mapper, save_path)

    fp_in = f"{save_path}/frame-*.png"
    fp_name = sim_file.split('/')[-1].replace('.csv', '')
    fp_out = f"{save_path}/{fp_name}.gif"
    img, *imgs = [Image.open(f).convert("RGB")
                  for f in sorted(glob.glob(fp_in))]
    img.save(
        fp=fp_out,
        format="GIF",
        append_images=imgs,
        save_all=True,
        # duration=20,
        duration=100,
        loop=0,
        optimise=True,
    )
    for file in glob.glob(fp_in):  # Delete images after use
        os.remove(file)


# Sum infections over all age groups, etc.
df = df.groupby(['time', 'location_x', 'location_y'], as_index=False).sum()

times = sorted(list(set(df['time'])))
make_gif(df, times)
