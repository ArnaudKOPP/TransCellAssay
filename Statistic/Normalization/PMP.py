__author__ = 'Arnaud KOPP'

import numpy as np
import Statistic.Test.SystematicErrorDetectionTest as SEDT


def PartialMeanPolish(input_array, epsilon=0.01, max_iteration=50):
    '''
    Implementation of Partial Mean Polish , published in 'Two effective methods for correcting experimental
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

            Rmu = []
            Cmu = []

            loop = 1
            converge = 0.0
            while True:
                diff = None
                converge = 0.0
                for i in Nrows:
                    for j in range(shape[1]):
                        Rmu[i] += input_array[i][j]
                    Rmu[i] /= shape[1]

                for j in Ncols:
                    for j in range(shape[0]):
                        Cmu[i] += input_array[i][j]
                    Rmu[i] /= shape[0]

                for i in Nrows:
                    diff = mu - Rmu[i]
                    converge += np.abs(diff)
                    for j in range(shape[1]):
                        input_array[i][j] += diff

                for j in Ncols:
                    diff = mu - Cmu[i]
                    converge += np.abs(diff)
                    for i in range(shape[0]):
                        input_array[i][j] += diff
                loop += 1
                if not (not (converge > epsilon) or not (loop < max_iteration)):
                    break

            return input_array
        else:
            raise TypeError
    except Exception as e:
        print(e)