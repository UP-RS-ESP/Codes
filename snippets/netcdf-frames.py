#!/usr/bin/python2
import sys
import numpy as np
from netCDF4 import Dataset
from matplotlib import pyplot as plt
from mpl_toolkits.basemap import Basemap
from progressbar import ProgressBar

cmap = plt.cm.viridis

# parse arguments: file name and variable name
fname = sys.argv[1]
vname = sys.argv[2]

# load data
f = Dataset(fname, 'r')
lons = f.variables['lon'][:]
lats = f.variables['lat'][:]
fvar = f.variables[vname][:]
tlen = fvar.shape[0]
print '%s of %s has %i time frames' % (vname, fname, tlen)

lons, lats = np.meshgrid(lons, lats)
llcrnrlat = lats.min()
urcrnrlat = lats.max()
llcrnrlon = lons.min()
urcrnrlon = lons.max()
vmin = fvar.min()
vmax = fvar.max()
levels = np.linspace(vmin, vmax, 11)

# figures
i = 0
bar = ProgressBar(maxval = tlen).start()
for t in xrange(tlen):
    plt.figure(1, (12.80, 7.2))
    bm = Basemap(projection='cyl', resolution = 'l',
                llcrnrlat = llcrnrlat, urcrnrlat = urcrnrlat,
                llcrnrlon = llcrnrlon, urcrnrlon = urcrnrlon)
    bm.shadedrelief()
    bm.drawcoastlines()
    bm.drawparallels(np.arange(-90.,91.,5.), labels = [1,0,0,0])
    bm.drawmeridians(np.arange(-180.,181.,5.), labels = [0,0,1,1])
    bm.contourf(lons, lats, fvar[t], levels, cmap = cmap, latlon = True, alpha = 0.5)
    plt.colorbar()
    plt.savefig('%04d.png' % i)
    i += 1
    plt.clf()
    bar.update(t+1)

bar.finish()
