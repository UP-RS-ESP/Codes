import sys
import numpy as np
from matplotlib import pyplot as pl

#dd = float(sys.argv[1])
dd = 0.01
xw = yw = 3

#xr = np.linspace(-1.5, 1.5)
#yr = np.linspace(-1.5, 1.5)
#xtr, ytr = np.meshgrid(xr, yr)
#xtr, ytr = xtr.flatten(), ytr.flatten()

phi = np.arange(0, 2*np.pi, 0.01)
rho = np.linspace(1, 2, len(phi))
xtr = rho * np.cos(phi)
ytr = rho * np.sin(phi)

for k in range(len(xtr)):
    x0 = xtr[k]
    y0 = ytr[k]
    xb = np.arange(x0, x0+xw, dd)
    yb = np.arange(y0, y0+yw, dd)
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

    fig, axs = pl.subplots(2, 3, figsize = (13.66, 7.68))
    axs = axs.flatten()
    Zl = (Zp-dZ, (Zp-dZ)/Zp, Zpp-ddZ, (Zpp-ddZ)/Zpp, Zp, Zpp)
    title = ('abs diff gradient', 'rel diff gradient', 'abs diff laplace', 'rel diff laplace', 'slope', 'curvature')
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
        axs[i].axis('off')

    for i in range(4, 6):
        axs[i].set_aspect('equal')
        axs[i].set_title(title[i])
        im = axs[i].pcolormesh(Xb, Yb, Zl[i])
        #cb = fig.colorbar(im, ax = axs[i])
        axs[i].axis('off')

    fig.tight_layout()
    pl.savefig('%04d.png' % k)
    #pl.clf()
    pl.close('all')
