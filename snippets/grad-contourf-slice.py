import sys
import numpy as np
from matplotlib import pyplot as pl

def level(v, n):
    vmin = v.min()
    vmax = v.max()
    if vmin < 0 and vmax < -vmin:
        vmax = -vmin
    return np.linspace(-vmax, vmax, n)

dd = float(sys.argv[1])
xb = np.arange(-1.1, 2.9, dd)
yb = np.arange(-1.2, 2.3, dd)
x = xb[:-1] + dd / 2.0
y = yb[:-1] + dd / 2.0
X, Y = np.meshgrid(x, y)
Xb, Yb = np.meshgrid(xb, yb)

fig, axs = pl.subplots(2, 2)#, figsize = (10.24, 7))

Z = np.exp(-X*X-Y*Y)
Zp = -2 * np.sqrt(X*X+Y*Y) * Z
Zpp = (2 * (X*X+Y*Y) - 1) * 2 * Z
dy, dx = np.gradient(Z, dd)
dZ = -np.sqrt(dx*dx+dy*dy)
dy, _ = np.gradient(dy, dd)
_, dx = np.gradient(dx, dd)
ddZ = (dx + dy) / 2

Zl = (dZ, ddZ)
label = ('Gradient', 'Laplacian')
for j in range(2):
    axs[j, 0].set_aspect('equal')
    im = axs[j, 0].pcolormesh(Xb, Yb, Zl[j])
    cb = fig.colorbar(im, ax = axs[j, 0])
    cb.set_label(label[j])

Zl = (Zp-dZ, Zpp-ddZ)
label = ('Slope - Gradient', 'Curvature - Laplacian')
for j in range(2):
    D = Zl[j]
    for k in range(j+1):
        D = D[1:-1, 1:-1]
    X = X[1:-1, 1:-1]
    Y = Y[1:-1, 1:-1]
    axs[j, 1].set_aspect('equal')
    im = axs[j, 1].contourf(X, Y, D, level(D, 10),
            cmap = pl.cm.seismic)
    cb = fig.colorbar(im, ax = axs[j, 1])
    cb.set_label(label[j])

fig.tight_layout()
#pl.savefig('%s.png' % sys.argv[0][:-3])
pl.show()

