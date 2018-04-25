import sys
import numpy as np
from laspy.file import File
from DemNets import *
from scipy.spatial import Delaunay
from scipy.spatial import cKDTree as kdtree
from scipy.stats import iqr
import matplotlib as mpl
mpl.use('Agg')
from matplotlib import pyplot as pl

fname = 'data.laz'
SCA = True

print('load %s ..' % fname)
f = File(fname, mode = 'r')

if SCA:
    x = f.x
    y = f.y
    z = f.z
    xoff = x.min()
    yoff = y.min()
    zoff = np.random.random(len(z)) / 10000.
    x -= xoff
    y -= yoff
    z += zoff

    print('load bool.gz ..')
    b = np.loadtxt('bool.gz', dtype = 'bool')
    print(len(b[b == True]), len(b))
    x = x[b]
    y = y[b]
    z = z[b]
    zoff = zoff[b]

    print('load densities ..')
    p = np.loadtxt('density-10.gz')
    p = p[b]
    if len(p) != len(x):
        sys.exit('len(p) not len(x)')
    p = 1./p
    p /= p.sum()
    print((p.min(), p.mean(), p.max()))
    n = len(p)
    i = np.random.choice(n, size = int(n*.1), replace = False, p = p)
    x = x[i]
    y = y[i]
    z = z[i]
    print(len(z), n)
    zoff = zoff[i]
    
    print('triangulation ..')
    tri = Delaunay(np.transpose((x, y)), qhull_options = 'Qt').simplices.astype('uint32')

    print('facet flow network ..')
    net = Simplicies(tri, len(x))
    spx, spw, spa, spd, phi = FacetFlowNetwork(tri, net, x, y, z)
    print('no zero width:', len(spd[spd == 0]))
    
    print('Tubes ..')
    spx, spw, spa = Tubes(tri, net, x, y, z, spx, spw, spa)
    
    print('network node coords ..')
    xp = x[tri].mean(axis=1)
    yp = y[tri].mean(axis=1)
    z -= zoff
    zp = z[tri].mean(axis=1)
    
    print('flow accumulation ..')
    sca = FacetFlowThroughput(spx, spw, spa)
    sca = sca.sum(axis=1)
    sca /= spd

    print('no NaNs:', len(sca[np.isnan(sca)]))
    print('no zeros:', len(sca[sca == 0.0]))
   
    #print('save SCAs ..')
    #np.savez('sca.npz', sca=sca, x=xp, y=yp, z=zp, xoff=xoff, yoff=yoff)

else:
    print('load sca.npy ..')
    h = np.load('sca.npz')
    sca = h['sca']
    xoff = h['xoff']
    yoff = h['yoff']
    xp = h['x']
    yp = h['y']
    zp = h['z']

sca = np.log10(sca)
sca -= sca.min()
sca /= sca.max()

print('convert to 16-bit rgbs ..')
cm = pl.cm.viridis
rgb = cm(sca)
rgb = rgb[:, :3]
rgb *= 65535
rgb = rgb.astype('uint')

print('open sca.las ..')
g = File('sca.las', mode = 'w', header = f.header)
#g.points = f.points
g.x = xp + xoff
g.y = yp + yoff
g.z = zp
g.set_red(rgb[:, 0])
g.set_green(rgb[:, 1])
g.set_blue(rgb[:, 2])
g.close()
