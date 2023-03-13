import os
import matplotlib.pyplot as plt

from cartopy import config
import cartopy.crs as ccrs
import cartopy


fig = plt.figure(figsize=(8, 12))

# get the path of the file. It can be found in the repo data directory.
fname = os.path.join(config["repo_data_dir"],
                     'raster', 'sample', 'Miriam.A2012270.2050.2km.jpg'
                     )
img_extent = (-64.9, -64.65, 32.25, 32.39)
# img = plt.imread(fname)

ax = plt.axes(projection=ccrs.PlateCarree())
plt.title('Bermuda Outline')

ax.use_sticky_edges = False
# set a margin around the data
ax.set_xmargin(0.05)
ax.set_ymargin(0.10)
ax.set_extent([-64.9, -64.64, 32.24, 32.39], crs=ccrs.PlateCarree())

# add the image. Because this image was a tif, the "origin" of the image is in
# the upper left corner
ax.add_feature(cartopy.feature.LAND, color='moccasin')
ax.add_feature(cartopy.feature.OCEAN, color='cornflowerblue', alpha=0.6)
ax.add_feature(cartopy.feature.LAKES, color='cornflowerblue', alpha=0.9)
ax.add_feature(cartopy.feature.COASTLINE, linewidth=0.3)
ax.add_feature(cartopy.feature.BORDERS, linewidth=0.3)

ax.coastlines(resolution='10m', color='black', linewidth=1)

plt.show()

Coast = cartopy.feature.COASTLINE
print('Coast: ', Coast)
# plt.plot(Coast)
# plt.show()
