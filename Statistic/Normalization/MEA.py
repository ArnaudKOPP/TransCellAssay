__author__ = 'Arnaud KOPP'

import numpy as np
import Statistic.Test.SystematicErrorDetectionTest as SEDT


def MatrixErrorAmendment(input_array):
    '''
    Implementation of Matrix Error Amendment , published in 'Two effective methods for correcting experimental
    HTS data ' Dragiev, et al 2012
    :param: input_array: numpy ndarray represent data
    :return:
    '''
    try:
        if isinstance(input_array, np.ndarray):
            # # count number of row and col affected by systematic error
            shape = input_array.shape
            Nrows = []
            Ncols = []

            # search systematic error in row
            for row in range(shape[0]):
                if SEDT.TTest(input_array[row, :], np.delete(input_array, row, 0)):
                    Nrows.append(row)
            # search systematic error in column
            for col in range(shape[1]):
                if SEDT.TTest(input_array[:, col], np.delete(input_array, col, 1)):
                    Ncols.append(col)

            # exit if not row or col affected
            N = Nrows.count() + Ncols.count()
            if N == 0:
                print('No Systematics Error detected')
                return input_array

            mu = 0
            # # compute mu
            for row in range(shape[0]):
                if not row in Nrows:
                    for col in range(shape[1]):
                        if not col in Ncols:
                            mu += input_array[row][col]
            mu /= ((shape[0] - Nrows) * (shape[1] - Ncols))

            # # exact solution
            X = np.array(N)
            A = np.array(N, N)
            B = np.array(N)

            for i in range(Nrows.count()):
                r = Nrows[i]
                A[i][i] = shape[1]
                for j in range(Nrows.count(), N, 1):
                    A[i, j] = 1.0
                B[i] = -shape[1] * mu
                for k in range(0, shape[1], 1):
                    B[i] += input_array[r][k]

            for i in range(Nrows.count(), N, 1):
                c = Ncols[i - Nrows.count()]
                A[i][i] = shape[0]
                for j in range(0, Nrows.count(), 1):
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

            for i in range(Nrows.count()):
                r = Nrows[i]
                for j in range(shape[1]):
                    input_array[r][j] -= X[i]

            for i in range(Nrows.count(), N, 1):
                c = Ncols[i - Nrows.count()]
                for j in range(Nrows.count()):
                    input_array[j][c] -= X[i]

            return input_array
        else:
            raise TypeError
    except Exception as e:
        print(e)