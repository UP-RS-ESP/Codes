import sys
import numpy as np
from matplotlib import pyplot as pl

dd = float(sys.argv[1])
xb = np.arange(-1.1, 2.9, dd)
yb = np.arange(-1.2, 2.3, dd)
x = xb[:-1] + dd / 2.0
y = yb[:-1] + dd / 2.0
X, Y = np.meshgrid(x, y)
Xb, Yb = np.meshgrid(xb, yb)

Z = np.exp(-X*X-Y*Y)
Zp = -2 * np.sqrt(X*X+Y*Y) * Z
Zpp = (2 * (X*X+Y*Y) - 1) * 2 * Z
dy, dx = np.gradient(Z, dd)
dZ = -np.sqrt(dx*dx+dy*dy)
dy, _ = np.gradient(dy, dd)
_, dx = np.gradient(dx, dd)
ddZ = (dx + dy) / 2

fig, axs = pl.subplots(2, 2)
axs = axs.flatten()

Xb, Yb = Xb[2:-2, 2:-2], Yb[2:-2, 2:-2]

Zl = (Zp-dZ, (Zp-dZ)/Zp, Zpp-ddZ, (Zpp-ddZ)/Zpp)
title = ('abs diff gradient', 'rel diff gradient', 'abs diff laplace', 'rel diff laplace')
for i in range(4):
    axs[i].set_title(title[i])
    axs[i].set_aspect('equal')
    Zli = Zl[i]
    Zli = Zli[2:-2, 2:-2]
    im = axs[i].pcolormesh(Xb, Yb, Zli)
    cb = fig.colorbar(im, ax = axs[i])

#pl.savefig('%s.png' % sys.argv[0][:-3])
pl.show()

