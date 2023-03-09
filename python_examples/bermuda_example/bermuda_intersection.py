import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import matplotlib.textpath
import matplotlib.patches
from matplotlib.font_manager import FontProperties


def main():
    fig = plt.figure(figsize=[8, 8])
    img_extent = (-64.9, -64.65, 32.25, 32.39)
# img = plt.imread(fname)

    ax = plt.axes(projection=ccrs.PlateCarree())
    plt.title('Bermuda Outline')
    ax.set_extent([-64.9, -64.64, 32.24, 32.39], crs=ccrs.PlateCarree())

    ax.coastlines()
    ax.gridlines()
    ax.stock_img()

    # Generate a matplotlib path representing the character "C".
    fp = FontProperties(family='DejaVu Sans', weight='bold')
    # logo_path = matplotlib.textpath.TextPath((-4.5e7, -3.7e7),
    #                                             'C', size=103250000, prop=fp)


    # Add the path as a patch, drawing black outlines around the text.
    # patch = matplotlib.patches.PathPatch(logo_path, facecolor='white',
    #                                         edgecolor='black', linewidth=10,
    #                                         transform=ccrs.PlateCarree())
    # ax.add_patch(patch)
    plt.show()


if __name__ == '__main__':
    main()