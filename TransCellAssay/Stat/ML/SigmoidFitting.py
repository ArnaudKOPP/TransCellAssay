# coding=utf-8
"""
Sigmoid fitting for dose response analysis
"""

import numpy as np
import pylab
from scipy.optimize import curve_fit

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


class sigmoidfitting():
    def __init__(self):
        try:
            self.input = None
            self.output = None
            self.concentrationpos = 0
        except Exception as e:
            print(e)

    """
    def sigmoid(x, x0, k):
        y = 1 / (1 + np.exp(-k*(x-x0)))
        return y

    xdata = np.array([0.0,   1.0,  3.0, 4.3, 7.0,   8.0,   8.5, 10.0, 12.0])
    ydata = np.array([0.01, 0.02, 0.04, 0.11, 0.43,  0.7, 0.89, 0.95, 0.99])

    popt, pcov = curve_fit(sigmoid, xdata, ydata)
    print(popt, pcov)

    x = np.linspace(-1, 15, 50)
    y = sigmoid(x, *popt)

    pylab.plot(xdata, ydata, 'o', label='data')
    pylab.plot(x,y, label='fit')
    pylab.ylim(0, 1.05)
    pylab.legend(loc='best')
    pylab.show()
    """