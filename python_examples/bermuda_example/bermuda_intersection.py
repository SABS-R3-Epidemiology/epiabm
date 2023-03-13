import cartopy.crs as ccrs
import matplotlib.pyplot as plt


def main():

    ax = plt.axes(projection=ccrs.PlateCarree())
    plt.title('Bermuda Outline')
    ax.set_extent([-65.2, -64.3, 31.9, 32.7], crs=ccrs.PlateCarree())

    ax.coastlines()
    ax.gridlines()
    ax.stock_img()

    plt.show()


if __name__ == '__main__':
    main()
