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
__license__ = "GPLv3"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"


class DoseResponseCurve(object):
    """
    class for Dose Response analysis
    http://psg.hitachi-solutions.com/masterplex/blog/the-4-parameter-logistic-4pl-nonlinear-regression-model
    """

    def __init__(self, func):

        __valid_function = ['sigmoid', '4pl', '5pl']
        if func not in __valid_function:
            raise ValueError('Valid func type : {}'.format(__valid_function))
        self.__fit()

    @staticmethod
    def __logistic4(x, A, B, C, D):
        """
        4PL logistic equation.
        A = Bottom
        B = HillCoef
        C = EC50 or inflection point
        D = Top
        """
        return ((A - D) / (1.0 + ((x / C) ** B))) + D

    @staticmethod
    def __logistic5(x, A, B, C, D, E):
        """
        :param x:
        :param A: is the MFI (Mean Fluorescent Intensity)/RLU (Relative Light Unit) value for the minimum asymptote
        :param B: is the Hill slope
        :param C: is the concentration at the inflection point
        :param D: is the MFI/RLU value for the maximum asymptote
        :param E: is the asymmetry factor
        :return:
        """
        return (D + (A - D) / ((1 + (x / C) ** B) ** E))

    @staticmethod
    def __sigmoid(x, x0, k):
        y = 1 / (1 + np.exp(-k * (x - x0)))
        return y

    def __fit(self):
        # Input Data
        xdata = np.array([0.0, 1.0, 3.0, 4.3, 7.0, 8.0, 8.5, 10.0, 12.0])
        ydata_sens = np.array([0.99, 0.95, 0.89, 0.7, 0.43, 0.11, 0.04, 0.02, 0.01]) # sensitive to drug
        ydata_part = np.array([0.99, 0.95, 0.89, 0.8, 0.75, 0.65, 0.59, 0.50, 0.43]) # partial response
        ydata_res = np.array([0.99, 0.95, 0.95, 0.93, 0.95, 0.95, 0.93, 0.92, 0.95]) #resistant to drug

        def do_fitting(xdata, ydata):
            # Fit curve to get parameters
            popt, pcov = curve_fit(self.__logistic4, xdata, ydata, maxfev=20000)
            perr = np.sqrt(np.diag(pcov))
            print('4Pl')
            print('Parameters :', popt)
            print('Std err    :', perr)
            print('Param cov  :', pcov)

            # # Create data for fitted curve
            # x = np.linspace(-1, 15, 50)
            # y = self.__logistic4(x, *popt)
            #
            # # Plot data and fitted curve
            # pylab.plot(xdata, ydata, 'o', label='Input data')
            # pylab.plot(x, y, label='Curve fit 4pl')
            # pylab.ylim(0, 1.05)
            # pylab.legend(loc='best')
            # pylab.show()

            # Fit curve to get parameters
            popt, pcov = curve_fit(self.__logistic5, xdata, ydata, maxfev=20000)
            perr = np.sqrt(np.diag(pcov))
            print('5Pl')
            print('Parameters :', popt)
            print('Std err    :', perr)
            print('Param cov  :', pcov)

            # # Create data for fitted curve
            # x = np.linspace(-1, 15, 50)
            # y = self.__logistic5(x, *popt)
            #
            # # Plot data and fitted curve
            # pylab.plot(xdata, ydata, 'o', label='Input data')
            # pylab.plot(x, y, label='Curve fit 5pl')
            # pylab.ylim(0, 1.05)
            # pylab.legend(loc='best')
            # pylab.show()

        print('Sensible to drug')
        do_fitting(xdata, ydata_sens)
        print('Partial response')
        do_fitting(xdata, ydata_part)
        print('Resistant to drug')
        do_fitting(xdata, ydata_res)