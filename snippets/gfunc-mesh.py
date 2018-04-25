import sys
import numpy as np
from matplotlib import pyplot as pl

def elevations(x, y):
    return np.exp(-x*x-y*y)

def slopes(x, y):
    # mathematically this would be negative!
    return 2 * np.sqrt(x*x+y*y) * np.exp(-x*x-y*y)

def aspects(x, y):
    # in degree
    return np.arctan2(y, x) * 180 / np.pi

# dimension of grid nxn
n = int(sys.argv[1])

# sym grid limits for area 10
r0 = np.sqrt(10) / 2
xmin, xmax = -r0, r0
ymin, ymax = -r0, r0

# cell boundaries
xb = np.linspace(xmin, xmax, n+1)
yb = np.linspace(ymin, ymax, n+1)
xx, yy = np.meshgrid(xb, yb)

# cell center
x = xb[:-1] + 0.5 * abs(xb[1]-xb[0])
y = yb[:-1] + 0.5 * abs(yb[1]-yb[0])
x, y = np.meshgrid(x, y)

z = elevations(x, y)
s = slopes(x, y)
a = aspects(x, y)

# figure
fig, axs = pl.subplots(ncols = 3)

cf = axs[0].pcolormesh(xx, yy, z, cmap = pl.cm.viridis)
cb = fig.colorbar(cf, ax = axs[0])
cb.set_label('Elevation [m]')
#axs[0].set_title('')
axs[0].set_aspect('equal')

cf = axs[1].pcolormesh(xx, yy, s, cmap = pl.cm.inferno)
cb = fig.colorbar(cf, ax = axs[1])
cb.set_label('Slope')
#axs[1].set_title('')
axs[1].set_aspect('equal')

cf = axs[2].pcolormesh(xx, yy, a, cmap = pl.cm.hsv)
cb = fig.colorbar(cf, ax = axs[2])
cb.set_label('Aspect [Degree]')
#axs[2].set_title('')
axs[2].set_aspect('equal')

fig.tight_layout()
pl.show()
