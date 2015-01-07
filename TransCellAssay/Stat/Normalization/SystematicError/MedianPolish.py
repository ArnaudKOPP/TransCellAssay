# coding=utf-8
"""
Tukey's two-ways median polish is utilized to calculate the row and col effect within plates using a non-controls-based
approach. In this method, the row and col medians are iteratively subtracted from all wells until the maximum tolerance
value is reached for the row and col medians as wells as for the row and col effect. The residuals in plate are then
calculated bu subtracting the estimated plate average, row effect and col effect from the true sample value. Since
median parameter is used in the calculations, this method is relatively insensitive to outliers.
-Bscore : this is a normalization parameters which involves the residual values calculated from median polish and the
sample MAD to account for data variability.
-BZscore : This is a modified version of Bscore method, where the median polish is folowed by zscore calculations. While
BSscore is more advantageous to Zscore  because of its capability to correct for row and col effect, it is less
powerfull than Bscore and does not fit very well with the normal distribution model.

trimmed mean : cut the outside limit default = 0.0 so its equivalent to the 'standart' mean.
"""

import numpy as np
from scipy import stats
from TransCellAssay.Utils.stat_misc import mad


__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


def median_polish(array, max_iterations=100, method='median', trimmed=0.0, verbose=False):
    """
    Implements Tukey's median polish alghoritm for additive models
        method - default is median, alternative is mean. That would give us result equal ANOVA.
        With non full plate, it work for the moment only with entire empty col or Row
        Get numeric data from numpy ndarray to self.tbl, keep the original copy in tbl_org
    :param array: numpy array to corrected
    :param max_iterations: max iterations in process
    :param method: median or average method
    :param trimmed: for average method only, trimmed the data with specified value, default is 0.0
    :param verbose: print some info
    :return: corrected array
    """
    try:
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
                    row_medians = stats.nanmedian(stats.mstats.trim(tbl, (trimmed, 1 - trimmed), axis=1), axis=1)
                    row_effects += row_medians
                    median_row_effects = stats.nanmedian(row_effects)
                elif method == 'average':
                    row_medians = stats.nanmean(stats.mstats.trim(tbl, (trimmed, 1 - trimmed), axis=1), axis=1)
                    row_effects += row_medians
                    median_row_effects = stats.nanmean(row_effects)
                grand_effect += median_row_effects
                row_effects -= median_row_effects
                tbl -= row_medians[:, np.newaxis]

                if method == 'median':
                    col_medians = stats.nanmedian(stats.mstats.trim(tbl, (trimmed, 1 - trimmed), axis=0), axis=0)
                    col_effects += col_medians
                    median_col_effects = stats.nanmedian(col_effects)
                elif method == 'average':
                    col_medians = stats.nanmean(stats.mstats.trim(tbl, (trimmed, 1 - trimmed), axis=0), axis=0)
                    col_effects += col_medians
                    median_col_effects = stats.nanmean(col_effects)

                tbl -= col_medians

                grand_effect += median_col_effects
            # become Bscore
            MAD = mad(tbl.flatten())
            tbl = tbl / (MAD)

            # # replace NaN with 0
            tbl = np.nan_to_num(tbl)
            np.set_printoptions(suppress=True)
            if verbose:
                print("Bscore :  ")
                print("Method used :", method)
                print("Max Iteration : ", max_iterations)
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
            raise TypeError('\033[0;31m[ERROR]\033[0m  Expected the argument to be a numpy.ndarray.')
    except Exception as e:
        print("\033[0;31m[ERROR]\033[0m", e)


def bz_median_polish(array, max_iterations=100, method='median', trimmed=0.0, verbose=False):
    """
    Implements Tukey's median polish alghoritm for additive models
        method - default is median, alternative is mean. That would give us result equal ANOVA.
        With non full plate, it work for the moment only with entire empty col or Row
        Get numeric data from numpy ndarray to self.tbl, keep the original copy in tbl_org
        BZ-score is a modifed version of bscore method, where the median polish is followed by zscore calculations
    :param array: numpy array to corrected
    :param max_iterations: max iterations in process
    :param method: median or average method
    :param trimmed: for average method only, trimmed the data with specified value, default is 0.0
    :param verbose: print some info
    :return: corrected array
    """
    try:
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
                    row_medians = stats.nanmedian(stats.mstats.trim(tbl, (trimmed, 1 - trimmed), axis=1), axis=1)
                    row_effects += row_medians
                    median_row_effects = stats.nanmedian(row_effects)
                elif method == 'average':
                    row_medians = stats.nanmean(stats.mstats.trim(tbl, (trimmed, 1 - trimmed), axis=1), axis=1)
                    row_effects += row_medians
                    median_row_effects = stats.nanmean(row_effects)
                grand_effect += median_row_effects
                row_effects -= median_row_effects
                tbl -= row_medians[:, np.newaxis]

                if method == 'median':
                    col_medians = stats.nanmedian(stats.mstats.trim(tbl, (trimmed, 1 - trimmed), axis=0), axis=0)
                    col_effects += col_medians
                    median_col_effects = stats.nanmedian(col_effects)
                elif method == 'average':
                    col_medians = stats.nanmean(stats.mstats.trim(tbl, (trimmed, 1 - trimmed), axis=0), axis=0)
                    col_effects += col_medians
                    median_col_effects = stats.nanmean(col_effects)

                tbl -= col_medians

                grand_effect += median_col_effects

            # # replace NaN with 0
            tbl = np.nan_to_num(tbl)

            # become BZscore
            for i in range(tbl.shape[0]):
                for j in range(tbl.shape[1]):
                    if not tbl[i][j] == np.NaN:
                        tbl[i][j] = (tbl[i][j] - np.mean(tbl.flatten()) / np.std(tbl.flatten()))

            np.set_printoptions(suppress=True)
            if verbose:
                print("BZscore:  ")
                print("Method used :", method)
                print("Max Iteration : ", max_iterations)
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
            raise TypeError('\033[0;31m[ERROR]\033[0m  Expected the argument to be a numpy.ndarray.')
    except Exception as e:
        print("\033[0;31m[ERROR]\033[0m", e)