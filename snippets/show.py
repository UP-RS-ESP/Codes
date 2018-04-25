import sys
import numpy as np
from matplotlib import pyplot as pl
from mpl_toolkits.mplot3d import Axes3D

np.random.seed(111)
n = 1000
x = np.random.random(n)
y = np.random.random(n)
z = np.exp(-x*x-y*y)

fg, ax = pl.subplots(1, 1,
        subplot_kw = dict(projection = '3d'))
ax.scatter(x, y, z, c = z)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
pl.show()
