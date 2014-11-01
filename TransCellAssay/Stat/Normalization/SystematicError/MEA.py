"""
The MEA method consist of the two followings steps:
    -Estimate the value of the row and col systematic errors, independently for every plate of the assay, by solving the
system of linear equations/
    -Adjust the measurement of all compounds located in rows and col of the plate affected by the systematic error using
the error estimates determinted in previous step.
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


def MatrixErrorAmendment(input_array, verbose=False, alpha=0.05):
    """
    Implementation of Matrix Error Amendment , published in 'Two effective methods for correcting experimental
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


            # # exact solution
            X = np.zeros(N)
            A = np.zeros([N, N])
            B = np.zeros(N)

            for i in range(Nrows.__len__()):
                r = Nrows[i]
                A[i][i] = shape[1]
                for j in range(Nrows.__len__(), N, 1):
                    A[i, j] = 1.0
                B[i] = -shape[1] * mu
                for k in range(0, shape[1], 1):
                    B[i] += input_array[r][k]
            for i in range(Nrows.__len__(), N, 1):
                c = Ncols[i - Nrows.__len__()]
                A[i][i] = shape[0]
                for j in range(0, Nrows.__len__(), 1):
                    A[i][j] = 1.0
                B[i] = -shape[0] * mu
                for k in range(0, shape[0], 1):
                    B[i] += input_array[k][c]

            A = np.linalg.inv(A)

            # X = Inv(A) * B, X is the estimated row and column error

            for i in range(N):
                X[i] = 0.0
                for j in range(N):
                    X[i] += A[i][j] * B[j]

            # Remove the systematic error form the plate measure

            for i in range(Nrows.__len__()):
                r = Nrows[i]
                for j in range(shape[1]):
                    input_array[r][j] -= X[i]

            for i in range(Nrows.__len__(), N, 1):
                c = Ncols[i - Nrows.__len__()]
                for j in range(Nrows.__len__()):
                    input_array[j][c] -= X[i]

            np.set_printoptions(suppress=True)
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
            raise TypeError
    except Exception as e:
        print("\033[0;31m[ERROR]\033[0m", e)