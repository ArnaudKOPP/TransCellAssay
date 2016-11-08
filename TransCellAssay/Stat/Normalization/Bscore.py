# coding=utf-8
"""
Tukey's two-ways median polish is utilized to calculate the row and col effect within plates using a non-controls-based
approach. In this method, the row and col medians are iteratively subtracted from all wells until the maximum tolerance
value is reached for the row and col medians as wells as for the row and col effect. The residuals in plate are then
calculated bu subtracting the estimated plate average, row effect and col effect from the true sample value. Since
median parameter is used in the calculations, this method is relatively insensitive to outliers.
-Bscore : this is a normalization parameters which involves the residual values calculated from median polish and the
sample MAD to account for data variability.
-BZscore : This is a modified version of Bscore method, where the median polish is followed by zscore calculations.
While BSscore is more advantageous to Zscore  because of its capability to correct for row and col effect, it is less
powerful than Bscore and does not fit very well with the normal distribution model.

trimmed mean : cut the outside limit default = 0.0 so its equivalent to the 'standard' mean.
"""

import numpy as np
import logging
from TransCellAssay.Utils.Stat import mad
from TransCellAssay.Stat.Normalization.MedianPolish import median_polish
log = logging.getLogger(__name__)


__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2016 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "GPLv3"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"


def bscore(array, max_iterations=10, eps=0.01, verbose=False):
    """
    Implements Tukey's median polish algorithm for additive models
    With non full plate, it work for the moment only with entire empty col or Row
    Get numeric data from numpy ndarray to self.tbl, keep the original copy in tbl_org
    :param array: numpy array to corrected
    :param max_iterations: max iterations in process
    :param eps: epsilon
    :param verbose: print some info
    :return: corrected array
    """
    assert isinstance(array, np.ndarray)

    tbl_org = array

    grand_effect, col_effects, row_effects, tbl, tbl_org = median_polish(tbl_org, max_iterations=max_iterations,
                                                                         eps=eps, verbose=False)
    # become Bscore
    MAD = mad(tbl.flatten())
    tbl = tbl / (MAD)

    if verbose:
        print("Bscore :  ")
        print("grand effect = ", grand_effect)
        print("column effects = ", col_effects)
        print("row effects = ", row_effects)
        print("-----Table of Bscore------")
        print(tbl)
        print("-----Original Table-------")
        print(tbl_org)
        print("")

    return grand_effect, col_effects, row_effects, tbl, tbl_org


def bzscore(array, max_iterations=100, eps=0.01, verbose=False):
    """
    Implements Tukey's median polish algorithm for additive models
    With non full plate, it work for the moment only with entire empty col or Row
    Get numeric data from numpy ndarray to self.tbl, keep the original copy in tbl_org
    BZ-score is a modifed version of bscore method, where the median polish is followed by zscore calculations
    :param array: numpy array to corrected
    :param max_iterations: max iterations in process
    :param eps: epsilon
    :param verbose: print some info
    :return: corrected array
    """
    assert isinstance(array, np.ndarray)

    tbl_org = array

    grand_effect, col_effects, row_effects, tbl, tbl_org = median_polish(tbl_org, max_iterations=max_iterations,
                                                                         eps=eps, verbose=False)

    # become BZscore
    for i in range(tbl.shape[0]):
        for j in range(tbl.shape[1]):
            if not tbl[i][j] == np.NaN:
                tbl[i][j] = (tbl[i][j] - np.mean(tbl.flatten()) / np.std(tbl.flatten()))

    if verbose:
        print("BZscore:  ")
        print("grand effect = ", grand_effect)
        print("column effects = ", col_effects)
        print("row effects = ", row_effects)
        print("-----Table of BZscore-----")
        print(tbl)
        print("-----Original Table-------")
        print(tbl_org)
        print("")

    return grand_effect, col_effects, row_effects, tbl, tbl_org
