import sys
import numpy as np
from time import sleep
import displaz
from matplotlib import pyplot as pl

def rgb(v):
    nv = v.copy()
    nv -= nv.min()
    nv /= nv.max()
    c = pl.cm.plasma(nv)
    return c[:, :-1]

np.random.seed(111)
n = 10

for i in range(1000):
    x = np.random.random(n)
    y = np.random.random(n)
    z = np.exp(-x*x-y*y)
    c = rgb(z)
    p = np.transpose((x, y, z))

    # display frame and wait 100ms
    displaz.plot(p, color = c)#, label = 'dem')
    sleep(1)
