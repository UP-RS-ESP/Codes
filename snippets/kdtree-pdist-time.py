import sys
import numpy as np
from matplotlib import pyplot as pl
from scipy.spatial import cKDTree as kdtree
from scipy.spatial.distance import pdist, squareform
from timeit import timeit

def tree(xp, yp, r = 0.01):
    tree = kdtree(np.transpose((xp, yp)))
    lsts = tree.query_ball_tree(tree, r = r)
    l = 0
    for i in range(len(xp)):
        l += len(lsts[i])

    return l

def dist(xp, yp, r = 0.01):
    d = pdist(np.transpose((xp, yp)))
    d = squareform(d)
    l = 0
    for i in range(len(xp)):
        b = d[i, :] <= r
        l += len(b[b])

    return l

def test_tree():
    tree(xp, yp)

def test_dist():
    dist(xp, yp)

number = 100
n = 1000
xp = np.random.random(n)
yp = np.random.random(n)
print tree(xp, yp)
print dist(xp, yp)

ta = timeit('test_tree()', setup = 'from __main__ import test_tree',
        number = number) / number
tb = timeit('test_dist()', setup = 'from __main__ import test_dist',
        number = number) / number
print ta, tb

#sys.exit()

nn = 20
#nr = np.linspace(10, 1000, nn).astype('int')
nr = np.logspace(1, 3, nn).astype('int')
ra = np.zeros(nn)
for i in range(nn):
    n = nr[i]
    xp = np.random.random(n)
    yp = np.random.random(n)
    ta = timeit('test_tree()', setup = 'from __main__ import test_tree', number = number) / number
    tb = timeit('test_dist()', setup = 'from __main__ import test_dist', number = number) / number
    print(ta, tb)
    ra[i] = tb / ta

pl.figure(1, (10.24, 7.68))
pl.plot(nr, ra)
pl.xlabel('Number of points')
pl.ylabel('Ratio pdist / kdtree')
#pl.savefig('%s.png' % sys.argv[0][:-3])
pl.show()
