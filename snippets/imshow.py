#!/usr/bin/python2
import sys
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

cmap = plt.cm.viridis

z = np.loadtxt(sys.stdin)

# figure
f, ax = plt.subplots(figsize = (10.24, 7.68))
im = ax.imshow(z, cmap = cmap, interpolation = 'none', origin = 'lower')
plt.axis('off')
d = make_axes_locatable(ax)
cax = d.append_axes('bottom', size='3%', pad=0.05)
cb = plt.colorbar(im, cax = cax, orientation = 'horizontal')
try:
    cb.set_label(sys.argv[1])
except:
    print 'you can specifiy a colorbar label as an argument to %s' % sys.argv[0]
plt.show()
