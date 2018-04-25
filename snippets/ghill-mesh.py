import sys
import numpy as np
from matplotlib import pyplot as pl

xn, yn = 41, 31
xb = np.linspace(-1.0, 2.0, xn)
yb = np.linspace(-1.2, 1.8, yn)
x = xb[:-1] + abs(xb[1]-xb[0]) / 2.0
y = yb[:-1] + abs(yb[1]-xb[0]) / 2.0
X, Y = np.meshgrid(x, y)
Z = np.exp(-X*X-Y*Y)

if sys.argv[1] == 'mesh':
    Xb, Yb = np.meshgrid(xb, yb)
    pl.pcolormesh(Xb, Yb, Z)
    pl.colorbar()
    pl.savefig('%s-mesh.pdf' % sys.argv[0][:-3])
else:
    pl.contourf(X, Y, Z, levels = np.linspace(Z.min(), Z.max(), 4))
    pl.colorbar()
    pl.savefig('%s-contour.pdf' % sys.argv[0][:-3])
