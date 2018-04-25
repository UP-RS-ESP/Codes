import sys
import numpy as np
from netCDF4 import Dataset
from matplotlib import pyplot as pl

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
pl.contourf(lon, lat, var, 10, alpha = 0.5)
pl.colorbar()
pl.show()
