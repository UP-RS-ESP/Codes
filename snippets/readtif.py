#!/usr/bin/python2
import sys
import numpy as np
import gdal

f = gdal.Open(sys.argv[1])
z = f.ReadAsArray()

# print to stdout as integers
np.savetxt(sys.stdout, z, fmt='%i')
