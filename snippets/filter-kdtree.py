import sys
import numpy as np
from matplotlib import pyplot as pl
from scipy.interpolate import griddata
from scipy.spatial import cKDTree as kdtree

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
            m = np.median(zp[b])
            t += b * (zp <= m)

    # grid center
    dbx, dby = abs(xb[0]-xb[1]), abs(yb[0]-yb[1])
    x, y = xb[:-1] + dbx/2, yb[:-1] + dby/2
    X, Y = np.meshgrid(x, y)

    return griddata((xp[t], yp[t]), zp[t], (X, Y), method = method)

def radialfilter(xp, yp, zp, r = 1.0, method = 'linear'):
    n = len(zp)
    print('kd-tree ..')
    tree = kdtree(np.transpose((xp, yp)))
    
    print('query ball tree ..')
    lsts = tree.query_ball_tree(tree, r = r)
    print(n, len(lsts))

    t = np.zeros(n, dtype = 'bool')
    for i in range(n):
        m = np.percentile(zp[lsts[i]], 10)
        b = np.zeros(n, dtype = 'bool')
        b[lsts[i]] = True
        t += b * (zp <= m)

    # grid center
    dbx, dby = abs(xb[0]-xb[1]), abs(yb[0]-yb[1])
    x, y = xb[:-1] + dbx/2, yb[:-1] + dby/2
    X, Y = np.meshgrid(x, y)

    return griddata((xp[t], yp[t]), zp[t], (X, Y), method = method)

# grid setup
np.random.seed(35791)
method = 'cubic'
nopgc = 20
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
      radialfilter(xp, yp, zp+noise, r = .1, method = method)]

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
