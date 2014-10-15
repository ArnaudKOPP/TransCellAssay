__author__ = 'Arnaud KOPP'
"""
Define method for median polish, this algo is used for removing edge effect
"""
import numpy as np
from scipy import stats


def MedianPolish(array, max_iterations=100, method='median', verbose=False):
    """
        Implements Tukey's median polish alghoritm for additive models
        method - default is median, alternative is mean. That would give us result equal ANOVA.
        With non full plate, it work for the moment only with entire empty col or Row
        Get numeric data from numpy ndarray to self.tbl, keep the original copy in tbl_org
    """
    if isinstance(array, np.ndarray):
        tbl_org = array
        tbl = tbl_org.copy()

        # # replace 0 with NaN
        tbl[tbl == 0] = np.NaN
        grand_effect = 0
        median_row_effects = 0
        median_col_effects = 0
        row_effects = np.zeros(shape=tbl.shape[0])
        col_effects = np.zeros(shape=tbl.shape[1])

        for i in range(max_iterations):
            if method == 'median':
                row_medians = stats.nanmedian(tbl, 1)
                row_effects += row_medians
                median_row_effects = stats.nanmedian(row_effects)
            elif method == 'average':
                row_medians = stats.nanmean(tbl, 1)
                row_effects += row_medians
                median_row_effects = stats.nanmean(row_effects)
            grand_effect += median_row_effects
            row_effects -= median_row_effects
            tbl -= row_medians[:, np.newaxis]

            if method == 'median':
                col_medians = stats.nanmedian(tbl, 0)
                col_effects += col_medians
                median_col_effects = stats.nanmedian(col_effects)
            elif method == 'average':
                col_medians = stats.nanmean(tbl, 0)
                col_effects += col_medians
                median_col_effects = stats.nanmean(col_effects)

            tbl -= col_medians

            grand_effect += median_col_effects
        MAD = mad(tbl.flatten())
        tbl = tbl / (1.4826 * MAD)
        # # replace NaN with 0
        tbl = np.nan_to_num(tbl)
        np.set_printoptions(suppress=True)
        if verbose:
            print("median polish:  ")
            print("grand effect = ", grand_effect)
            print("column effects = ", col_effects)
            print("row effects = ", row_effects)
            print("-----Table of Residuals-------")
            print(tbl)
            print("-----Original Table-------")
            print(tbl_org)
            print("")

        return grand_effect, col_effects, row_effects, tbl, tbl_org
    else:
        raise TypeError('Expected the argument to be a numpy.ndarray.')


def mad(arr):
    """ Median Absolute Deviation: a "Robust" version of standard deviation.
        Indices variabililty of the sample.
        https://en.wikipedia.org/wiki/Median_absolute_deviation
    """
    try:
        arr = np.ma.array(arr).compressed()  # should be faster to not use masked arrays.
        med = np.median(arr)
        return np.median(np.abs(arr - med))
    except Exception as e:
        print(e)