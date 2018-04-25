import sys
import numpy as np
from matplotlib import pyplot as pl

typ = sys.argv[1]

xn, yn = 41, 31
xb = np.linspace(-1.0, 2.0, xn)
yb = np.linspace(-1.2, 1.8, yn)
x = xb[:-1] + abs(xb[1]-xb[0]) / 2.0
y = yb[:-1] + abs(yb[1]-xb[0]) / 2.0
X, Y = np.meshgrid(x, y)

Z = np.exp(-X*X-Y*Y)
if typ == 'slope':
    Z = -2 * np.sqrt(X*X+Y*Y) * Z
elif typ == 'curvature':
    Z = (2 * (X*X+Y*Y) - 1) * 2 * Z

Xb, Yb = np.meshgrid(xb, yb)
pl.pcolormesh(Xb, Yb, Z)
pl.axes().set_aspect('equal')
cb = pl.colorbar()
cb.set_label(typ)
pl.show()
