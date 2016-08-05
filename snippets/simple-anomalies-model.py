#!/usr/bin/python2
import sys
import numpy as np
from matplotlib import pyplot as plt

w = float(sys.argv[1])
r = np.random.normal(size = 365 * int(sys.argv[2]))
t = np.arange(len(r), dtype = 'float')
s = r + w * np.sin(np.pi * t / 182.5)

plt.plot(t, s)
plt.show()

d = np.zeros(365)
m = np.zeros(365)
for i in xrange(365):
    m[i] = s[i::365].mean()
    d[i] = s[i::365].std()

plt.plot(m, 'r-', label = 'Mean')
plt.plot(d, 'c--', label = 'Standard deviation')
plt.legend(loc = 'upper right')
plt.show()

a = np.zeros(s.shape)
for i in xrange(365):
    a[i::365] = s[i::365] - s[i::365].mean()

plt.plot(t, r, label = 'Prescribed gaussian noise')
plt.plot(t, a, label = 'Estimated anomalies')
plt.legend(loc = 'upper right')
plt.show()
