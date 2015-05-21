# coding=utf-8
"""
Sigmoid fitting for dose response analysis
"""

import numpy as np
import pylab
import numpy.random as npr
import matplotlib.pyplot as plt
from scipy.optimize import leastsq
from scipy.optimize import curve_fit

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


class sigmoid_fitting():
    """
    class for Dose Response analysis
    """

    def __init__(self):

        def sigmoid(x, x0, k):
            y = 1 / (1 + np.exp(-k * (x - x0)))
            return y

        xdata = np.array([0.0, 1.0, 3.0, 4.3, 7.0, 8.0, 8.5, 10.0, 12.0])
        ydata = np.array([0.01, 0.02, 0.04, 0.11, 0.43, 0.7, 0.89, 0.95, 0.99])

        popt, pcov = curve_fit(sigmoid, xdata, ydata)
        print(popt, pcov)

        x = np.linspace(-1, 15, 50)
        y = sigmoid(x, *popt)

        pylab.plot(xdata, ydata, 'o', label='data')
        pylab.plot(x, y, label='fit')
        pylab.ylim(0, 1.05)
        pylab.legend(loc='best')
        pylab.show()

        # http://people.duke.edu/~ccc14/pcfb/analysis.html
        def logistic4(x, A, B, C, D):
            """4PL lgoistic equation."""
            return ((A-D)/(1.0+((x/C)**B))) + D

        def residuals(p, y, x):
            """Deviations of data from fitted 4PL curve"""
            A,B,C,D = p
            err = y-logistic4(x, A, B, C, D)
            return err

        def peval(x, p):
            """Evaluated value at x with current parameters."""
            A,B,C,D = p
            return logistic4(x, A, B, C, D)

        # Make up some data for fitting and add noise
        # In practice, y_meas would be read in from a file
        x = np.linspace(0,20,20)
        A,B,C,D = 0.5,2.5,8,7.3
        y_true = logistic4(x, A, B, C, D)
        y_meas = y_true + 0.2*npr.randn(len(x))

        # Initial guess for parameters
        p0 = [0, 1, 1, 1]

        # Fit equation using least squares optimization
        plsq = leastsq(residuals, p0, args=(y_meas, x))

        # Plot results
        plt.plot(x,peval(x,plsq[0]),x,y_meas,'o',x,y_true)
        plt.title('Least-squares 4PL fit to noisy data')
        plt.legend(['Fit', 'Noisy', 'True'], loc='upper left')
        for i, (param, actual, est) in enumerate(zip('ABCD', [A,B,C,D], plsq[0])):
            plt.text(10, 3-i*0.5, '%s = %.2f, est(%s) = %.2f' % (param, actual, param, est))
        plt.show()

