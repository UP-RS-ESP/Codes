import sys
import numpy as np
from matplotlib import pyplot as pl
from matplotlib.colors import LogNorm

dd = float(sys.argv[1])
xb = np.arange(0, 4, dd)
x = xb[:-1] + dd / 2.0

Z = np.exp(-x*x)
R = x

Zp = -2 * R * Z
Zpp = (2 * R * R - 1) * 2 * Z
dZ = np.gradient(Z, dd)
ddZ = np.gradient(dZ, dd)

R = R[2:-2]
Zp = Zp[2:-2].flatten()
Zpp = Zpp[2:-2].flatten()
dZ = dZ[2:-2].flatten()
ddZ = ddZ[2:-2].flatten()

fig, axs = pl.subplots(2, 2)
axs = axs.flatten()

Zl = (Zp-dZ, (Zp-dZ)/Zp, Zpp-ddZ, (Zpp-ddZ)/Zpp)
title = ('abs diff gradient', 'rel diff gradient', 'abs diff laplace', 'rel diff laplace')

nbin = 100
bx = np.linspace(0, R.max(), nbin)
for i in range(4):
    D = Zl[i]
    if i == 3:
        Dmin, Dmax = np.percentile(D, 1), np.percentile(D, 99)
    else:
        Dmin, Dmax = 1.05 * D.min(), 1.1 * D.max()
    by = np.linspace(Dmin, Dmax, nbin)
    P, bx, by = np.histogram2d(R, D, bins = [bx, by], normed = True)
    Bx, By = np.meshgrid(bx, by)
    im = axs[i].pcolormesh(Bx, By, P.T, norm = LogNorm())
    cb = fig.colorbar(im, ax = axs[i])
    axs[i].axvline(np.sqrt(0.5), color = 'r')
    axs[i].set_ylabel(title[i])
    axs[i].set_xlabel('R')

#pl.savefig('%s.png' % sys.argv[0][:-3])
pl.show()

