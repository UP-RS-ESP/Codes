import sys
import numpy as np
from matplotlib import pyplot as pl
from time import sleep

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

f = open('flush.txt', 'ab')
for i in range(0, n, 10):
    np.savetxt(f,
        np.transpose((x[i:i+10], y[i:i+10], z[i:i+10], c[i:i+10, 0], c[i:i+10, 1], c[i:i+10, 2])),
        fmt = '%.4f')
    f.flush()
    sleep(1)

f.close()
