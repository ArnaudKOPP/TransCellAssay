# coding=utf-8
"""
Calculates the T-test for the means of TWO INDEPENDENT samples of scores.
This is a two-sided test for the null hypothesis that 2 independent samples have identical average (expected) values.
This test assumes that the populations have identical variances.

We can use this test, if we observe two independent samples from the same or different population, e.g. exam scores of
boys and girls or of two ethnic groups. The test measures whether the average (expected) value differs significantly
across samples. If we observe a large p-value, for example larger than 0.05 or 0.1, then we cannot reject the null
hypothesis of identical average scores. If the p-value is smaller than the threshold, e.g. 1%, 5% or 10%, then we
reject the null hypothesis of equal averages.
"""
from scipy import stats
import TransCellAssay as TCA
from TransCellAssay.Stat.Score.SSMD_old import __search_unpaired_data
import numpy as np
import logging
log = logging.getLogger(__name__)

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2016 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "GPLv3"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"


def plate_ttest_score_old(plate, neg, chan=None, sec_data=False, equal_var=False, verbose=False, control_plate=None):
    """
    Perform t-test against neg reference for all well of plate/replica
    :param chan: which chan to use
    :param plate: Plate object
    :param neg: negative reference
    :param sec_data: use sec data
    :param equal_var: equal variance or not
    :param verbose: print or not result
    :return: numpy array with result
    """
    assert isinstance(plate, TCA.Plate)
    # if no neg was provided raise AttributeError
    if neg is None:
        raise ValueError('Must provided negative control')

    if plate._array_channel != chan and chan is not None:
        plate.agg_data_from_replica_channel(channel=chan, forced_update=True)

    log.info('Perform T-Test on plate : {0} over channel {1}'.format(plate.name, chan))

    if len(plate) > 1:

        ttest_score = np.zeros(plate.platemap.platemap.shape)

        if control_plate is not None:
            neg_position = control_plate.platemap.search_coord(neg)
            if not neg_position:
                raise Exception("Not Well for control")
            neg_value = __search_unpaired_data(control_plate, neg_position, sec_data)
        else:
            neg_position = plate.platemap.search_coord(neg)
            if not neg_position:
                raise Exception("Not Well for control")
            neg_value = __search_unpaired_data(plate, neg_position, sec_data)

        # search rep value for ith well
        for i in range(ttest_score.shape[0]):
            for j in range(ttest_score.shape[1]):
                well_value = []
                for key, value in plate.replica.items():
                    if (i, j) in value.skip_well:
                        continue
                    try:
                        if sec_data:
                            well_value.append(value.array_c[i][j])
                        else:
                            well_value.append(value.array[i][j])
                    except Exception:
                        raise Exception("Your desired datatype are not available")

                # # performed unpaired t-test
                ttest_score[i][j] = stats.ttest_ind(neg_value, well_value, equal_var=equal_var)[1]

        # # determine fdr
        or_shape = ttest_score.shape
        fdr = TCA.adjustpvalues(pvalues=ttest_score.flatten())
        fdr = fdr.reshape(or_shape)

        if verbose:
            print("Unpaired ttest :")
            print("Perform on : {}".format(plate.name))
            print("Systematic Error Corrected Data : ", sec_data)
            print("Data type : ", plate.datatype)
            print("Equal variance : ", equal_var)
            print("ttest p-value score :")
            print(ttest_score)
            print("fdr score :")
            print(fdr)
            print("")

    else:
        raise ValueError("T-test need at least two replica")
    return ttest_score, fdr
