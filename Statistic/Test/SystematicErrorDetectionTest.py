__author__ = 'Arnaud KOPP'

import numpy as np
from scipy import stats

from Statistic.Test.ttest import t_test


def SystematicErrorDetectionTest(Array, save=False, datatype='Median', alpha=0.05, verbose=False):
    '''
    Search for systematic error in plate or replicat
    :param Plate:
    :return:
    '''
    try:
        if isinstance(Array, np.ndarray):
            Matrix = Array
            shape = Matrix.shape
            SEDT_Array = np.zeros(shape)
            # search systematic error in row
            for row in range(shape[0]):
                tstat, dof = t_test(Matrix[row, :], np.delete(Matrix, row, 0))
                theo = stats.t.isf(alpha, dof)
                if tstat > theo:
                    SEDT_Array[row, :] = 1
            # search systematic error in column
            for col in range(shape[1]):
                tstat, dof = t_test(Matrix[:, col], np.delete(Matrix, col, 1))
                theo = stats.t.isf(alpha, dof)
                if tstat > theo:
                    SEDT_Array[:, col] = 1

            if verbose:
                print("Systematics Error Detection Test for plate")
                print(SEDT_Array)
                print("")

            return SEDT_Array
        else:
            raise TypeError
    except Exception as e:
        print(e)


