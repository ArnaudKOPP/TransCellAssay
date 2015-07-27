# coding=utf-8
"""
Computes the Kolmogorov-Smirnov statistic on 2 samples.

This is a two-sided test for the null hypothesis that 2 independent samples are drawn from the same continuous distribution.
"""
from scipy import stats
import TransCellAssay as TCA
import numpy as np
import logging
log = logging.getLogger(__name__)

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "GPLv3"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"


def plate_kstest(plate, neg, channel, verbose=False, control_plate=None):
    """
    Perform t-test against neg reference for all well of plate/replica
    :param plate: Plate object
    :param neg: negative reference
    :param verbose: print or not result
    :return: numpy array with result
    """
    assert isinstance(plate, TCA.Plate)
    # if no neg was provided raise AttributeError
    if neg is None:
        raise ValueError('Must provided negative control')
    log.info('Perform KS test on plate : {}'.format(plate.name))

    ks_stat = np.zeros(plate.platemap.platemap.shape)
    ks_pvalue = np.zeros(plate.platemap.platemap.shape)

    if control_plate is not None:
        assert isinstance(control_plate, TCA.Plate)
        neg_position = control_plate.platemap.search_well(neg)
        if not neg_position:
            raise Exception("Not Well for control")
        neg_value = control_plate.get_raw_data(channel=channel, well=neg_position)
    else:
        neg_position = plate.platemap.search_well(neg)
        if not neg_position:
            raise Exception("Not Well for control")
        neg_value = plate.get_raw_data(channel=channel, well=neg_position)

    # search rep value for ith well
    for i in range(ks_stat.shape[0]):
        for j in range(ks_stat.shape[1]):
            log.debug("KS on well : {}".format(TCA.get_opposite_well_format((i, j))))
            well_value = list()
            try:
                well_value.extend(plate.get_raw_data(channel=channel, well=TCA.get_opposite_well_format((i, j))))
            except:
                continue
            # # performed unpaired t-test
            ks = stats.stats.ks_2samp(neg_value, well_value)
            ks_stat[i][j] = ks[0]
            ks_pvalue[i][j] = ks[1]

    # # determine fdr
    or_shape = ks_pvalue.shape
    fdr = TCA.adjustpvalues(pvalues=ks_pvalue.flatten())
    fdr = fdr.reshape(or_shape)

    if verbose:
        print("Kolmogorov smirnov test :")
        print("Perform on : {}".format(plate.name))
        print("ks stat score :")
        print(ks_stat)
        print("ks p-value :")
        print(ks_pvalue)
        print("fdr score :")
        print(fdr)
        print("")

    return ks_stat, ks_pvalue, fdr