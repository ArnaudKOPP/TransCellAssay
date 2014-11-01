"""
Main steps of the PMP method:
    -Compute mean value of all entities of the given plate that are not affected by the systematic error.
    -For each row, compute the mean value and estimates the row bias; for each col, compute the mean and estimates the
row bias.
    -For all rows affected by systematics bias, adjust their measurement using the error estimates determined in
previous step for each row and col; For all col affected by systematics bias, adjust their measurement using the error estimates determined in
previous step for each row and col.
    -Compute value of the convergence parameter.
    -If convergence parameter is inf of ref threshold, stop, else repeat previous step.
"""

import numpy as np

from TransCellAssay.Stat.Test.ttest import TTest


__author__ = "Arnaud KOPP"
__copyright__ = "© 2014 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


def PartialMeanPolish(input_array, epsilon=0.01, max_iteration=50, verbose=False, alpha=0.05):
    """
    Implementation of Partial Mean Polish , published in 'Two effective methods for correcting experimental
    HTS data ' Dragiev, et al 2012
    :param: input_array: numpy ndarray represent data
    :return:
    """
    try:
        if isinstance(input_array, np.ndarray):
            array_org = input_array.copy()
            # # count number of row and col affected by systematic error
            shape = input_array.shape
            Nrows = []
            Ncols = []

            # search systematic error in row
            for row in range(shape[0]):
                if TTest(input_array[row, :], np.delete(input_array, row, 0), alpha=alpha):
                    Nrows.append(row)
            # search systematic error in column
            for col in range(shape[1]):
                if TTest(input_array[:, col], np.delete(input_array, col, 1), alpha=alpha):
                    Ncols.append(col)

            # exit if not row or col affected
            N = Nrows.__len__() + Ncols.__len__()
            if N == 0:
                print('\033[0;33m[WARNING]\033[0m No Systematics Error detected')
                return input_array

            mu = 0
            # # compute mu
            for row in range(shape[0]):
                if not row in Nrows:
                    for col in range(shape[1]):
                        if not col in Ncols:
                            mu += input_array[row][col]
            mu /= ((shape[0] - Nrows.__len__()) * (shape[1] - Ncols.__len__()))

            Rmu = [0] * shape[0]
            Cmu = [0] * shape[1]

            loop = 1
            converge = 0.0
            while True:
                diff = 0.0
                converge = 0.0
                for i in Nrows:
                    for j in range(shape[1]):
                        Rmu[i] += input_array[i][j]
                    Rmu[i] /= shape[1]

                for j in Ncols:
                    for i in range(shape[0]):
                        Cmu[j] += input_array[i][j]
                    Cmu[j] /= shape[0]

                for i in Nrows:
                    diff = mu - Rmu[i]
                    converge += np.absolute(diff)
                    for j in range(shape[1]):
                        input_array[i][j] += diff

                for j in Ncols:
                    diff = mu - Cmu[i]
                    converge += np.absolute(diff)
                    for i in range(shape[0]):
                        input_array[i][j] += diff
                loop += 1
                if not (not (converge > epsilon) or not (loop < max_iteration)):
                    break

            np.set_printoptions(suppress=True)
            if verbose:
                print("PMP methods for removing systematics error")
                print(u'\u03B1'" for T-Test : ", alpha)
                print(u'\u03B5'" : ", epsilon)
                print("Max Iteration : ", max_iteration)
                print("-----Normalized Table-------")
                print(input_array)
                print("-----Original Table-------")
                print(array_org)
                print("")
            return input_array
        else:
            raise TypeError
    except Exception as e:
        print("\033[0;31m[ERROR]\033[0m", e)