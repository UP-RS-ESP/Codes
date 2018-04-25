import sys
import numpy as np
from matplotlib import pyplot as pl
from scipy.interpolate import griddata

def level(v, n):
    vmin = v.min()
    vmax = v.max()
    if vmin < 0 and vmax < -vmin:
        vmax = -vmin
    return np.linspace(-vmax, vmax, n)

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
Zi = np.exp(-X*X-Y*Y)
Xb, Yb = np.meshgrid(xb, yb)

xp = (xmax - xmin) * np.random.random(nm) + xmin
yp = (ymax - ymin) * np.random.random(nm) + ymin
zp = np.exp(-xp*xp-yp*yp)
noise = [0, np.abs(np.random.normal(0, 0.1, len(zp)))]

fig, ax = pl.subplots(1, 2)

for i in range(2):
    Z = griddata((xp, yp), zp+noise[i], (X, Y), method = method)
    Z = np.ma.masked_invalid(Z)
    im = ax[i].contourf(X, Y, Zi-Z, level(Zi-Z, 10), cmap = pl.cm.seismic)
    cb = fig.colorbar(im, ax = ax[i])
    ax[i].set_aspect('equal')
    ax[i].scatter(xp, yp, s = 5, c = 'g')
    ax[i].set_xlim((xmin, xmax))
    ax[i].set_ylim((ymin, ymax))

fig.tight_layout()
pl.show()
