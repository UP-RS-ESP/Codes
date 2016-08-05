#!/usr/bin/python2
import sys
import numpy as np
from netCDF4 import Dataset

if len(sys.argv) != 4:
    sys.exit('usage: %s file_name variable_name percentile' % sys.argv[0])

# parse arguments
fname = sys.argv[1]
vname = sys.argv[2]
perct = float(sys.argv[3])

# load data
f = Dataset(sys.argv[1], 'r')
lons = f.variables['lon'][:]
lats = f.variables['lat'][:]
precip = f.variables['r'][:]

# get temporal percentile for each grid cell
precip = np.percentile(precip, float(sys.argv[2]), axis = 0)

# data parsing via stdout -> stdin (piping)
lons, lats = np.meshgrid(lons, lats)
np.savetxt(sys.stdout, lons)
np.savetxt(sys.stdout, lats)
np.savetxt(sys.stdout, precip)
