import sys
import numpy as np
from matplotlib import pyplot as pl

xn, yn = 51, 51
xb = np.linspace(-1.0, 2.0, xn)
yb = np.linspace(-1.2, 1.8, yn)
dd = abs(xb[1]-xb[0])
x = xb[:-1] + dd / 2.0
y = yb[:-1] + dd / 2.0
X, Y = np.meshgrid(x, y)
Xb, Yb = np.meshgrid(xb, yb)

fig, axs = pl.subplots(2, 2, figsize = (10.24, 7.68))

i = 0
types = ('elevation', 'slope', 'curvature', 'gradient')
for j in range(2):
    for k in range(2):
        typ = types[i]
        Z = np.exp(-X*X-Y*Y)
        if typ == 'slope':
            Z = -2 * np.sqrt(X*X+Y*Y) * Z
        elif typ == 'curvature':
            Z = (2 * (X*X+Y*Y) - 1) * 2 * Z
        elif typ == 'gradient':
            dy, dx = np.gradient(Z, dd)
            Z = -np.sqrt(dx*dx+dy*dy)

        axs[j, k].set_aspect('equal')    
        im = axs[j, k].pcolormesh(Xb, Yb, Z)
        cb = fig.colorbar(im, ax = axs[j, k])
        cb.set_label(typ)
        i += 1

fig.tight_layout()
pl.savefig('%s.png' % sys.argv[0][:-3])
#pl.show()










