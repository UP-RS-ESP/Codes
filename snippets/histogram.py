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

Zl = (Zp-dZ, (Zp-dZ)/Zp, Zpp-ddZ, (Zpp-ddZ)/Zpp)
for i in range(4):
    D = Zl[i]
    if i < 2:
        D = D[1:-1, 1:-1]
    else:
        D = D[2:-2, 2:-2]
    u, v = np.percentile(D, 1), np.percentile(D, 99)
    D = D[D > u]
    D = D[D < v]
    p, b = np.histogram(D, 'auto', density = True)
    x = b[:-1] + abs(b[0]-b[1])/2.
    pl.plot(x, p)
    #pl.savefig('%s.png' % sys.argv[0][:-3])
    pl.show()

