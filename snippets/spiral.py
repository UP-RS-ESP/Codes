import numpy as np
from matplotlib import pyplot as pl
from matplotlib.colors import LogNorm

def fib(n):
    if n == 0 or n == 1:
        r = 1
    else:
        r = fib(n-1)+fib(n-2)
    return r

a = np.zeros((10000, 10000))
x = y = 5000
k = 0

for i in range(4):
    fk = fib(k)
    a[y:y+fk, x:x+fk] = k+1
    x += fk
    y += fk
    k += 1
    fk = fib(k)
    y -= fk
    a[y:y+fk, x:x+fk] = k+1
    x += fk
    k += 1
    fk = fib(k)
    u = fk
    y -= fk
    x -= fk
    a[y:y+fk, x:x+fk] = k+1
    k += 1
    fk = fib(k)
    v = fk
    x -= fk
    a[y:y+fk, x:x+fk] = k+1
    y += fk
    k += 1

z = a[a > 0]
z.shape = (v, v+u)

norm = LogNorm()
cmap = pl.cm.viridis_r

#pl.imshow(z, origin = 'lower', interpolation = 'none', norm = norm, cmap = cmap)

x = range(v+u+1)
y = range(v+1)
x, y = np.meshgrid(x, y)
pl.pcolormesh(x, y, z, norm = norm, cmap = cmap)

#x = range(v+u)
#y = range(v)
#x, y = np.meshgrid(x, y)
#pl.contourf(x, y, z, 20, cmap = cmap)

pl.colorbar()
pl.show()
