# coding=utf-8
"""
Search for systematic error in plate or replicat, use Welch T-Test

"""

import numpy as np
from scipy import stats


__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


def systematic_error_detection_test(array, alpha=0.05, verbose=False, path=None):
    """
    Search for systematic error in plate or replicat, use Welch T-Test
    :param array: numpy array to test
    :param alpha: alpha for t-test
    :param verbose: verbose or not
    :param path: if not none, path to save array that contain info of test
    :return: array with 0 if not SE and 1 if SE contain in col or row
    """
    try:
        if isinstance(array, np.ndarray):
            matrix = array
            shape = matrix.shape
            sedt_array = np.zeros(shape)
            # search systematic error in row
            for row in range(shape[0]):
                t, prob = stats.ttest_ind(matrix[row, :].flatten(), np.delete(matrix, row, 0).flatten(),
                                          equal_var=False)
                if prob < alpha:
                    sedt_array[row, :] = 1
            # search systematic error in column
            for col in range(shape[1]):
                t, prob = stats.ttest_ind(matrix[:, col].flatten(), np.delete(matrix, col, 1).flatten(),
                                          equal_var=False)
                if prob < alpha:
                    sedt_array[:, col] = 1

            if verbose:
                print("\033[0;32m[INFO]\033[0m Systematics Error Detection Test")
                print(u'\u03B1'" setting for T-Test : ", alpha)
                print(sedt_array)
                print("")

            if path is not None:
                try:
                    np.savetxt(fname=path, X=sedt_array, delimiter=',')
                except Exception:
                    raise IOError("Can't save on defined path")
            return sedt_array
        else:
            raise TypeError("Must provided an Array")
    except Exception as e:
        print("\033[0;31m[ERROR]\033[0m", e)


