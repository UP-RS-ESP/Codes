import sys
import numpy as np
from matplotlib import pyplot as pl

dd = float(sys.argv[1])
xb = np.arange(-1.1, 2.9, dd)
yb = np.arange(-1.2, 2.3, dd)
x = xb[:-1] + dd / 2.0
y = yb[:-1] + dd / 2.0
X, Y = np.meshgrid(x, y)

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

Zl = (Zp-dZ, (Zp-dZ)/Zp, Zpp-ddZ, (Zpp-ddZ)/Zpp)
title = ('abs diff gradient', 'rel diff gradient', 'abs diff laplace', 'rel diff laplace')
for i in range(4):
    D = Zl[i]
    if i < 2:
        D = D[1:-1, 1:-1]
    else:
        D = D[2:-2, 2:-2]
    xmin, xmax = np.percentile(D, 5), np.percentile(D, 95)
    p, b = np.histogram(D, 'auto', density = True)
    x = b[:-1] + abs(b[0]-b[1])/2.
    axs[i].set_title(title[i])
    axs[i].plot(x, p)
    axs[i].set_xlim((xmin, xmax))

#pl.savefig('%s.png' % sys.argv[0][:-3])
pl.show()

