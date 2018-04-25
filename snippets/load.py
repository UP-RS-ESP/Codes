import sys
import numpy as np
from matplotlib import pyplot as pl
from mpl_toolkits.mplot3d import Axes3D

np.random.seed(111)
n = 1000
xp = np.random.random(n)
yp = np.random.random(n)
zp = np.exp(-xp*xp-yp*yp)

f = np.load('archive.npz')
x = f['x']
y = f['y']
z = f['z'] 
c = f['c']

#print(np.mean(x), np.mean(y), np.mean(z))
#sys.exit()

fg, ax = pl.subplots(1, 1,
        subplot_kw = dict(projection = '3d'))
ax.scatter(x, y, z, c = c)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
pl.show()
