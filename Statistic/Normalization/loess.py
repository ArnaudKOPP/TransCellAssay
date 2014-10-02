__author__ = 'Arnaud KOPP'

import sys
import math
import matplotlib.pyplot as plt

SQRT_2PI = math.sqrt(2.0 * math.pi)

def gaussian(x):
    return math.exp(-0.5*x*x)/SQRT_2PI

# tri-cube weight function
def tricube(x):
    if x < -1 or x > 1:
        return 0
    return (1 - math.fabs(x)**3)**3

def weights(x, h, X):
    return [ tricube((xi - x)/float(h))/float(h) for xi in X ]

def loess(x, h, X, Y):
    W = weights(x, h, X)
    SUMW = sum(W)
    SUMWX = sum( [ W[i]*X[i] for i in range(len(X)) ] )
    SUMWY = sum( [ W[i]*Y[i] for i in range(len(X)) ] )
    SUMWXY = sum( [ W[i]*X[i]*Y[i] for i in range(len(X)) ] )
    SUMWXX = sum( [ X[i]*X[i] for i in range(len(X)) ] )
    SUMWYY = sum( [ Y[i]*Y[i] for i in range(len(X)) ] )
    m = (SUMW * SUMWXY - SUMWX * SUMWY) / ( SUMW * SUMWXX - SUMWX * SUMWX)
    b = (SUMWY - m*SUMWX) / SUMW
    return m*x+b

if __name__=='__main__':

    X = []
    Y = []

    i = 0
    for line in file('draft_70.tab'):
        line = line.strip()
        if i > 2:
            [day, month, monthNo, dayOfYear, draftNo] = line.split("\t")
            X.append( float(dayOfYear) )
            Y.append( float(draftNo) )
        i += 1

    L25 = []
    L100 = []
    for x in X:
        L25.append( loess(x, 25, X, Y) )
        L100.append( loess(x, 100, X, Y) )

    # Plot the master bin
    plt.plot(X, Y, 'g+')
    plt.plot(X, L25, 'b-')
    plt.plot(X, L100, 'r-')
    plt.show()