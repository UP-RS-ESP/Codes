import sys
import numpy as np
from matplotlib import pyplot as pl
from scipy.interpolate import griddata
from progressbar import ProgressBar as pbar

def level(v, n):
    vmin, vmax = np.percentile(v, 10), np.percentile(v, 90)
    if vmin < 0 and vmax < -vmin:
        vmax = -vmin
    return np.linspace(-vmax, vmax, n)

def minfilter(xp, yp, zp, xb, yb):
    shape = (len(yb)-1, len(xb)-1)
    Z = np.zeros(shape)
    for i in range(shape[0]):
        for k in range(shape[1]):
            b = (xb[k] <= xp) * (xp < xb[k+1])
            b *= (yb[i] <= yp) * (yp < yb[i+1])
            if len(zp[b]) == 0:
                Z[i, k] = np.nan
            else:
                Z[i, k] = np.min(zp[b])
    
    return Z

def medianfilter(xp, yp, zp, xb, yb, method = 'linear'):
    shape = (len(yb)-1, len(xb)-1)
    t = np.zeros(len(zp), dtype = 'bool')
    for i in range(shape[0]):
        for k in range(shape[1]):
            b = (xb[k] <= xp) * (xp < xb[k+1])
            b *= (yb[i] <= yp) * (yp < yb[i+1])
            if len(zp[b]):
                m = np.median(zp[b])
                t += b * (zp <= m)

    # grid center
    dbx, dby = abs(xb[0]-xb[1]), abs(yb[0]-yb[1])
    x, y = xb[:-1] + dbx/2, yb[:-1] + dby/2
    X, Y = np.meshgrid(x, y)

    return griddata((xp[t], yp[t]), zp[t], (X, Y), method = method)

def radialfilter(xp, yp, zp, xb, yb, r = 1.0, method = 'linear'):
    n = len(zp)
    D = np.zeros((n, n))
    pb = pbar(maxval = n*(n-1)/2)
    pb.start()
    j = 0
    for i in range(n):
        for k in range(i):
            pb.update(j)
            j += 1
            dik = np.sqrt((xp[i]-xp[k])**2+(yp[i]-yp[k])**2)
            D[i, k] = D[k, i] = dik

    pb.finish()
    t = np.zeros(n, dtype = 'bool')
    for i in range(n):
        di = D[i, :]
        b = di <= r
        if len(zp[b]) > 5:
            m = np.median(zp[b])
            t += b * (zp <= m)

    # grid center
    dbx, dby = abs(xb[0]-xb[1]), abs(yb[0]-yb[1])
    x, y = xb[:-1] + dbx/2, yb[:-1] + dby/2
    X, Y = np.meshgrid(x, y)

    return griddata((xp[t], yp[t]), zp[t], (X, Y), method = method)

# grid setup
np.random.seed(35791)
method = 'cubic'
nopgc = 10
shape = (50, 50)
nop = nopgc * shape[0] * shape[1]
xmin, xmax = -2, 2
ymin, ymax = -2, 2
xb = np.linspace(xmin, xmax, shape[1]+1)
yb = np.linspace(ymin, ymax, shape[0]+1)
dbx, dby = abs(xb[0]-xb[1]), abs(yb[0]-yb[1])
x, y = xb[:-1] + dbx/2, yb[:-1] + dby/2
Xb, Yb = np.meshgrid(xb, yb)
X, Y = np.meshgrid(x, y)
Z = np.exp(-X*X-Y*Y)

# point clouds
xp = (xmax - xmin) * np.random.random(nop) + xmin
yp = (ymax - ymin) * np.random.random(nop) + ymin
zp = np.exp(-xp*xp-yp*yp)
noise = np.abs(np.random.normal(0, 0.02, nop))

Zs = [griddata((xp, yp), zp+noise, (X, Y), method = method),
      minfilter(xp, yp,  zp+noise, xb, yb),
      medianfilter(xp, yp, zp+noise, xb, yb, method = method),
      radialfilter(xp, yp, zp+noise, xb, yb, r = .2, method = method)]

label = ['Gridded zp+noise',
         'Minimum filter of zp+noise',
         'Median filter of zp+noise',
         'Radial filter of zp+noise']

fig, ax = pl.subplots(2, 2, figsize = (10.24, 7.68))
ax = ax.flatten()
for i in range(4):
    Zi = np.ma.masked_invalid(Zs[i])
    im = ax[i].contourf(X, Y, Z-Zi, level(Z-Zi, 50),
            cmap = pl.cm.seismic, extend = 'both')
    im.cmap.set_under('cyan')
    im.cmap.set_over('yellow')
    cb = fig.colorbar(im, ax = ax[i])
    cb.set_label(label[i])
    ax[i].set_aspect('equal')
    ax[i].set_xlim((xmin, xmax))
    ax[i].set_ylim((ymin, ymax))

fig.tight_layout()
pl.show()
