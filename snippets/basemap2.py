import sys
import numpy as np
from netCDF4 import Dataset
#import matplotlib as mpl
#mpl.use('Agg')
from matplotlib import pyplot as pl
from mpl_toolkits.basemap import Basemap

cmap = pl.cm.inferno

if len(sys.argv) != 4:
    sys.exit('usage: %s file_name variable_name percentile' % sys.argv[0])

# parse arguments
fname = sys.argv[1]
vname = sys.argv[2]
perct = float(sys.argv[3])

# load data
f = Dataset(fname, 'r')
lon = f.variables['lon'][:]
lat = f.variables['lat'][:]
var = f.variables[vname][:]

# get temporal percentile for each grid cell
var = np.percentile(var, perct, axis = 0)

lon, lat = np.meshgrid(lon, lat)

# basemap
fig = pl.figure(1, (20.48, 15.36))
bm = Basemap(projection='cyl', resolution = 'l',
            llcrnrlat = lat.min(), urcrnrlat = lat.max(),
            llcrnrlon = lon.min(), urcrnrlon = lon.max())
bm.shadedrelief()
bm.drawcoastlines()
bm.drawparallels(np.arange(-90.,91.,10.), labels = [1,0,0,0])
bm.drawmeridians(np.arange(-180.,181.,25.), labels = [0,0,1,1])
bm.contourf(lon, lat, var, 10,
      latlon = True, cmap = cmap, alpha = 0.5)
bm.colorbar()
pl.tight_layout()
pl.savefig('%s.png' % sys.argv[0][:-3])
