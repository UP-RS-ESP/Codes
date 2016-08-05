#!/usr/bin/python2
import sys
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.basemap import Basemap

cmap = plt.cm.viridis

# data parsing via stdout -> stdin
var = np.loadtxt(sys.stdin)
h = var.shape[0] / 3
lons = var[:h, :]
lats = var[h:h*2, :]
z = var[h*2:, :]

# figure
bm = Basemap(projection='cyl', resolution = 'l',
            llcrnrlat = lats.min(), urcrnrlat = lats.max(),
            llcrnrlon = lons.min(), urcrnrlon = lons.max())
bm.shadedrelief()
bm.drawcoastlines()
bm.drawparallels(np.arange(-90.,91.,5.), labels = [1,0,0,0])
bm.drawmeridians(np.arange(-180.,181.,5.), labels = [0,0,1,1])
bm.contourf(lons, lats, z, 10, cmap = cmap, latlon = True, alpha = 0.9)
#bm.pcolormesh(lons, lats, z, cmap = cmap, latlon = True)
plt.colorbar()
plt.show()
