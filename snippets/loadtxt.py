import sys
import numpy as np
from matplotlib import pyplot as pl
from mpl_toolkits.mplot3d import Axes3D

np.random.seed(111)
n = 1000
xp = np.random.random(n)
yp = np.random.random(n)
zp = np.exp(-xp*xp-yp*yp)

x, y, z = np.loadtxt('csv.gz',
        delimiter = ',',
        usecols = (0, 1, 2),
        unpack = True)

fg, ax = pl.subplots(1, 1,
        subplot_kw = dict(projection = '3d'))
ax.scatter(x, y, z, c = z)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
pl.show()

x -= xp
y -= yp
z -= zp
fg, ax = pl.subplots(1, 1,
        subplot_kw = dict(projection = '3d'))
ax.scatter(x, y, z)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
pl.show()

x, y, z, r, g, b = np.loadtxt('csv.gz',
        delimiter = ',',
        unpack = True)

fg, ax = pl.subplots(1, 1,
        subplot_kw = dict(projection = '3d'))
ax.scatter(x, y, z, c = np.transpose((r, g, b)))
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
pl.show()
