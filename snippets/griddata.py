import sys
import numpy as np
from matplotlib import pyplot as pl
from scipy.interpolate import griddata

nd = int(sys.argv[1])
nm = int(sys.argv[2])
method = sys.argv[3]

xmin, xmax = -2, 2
ymin, ymax = -1, 3

xb = np.linspace(xmin, xmax, nd+1)
yb = np.linspace(ymin, ymax, nd+1)
x = xb[:-1] + abs(xb[0]-xb[1]) / 2.0
y = yb[:-1] + abs(yb[0]-yb[1]) / 2.0
X, Y = np.meshgrid(x, y)
Xb, Yb = np.meshgrid(xb, yb)

xp = (xmax - xmin) * np.random.random(nm) + xmin
yp = (ymax - ymin) * np.random.random(nm) + ymin
zp = np.exp(-xp*xp-yp*yp)

Z = griddata((xp, yp), zp, (X, Y), method = method)
Z = np.ma.masked_invalid(Z)

pl.pcolormesh(xb, yb, Z)
pl.colorbar()
pl.axes().set_aspect('equal')
pl.scatter(xp, yp, s = 1, c = 'r')
pl.xlim((xmin, xmax))
pl.ylim((ymin, ymax))
pl.tight_layout()
pl.show()

