import sys
import numpy as np
from matplotlib import pyplot as pl

xn, yn = 41, 31
xb = np.linspace(-1.0, 2.0, xn)
yb = np.linspace(-1.2, 1.8, yn)
x = xb[:-1] + abs(xb[1]-xb[0]) / 2.0
y = yb[:-1] + abs(yb[1]-xb[0]) / 2.0
X, Y = np.meshgrid(x, y)
Xb, Yb = np.meshgrid(xb, yb)

fig, axs = pl.subplots(ncols = 3, figsize = (13, 3.2))

i = 0
for typ in ('elevation', 'slope', 'curvature'):
    Z = np.exp(-X*X-Y*Y)
    if typ == 'slope':
        Z = -2 * np.sqrt(X*X+Y*Y) * Z
    elif typ == 'curvature':
        Z = (2 * (X*X+Y*Y) - 1) * 2 * Z

    axs[i].set_aspect('equal')    
    im = axs[i].pcolormesh(Xb, Yb, Z)
    cb = fig.colorbar(im, ax = axs[i])
    cb.set_label(typ)
    i += 1

fig.tight_layout()
pl.savefig('%s.png' % sys.argv[0][:-3])
#pl.show()










