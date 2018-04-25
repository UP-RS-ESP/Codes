import sys
import numpy as np
from matplotlib import pyplot as pl

#xn, yn = 51, 51
#xb = np.linspace(-1.0, 2.0, xn)
#yb = np.linspace(-1.2, 1.8, yn)
xb = np.arange(-1.1, 2.5, 0.01)
yb = np.arange(-1.2, 1.7, 0.01)
dd = abs(xb[1]-xb[0])
x = xb[:-1] + dd / 2.0
y = yb[:-1] + dd / 2.0
X, Y = np.meshgrid(x, y)
Xb, Yb = np.meshgrid(xb, yb)

Z = np.exp(-X*X-Y*Y)
dy, dx = np.gradient(Z, dd)

fg = pl.figure(1, (10.24, 7.68))
ax = fg.add_axes([0.1, 0.1, 0.8, 0.8])
ax.set_aspect('equal')
cs = ax.contour(X, Y, Z, 10, colors = 'k')
pl.clabel(cs)
im = ax.streamplot(X, Y, dx, dy,
        linewidth = 2*np.sqrt(dx*dx+dy*dy),
        #density = 2,
        color = np.sqrt(dx*dx+dy*dy),
        arrowstyle = '<|-')
cb = fg.colorbar(im.lines, ax = ax)
cb.set_label('gradient')

pl.savefig('%s.png' % sys.argv[0][:-3])
#pl.show()

