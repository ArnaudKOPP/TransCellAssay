# coding=utf-8
"""
The MEA method consist of the two followings steps:
    -Estimate the value of the row and col systematic errors, independently for every plate of the assay, by solving the
system of linear equations/
    -Adjust the measurement of all compounds located in rows and col of the plate affected by the systematic error using
the error estimates determinted in previous step.
"""

import numpy as np
from scipy import stats
import logging
log = logging.getLogger(__name__)


__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


def matrix_error_amendmend(input_array, verbose=False, alpha=0.05, skip_col=[], skip_row=[]):
    """
    Implementation of Matrix Error Amendment , published in 'Two effective methods for correcting experimental
    HTS data ' Dragiev, et al 2012
    :param alpha: alpha for TTrest
    :param verbose: print or not result
    :param input_array: numpy ndarray represent data
    :param skip_col: index of col to skip
    :param skip_row: index of row to skip
    :return: normalized array
    """
    if isinstance(input_array, np.ndarray):
        array_org = input_array.copy()
        # # count number of row and col affected by systematic error
        shape = input_array.shape
        nrows = []
        ncols = []

        # search systematic error in row
        for row in range(shape[0]):
            t, prob = stats.ttest_ind(input_array[row, :].flatten(), np.delete(input_array, row, 0).flatten(),
                                      equal_var=False)
            if prob < alpha:
                nrows.append(row)
        # search systematic error in column
        for col in range(shape[1]):
            t, prob = stats.ttest_ind(input_array[:, col].flatten(), np.delete(input_array, col, 1).flatten(),
                                      equal_var=False)
            if prob < alpha:
                ncols.append(col)

        nrows = [x for x in nrows if x not in skip_row]
        ncols = [x for x in ncols if x not in skip_col]

        # exit if not row or col affected
        n = nrows.__len__() + ncols.__len__()
        if n == 0:
            log.info('MEA : No Systematics Error detected')
            return input_array

        mu = 0
        # # compute mu
        for row in range(shape[0]):
            if row not in nrows:
                for col in range(shape[1]):
                    if col not in ncols:
                        mu += input_array[row][col]
        mu /= ((shape[0] - nrows.__len__()) * (shape[1] - ncols.__len__()))

        # exact solution
        x = np.zeros(n)
        a = np.zeros([n, n])
        b = np.zeros(n)

        for i in range(nrows.__len__()):
            r = nrows[i]
            a[i][i] = shape[1]
            for j in range(nrows.__len__(), n, 1):
                a[i, j] = 1.0
            b[i] = -shape[1] * mu
            for k in range(0, shape[1], 1):
                b[i] += input_array[r][k]
        for i in range(nrows.__len__(), n, 1):
            c = ncols[i - nrows.__len__()]
            a[i][i] = shape[0]
            for j in range(0, nrows.__len__(), 1):
                a[i][j] = 1.0
            b[i] = -shape[0] * mu
            for k in range(0, shape[0], 1):
                b[i] += input_array[k][c]

        a = np.linalg.inv(a)

        # x = Inv(a) * b, x is the estimated row and column error

        for i in range(n):
            x[i] = 0.0
            for j in range(n):
                x[i] += a[i][j] * b[j]

        # Remove the systematic error form the plate measure

        for i in range(nrows.__len__()):
            r = nrows[i]
            for j in range(shape[1]):
                input_array[r][j] -= x[i]

        for i in range(nrows.__len__(), n, 1):
            c = ncols[i - nrows.__len__()]
            for j in range(nrows.__len__()):
                input_array[j][c] -= x[i]

        if verbose:
            print("MEA methods for removing systematics error")
            print(u'\u03B1'" for T-Test : ", alpha)
            print("-----Normalized Table-------")
            print(input_array)
            print("-----Original Table-------")
            print(array_org)
            print("")
        return input_array
    else:
        raise TypeError('Expected the argument to be a numpy.ndarray.')