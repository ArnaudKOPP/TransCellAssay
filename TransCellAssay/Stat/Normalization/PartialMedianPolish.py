# coding=utf-8
"""
Main steps of the PMP method:

    -Compute mean value of all entities of the given plate that are not affected by the systematic error.
    -For each row, compute the mean value and estimates the row bias; for each col, compute the mean and estimates the
row bias.
    -For all rows affected by systematics bias, adjust their measurement using the error estimates determined in
previous step for each row and col; For all col affected by systematics bias, adjust their measurement using the error
estimates determined in previous step for each row and col.
    -Compute value of the convergence parameter.
    -If convergence parameter is inf of ref threshold, stop, else repeat previous step.
"""

import numpy as np
from scipy import stats
import logging
log = logging.getLogger(__name__)


__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2016 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "GPLv3"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"


def partial_mean_polish(input_array, epsilon=0.01, max_iteration=50, verbose=False, alpha=0.05, skip_col=[],
                        skip_row=[]):
    """
    Implementation of Partial Mean Polish , published in 'Two effective methods for correcting experimental
    HTS data ' Dragiev, et al 2012
    :param alpha: alpha for TTest
    :param verbose: print or not result
    :param max_iteration: max iteration for PMP
    :param epsilon: epsilon for convergence
    :param input_array: numpy ndarray represent data
    :param skip_col: index of col to skip
    :param skip_row: index of row to skip
    :return: normalized array
    """
    assert isinstance(input_array, np.ndarray)

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
        log.info('PMP : No Systematics Error detected')
        return input_array

    mu = 0
    # # compute mu
    for row in range(shape[0]):
        if row not in nrows:
            for col in range(shape[1]):
                if col not in ncols:
                    mu += input_array[row][col]

    try:
        mu /= ((shape[0] - len(nrows)) * (shape[1] - len(ncols)))
    except:
        log.debug('PMP : set Mu to 0 (divided by zero)')
        pass

    rmu = [0] * shape[0]
    cmu = [0] * shape[1]

    loop = 1
    converge = 0.0
    while True:
        log.debug('PMP iteration : %s' % loop)
        diff = 0.0
        converge = 0.0
        for i in nrows:
            for j in range(shape[1]):
                rmu[i] += input_array[i][j]
            rmu[i] /= shape[1]

        for j in ncols:
            for i in range(shape[0]):
                cmu[j] += input_array[i][j]
            cmu[j] /= shape[0]

        for i in nrows:
            diff = mu - rmu[i]
            converge += np.absolute(diff)
            for j in range(shape[1]):
                input_array[i][j] += diff

        for j in ncols:
            diff = mu - cmu[j]
            converge += np.absolute(diff)
            for i in range(shape[0]):
                input_array[i][j] += diff
        loop += 1
        if converge < epsilon:
            break
        if loop > max_iteration:
            break

    if verbose:
        print("PMP methods for removing systematics error")
        print(u'\u03B1'" for T-Test : ", alpha)
        print(u'\u03B5'" : ", epsilon)
        print("-----Normalized Table-------")
        print(input_array)
        print("-----Original Table-------")
        print(array_org)
        print("")
    return input_array
