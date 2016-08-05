#!/usr/bin/python2
import sys
import numpy as np
import pygrib
from matplotlib import pyplot as plt
from mpl_toolkits.basemap import Basemap
from progressbar import ProgressBar

cmap = plt.cm.viridis

if len(sys.argv) != 3:
    sys.exit('usage: %s filename \'variable name\'' % sys.argv[0])

fname = sys.argv[1]
vname = sys.argv[2]

# load data
grb = pygrib.open(fname)

# select vname
lst = grb.select(name = vname)
print 'got', len(lst), 'matches'

# check data frame
shape = lst[0].values.shape
vmin, vmax = 999999.9, -999999.9
for o in lst:
    if o.values.min() < vmin:
        vmin = o.values.min()
    if o.values.max() > vmax:
        vmax = o.values.max()
    if shape != o.values.shape:
        sys.exit('error: varying dimensions')
lats, lons = lst[0].latlons()

# figures
i = 0
bar = ProgressBar(maxval = len(lst)).start()
for l in lst:
    plt.figure(1, (12.80, 7.2))
    bm = Basemap(projection = 'kav7', lon_0 = 0, resolution = 'c')
    bm.drawcoastlines()
    bm.drawparallels(np.arange(-90, 91, 30), labels = [1,1,0,0])
    bm.drawmeridians(np.arange(-180, 181, 60), labels = [0,0,1,0])
    bm.pcolormesh(lons, lats, l.values, vmin = vmin, vmax = vmax, cmap = cmap, latlon = True)
    bm.colorbar(location = 'bottom')
    plt.savefig('%04d.png' % i)
    i += 1
    plt.clf()
    bar.update(i)

bar.finish()
