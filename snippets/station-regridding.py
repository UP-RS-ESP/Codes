#!/usr/bin/python2
import sys
import numpy as np
from scipy.interpolate import griddata
from netCDF4 import Dataset
from matplotlib import pyplot as plt
from mpl_toolkits.basemap import Basemap

cmap = plt.cm.viridis

# netcdf file and variable names
fname = sys.argv[1]
vname = sys.argv[2]

f = Dataset(fname, 'r')
lons = f.variables['lon'][:]
lats = f.variables['lat'][:]
v = f.variables[vname][:]

# we loaded all times and take the spatial std
v = np.std(v, axis = 0)

llcrnrlat = lats.min()
urcrnrlat = lats.max()
llcrnrlon = lons.min()
urcrnrlon = lons.max()

xdim = len(lons)
ydim = len(lats)
lons, lats = np.meshgrid(lons, lats)

# samples from original grid
npts = 30
x = np.random.randint(xdim, size = npts)
y = np.random.randint(ydim, size = npts)
pts = np.transpose((lons[y, x], lats[y, x]))
var = v[y, x]

# new refined grid which is 10x finer in each dim
lons = np.linspace(llcrnrlon, urcrnrlon, 10 * xdim)
lats = np.linspace(llcrnrlat, urcrnrlat, 10 * ydim)
lons, lats = np.meshgrid(lons, lats)

# regridding
var = griddata(pts, var, (lons, lats), method = 'nearest')

# figure
bm = Basemap(projection='cyl', resolution = 'l',
             llcrnrlat = llcrnrlat, urcrnrlat = urcrnrlat,
             llcrnrlon = llcrnrlon, urcrnrlon = urcrnrlon)
bm.drawcoastlines()
bm.drawparallels(np.arange(-90.,91.,5.), labels = [1,0,0,0])
bm.drawmeridians(np.arange(-180.,181.,5.), labels = [0,0,1,1])
bm.pcolormesh(lons, lats, var, cmap = cmap, latlon = True)
plt.colorbar()
plt.show()
