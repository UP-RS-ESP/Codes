import sys
import numpy as np
import matplotlib as mpl
#mpl.use('Agg')
from matplotlib import pyplot as pl

def rgb(v):
    nv = v.copy()
    nv -= nv.min()
    nv /= nv.max()
    c = pl.cm.plasma(nv)
    return c[:, :-1]

np.random.seed(111)
n = 1000
x = np.random.random(n)
y = np.random.random(n)
z = np.exp(-x*x-y*y)
c = rgb(z)

p = np.transpose((x, y, z))

print(c.shape, p.shape)
sys.exit()

header = """ply
format ascii 1.0
element vertex %i
property float x
property float y
property float z
property float r
property float g
property float b
end_header""" % p.shape[0]

print(header)
np.savetxt(sys.stdout, np.hstack((p, c)), fmt = '%+.4e')
