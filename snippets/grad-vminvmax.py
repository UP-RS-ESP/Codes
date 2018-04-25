import sys
import numpy as np
from matplotlib import pyplot as pl

xb = np.arange(-1.1, 2.9, 0.1)
yb = np.arange(-1.2, 2.3, 0.1)
dd = abs(xb[1]-xb[0])
x = xb[:-1] + dd / 2.0
y = yb[:-1] + dd / 2.0
X, Y = np.meshgrid(x, y)
Xb, Yb = np.meshgrid(xb, yb)

fig, axs = pl.subplots(2, 2)

Z = np.exp(-X*X-Y*Y)
Zp = -2 * np.sqrt(X*X+Y*Y) * Z
Zpp = (2 * (X*X+Y*Y) - 1) * 2 * Z
dy, dx = np.gradient(Z, dd)
dZ = -np.sqrt(dx*dx+dy*dy)
dy, _ = np.gradient(dy, dd)
_, dx = np.gradient(dx, dd)
ddZ = (dx + dy) / 2

Zl = (Zp, dZ)
label = ('Slope', 'Gradient')
vmin = min(Zp.min(), dZ.min())
vmax = max(Zp.max(), dZ.max())
for j in range(2):
    axs[j, 0].set_aspect('equal')
    im = axs[j, 0].pcolormesh(Xb, Yb, Zl[j],
            vmin = vmin, vmax = vmax)
    cb = fig.colorbar(im, ax = axs[j, 0])
    cb.set_label(label[j])

Zl = (Zpp, ddZ)
label = ('Curvature', 'Laplacian')
vmin = min(Zpp.min(), ddZ.min())
vmax = max(Zpp.max(), ddZ.max())
for j in range(2):
    axs[j, 1].set_aspect('equal')
    im = axs[j, 1].pcolormesh(Xb, Yb, Zl[j],
            vmin = vmin, vmax = vmax)
    cb = fig.colorbar(im, ax = axs[j, 1])
    cb.set_label(label[j])

fig.tight_layout()
#pl.savefig('%s.png' % sys.argv[0][:-3])
pl.show()

