import numpy as np
import math
import pylab as pl

t = np.arange(0, 24.01, .01)
n1 = 4
lambda1 = 2
n2 = 7
lambda2 = 2
a = .3
c1 = 1
c2 = .5

hx = (t ** (n1 - 1)) * np.exp( - t / lambda1) / ((lambda1 ** n1) * math.factorial(n1 - 1))
hy = (t ** (n2 - 1)) * np.exp(-t / lambda2) / ((lambda2 ** n2) * math.factorial(n2 - 1))

hrf = a * (c1 * hx - c2 * hy)

pl.plot(t, hrf, 'k')
pl.axis([0, 25, -.01, .04])
pl.hold('on')

xx = np.zeros(9)
n = np.zeros(9)
for i in xrange(9):
    xx[i] = hrf[n[i]]

tt = np.arange(0, 27, 3)
print len(tt), len(xx)
pl.plot(tt, xx, 'o')
pl.hold('on')
pl.show()
