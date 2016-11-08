# coding=utf-8
"""
Method for curve fitting
"""
from math import ceil
import numpy as np
from scipy import linalg

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2016 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "GPLv3"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"


"""
This module implements the Lowess function for nonparametric regression.
Functions:
lowess        Fit a smooth nonparametric regression curve to a scatterplot.
For more information, see
William S. Cleveland: "Robust locally weighted regression and smoothing
scatterplots", Journal of the American Statistical Association, December 1979,
volume 74, number 368, pp. 829-836.
William S. Cleveland and Susan J. Devlin: "Locally weighted regression: An
approach to regression analysis by local fitting", Journal of the American
Statistical Association, September 1988, volume 83, number 403, pp. 596-610.
"""


def __lowess(x, y, iter, f=2./3.):
    """
    lowess(x, y, f=2./3., iter=3) -> yest
    Lowess smoother: Robust locally weighted regression.
    The lowess function fits a nonparametric regression curve to a scatterplot.
    The arrays x and y contain an equal number of elements; each pair
    (x[i], y[i]) defines a data point in the scatterplot. The function returns
    the estimated (smooth) values of y.
    The smoothing span is given by f. A larger value for f will result in a
    smoother curve. The number of robustifying iterations is given by iter. The
    function will run faster with a smaller number of iterations.
    """
    n = len(x)
    r = int(ceil(f * n))
    h = [np.sort(np.abs(x - x[i]))[r] for i in range(n)]
    w = np.clip(np.abs((x[:, None] - x[None, :]) / h), 0.0, 1.0)
    w = (1 - w ** 3) ** 3
    yest = np.zeros(n)
    delta = np.ones(n)
    for iteration in range(iter):
        for i in range(n):
            weights = delta * w[:, i]
            b = np.array([np.sum(weights * y), np.sum(weights * y * x)])
            A = np.array([[np.sum(weights), np.sum(weights * x)],
                          [np.sum(weights * x), np.sum(weights * x * x)]])
            beta = linalg.solve(A, b)
            yest[i] = beta[0] + beta[1] * x[i]

        residuals = y - yest
        s = np.median(np.abs(residuals))
        delta = np.clip(residuals / (6.0 * s), -1, 1)
        delta = (1 - delta ** 2) ** 2

    return yest


def lowess_fitting(input_array, max_iteration=3, verbose=False, skip_col=[], skip_row=[], f=2./3.):
    array_org = input_array.copy()
    shape = input_array.shape

    # apply on rows
    for row in range(shape[0]):
        if row in skip_row:
            pass
        else:
            input_array[row,:] = __lowess(x=np.linspace(1, shape[1], shape[1]), y=input_array[row,:],
                                          iter=max_iteration, f=f)

    # apply on columns
    for col in range(shape[1]):
        if col in skip_col:
            pass
        else:
            input_array[:,col] = __lowess(x=np.linspace(1, shape[0], shape[0]), y=input_array[:,col],
                                          iter=max_iteration, f=f)

    if verbose:
        print("Lowess fitting")
        print("robustifying iteration: {}".format(max_iteration))
        print("-----Normalized Table-------")
        print(input_array)
        print("-----Original Table-------")
        print(array_org)
        print("")
    return input_array


def polynomial_fitting(input_array, degree=4, verbose=False, skip_col=[], skip_row=[]):
    array_org = input_array.copy()
    shape = input_array.shape

    # apply on rows
    for row in range(shape[0]):
        if row in skip_row:
            pass
        else:
            poly = np.poly1d(np.polyfit(x=np.linspace(1, shape[1], shape[1]), y=input_array[row,:], deg=degree))
            input_array[row,:] = poly(np.linspace(1, shape[1], shape[1]))

    # apply on columns
    for col in range(shape[1]):
        if col in skip_col:
            pass
        else:
            poly = np.poly1d(np.polyfit(x=np.linspace(1, shape[0], shape[0]), y=input_array[:,col], deg=degree))
            input_array[:,col] = poly(np.linspace(1, shape[0], shape[0]))

    if verbose:
        print("Polynomial fitting")
        print("Degree of the fitting polynomial : {}".format(degree))
        print("-----Normalized Table-------")
        print(input_array)
        print("-----Original Table-------")
        print(array_org)
        print("")
    return input_array
