#!/usr/bin/python2
import sys
import numpy as np
import pygrib

fname = sys.argv[1]

grb = pygrib.open(fname)
for g in grb:
    print g
