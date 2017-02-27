# coding=utf-8
"""
Tukey's two-ways median polish is utilized to calculate the row and col effect within plates using a non-controls-based
approach. In this method, the row and col medians are iteratively subtracted from all wells until the maximum tolerance
value is reached for the row and col medians as wells as for the row and col effect. The residuals in plate are then
calculated bu subtracting the estimated plate average, row effect and col effect from the true sample value. Since
median parameter is used in the calculations, this method is relatively insensitive to outliers.
"""

import numpy as np
import logging
log = logging.getLogger(__name__)


__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2017 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "GPLv3"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"


def median_polish(array, max_iterations=10, eps=0.01, verbose=False):
    """
    Implements Tukey's median polish algorithm for additive models, implementation used is from R lang
    With non full plate, it work for the moment only with entire empty col or Row
    Get numeric data from numpy ndarray to self.tbl, keep the original copy in tbl_org
    :param array: numpy array to corrected
    :param max_iterations: max iterations in process
    :param eps: epsilon
    :param verbose: print result or not
    :return: corrected array
    """
    assert isinstance(array, np.ndarray)

    tbl_org = array
    z = tbl_org.copy()

    converged = False
    oldsum = 0
    t = 0
    r = np.zeros(shape=z.shape[0])
    c = np.zeros(shape=z.shape[1])

    for i in range(max_iterations):
        log.debug('Median Polish : iteration %s' % i)
        rdelta = np.median(z, axis=1)
        z -= rdelta[:, np.newaxis]
        r += rdelta
        delta = np.median(r)
        c += delta
        r -= delta
        cdelta = np.median(z, axis=0)
        z -= cdelta[np.newaxis, :]
        c += cdelta
        delta = np.median(c)
        r -= delta
        t += delta

        # log.debug("rows medians {0} & rows effects {1}".format(rdelta, r))
        # log.debug("col med {0} \ncol eff {1}".format(cdelta, c))

        newsum = np.sum(z.reshape(1, -1))

        if newsum == 0 or np.abs(newsum - oldsum) < eps*newsum:
            converged = True

        if converged:
            # log.debug("Median polish converged at iteration : {}".format(i))
            break
        oldsum = newsum

    if verbose:
        print("Median Polish:  ")
        print("grand effect = ", t)
        print("column effects = ", c)
        print("row effects = ", r)
        print("-----Table of Residuals-------")
        print(z)
        print("-----Original Table-------")
        print(tbl_org)
        print("")

    return t, c, r, z, tbl_org
