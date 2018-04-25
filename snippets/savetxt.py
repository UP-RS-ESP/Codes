import sys
import numpy as np
from matplotlib import pyplot as pl

def rgb(v):
    nv = v.copy()
    nv -= nv.min()
    nv /= nv.max()
    c = pl.cm.plasma(nv)
    return c[:, :-1]

np.random.seed(111)
n = 1000
x = np.random.random(n)
y = np.random.random(n)
z = np.exp(-x*x-y*y)
c = rgb(z)
np.savetxt('csv.gz', np.transpose((x, y, z, c[:, 0], c[:, 1], c[:, 2])),
        fmt = '%.4f', delimiter = ', ',
        header = '   x,      y,      z,      r,      g,      b')
