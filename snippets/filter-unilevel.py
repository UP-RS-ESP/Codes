import sys
import numpy as np
from matplotlib import pyplot as pl
from scipy.interpolate import griddata

def level(v, n):
    #vmin, vmax = v.min(), v.max()
    vmin, vmax = np.percentile(v, 5), np.percentile(v, 95)
    if vmin < 0 and vmax < -vmin:
        vmax = -vmin
    return np.linspace(-vmax, vmax, n)

def minfilter(xp, yp, zp, xb, yb):
    shape = (len(yb)-1, len(xb)-1)
    Z = np.zeros(shape)
    for i in range(shape[0]):
        for k in range(shape[1]):
            b = (xb[k] <= xp)
            b *= (xp < xb[k+1])
            b *= (yb[i] <= yp)
            b *= (yp < yb[i+1])
            if len(zp[b]) == 0:
                Z[i, k] = np.nan
            else:
                Z[i, k] = np.min(zp[b])
    
    return Z

# grid setup
method = 'cubic'
nopgc = 10
shape = (100, 100)
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
noise = np.abs(np.random.normal(0, 0.01, nop))

Zs = [griddata((xp, yp), zp,       (X, Y), method = method),
      griddata((xp, yp), zp+noise, (X, Y), method = method),
      minfilter(xp, yp,  zp+noise, xb, yb)]

# common levels
Zdiff = (Z - np.ma.masked_invalid(Zs[0])).flatten()
for i in range(1, 3):
    Zi = np.ma.masked_invalid(Zs[i])
    Zdiff = np.append(Zdiff, (Z-Zi).flatten())

level = level(Zdiff, 50)

label = ['Gridded zp',
         'Gridded zp+noise',
         'Minimum filter of zp+noise']

fig, ax = pl.subplots(1, 3)
for i in range(3):
    Zi = np.ma.masked_invalid(Zs[i])
    im = ax[i].contourf(X, Y, Z-Zi, level,
            cmap = pl.cm.seismic, extend = 'both')
    im.cmap.set_under('cyan')
    im.cmap.set_over('#aabbcc')
    cb = fig.colorbar(im, ax = ax[i])
    cb.set_label(label[i])
    ax[i].set_aspect('equal')
    ax[i].set_xlim((xmin, xmax))
    ax[i].set_ylim((ymin, ymax))

fig.tight_layout()
pl.show()
