# coding=utf-8
"""
Function that performed paired/unpaired T-Statistics

For the paired case, a measured value for an siRNA is paired with a median value of a negative reference in the same
plate. The mean and variability of the difference of all these pairs across all plates are used to calculate t stat.
For the unpaired case, all the measured value of an siRNA are formed as a group and all the measured value of a negative
reference in the whole screen are formed as another group. The means and variability of these two separate groups are
used to calculate the t stat.

A large and positive T statistics indicates that three activity readings are consistently higher than the threshold
value µ by a large margin, giving a high degree of confidence that the compound i is highly potent inhibitor. On the
other hand, inconsistency among the three readings, reflected by a small t statistic and high p value as a result of the
large standard deviation, weakens one's belief that the compound i is truly active even when the average of triplicates
may be greater than the cutoff value.
"""

import numpy as np
import TransCellAssay as TCA
from TransCellAssay.Stat.Score.SSMD_old import __search_paired_data, __search_unpaired_data
from TransCellAssay.Utils.Stat import mad
import logging
log = logging.getLogger(__name__)


__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2016 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "GPLv3"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"


def plate_tstat_score_old(plate, neg_control, chan=None, variance='unequal', paired=False, sec_data=True, verbose=False, robust=True,
                      control_plate=None):
    """
    Performed t-stat on plate object
    unpaired is for plate with replica without great variance between them
    paired is for plate with replica with great variance between them
    :param plate: Plate Object to analyze
    :param neg_control:  negative control reference
    :param variance: unequal or equal variance
    :param paired: paired or unpaired
    :param sec_data: use data with Systematic Error Corrected
    :param verbose: be verbose or not
    :return: score data
    """
    assert isinstance(plate, TCA.Plate)
    # if no neg was provided raise AttributeError
    if neg_control is None:
        raise ValueError('Must provided negative control')

    if plate._array_channel != chan and chan is not None:
        plate.agg_data_from_replica_channel(channel=chan, forced_update=True)

    log.info('Perform T-Stat on plate : {0} over channel {1}'.format(plate.name, chan))
    if len(plate) > 1:
        if paired:
            score = __paired_tstat_score(plate, neg_control, sec_data=sec_data, verbose=verbose, robust=robust)
        else:
            score = __unpaired_tstat_score(plate, neg_control, variance=variance, data_c=sec_data,
                                           verbose=verbose, robust=robust, control_plate=control_plate)
    else:
        raise ValueError("T-Stat need at least two replica")
    return score


def __unpaired_tstat_score(plate, neg_control, variance='unequal', data_c=True, verbose=False, robust=True,
                           control_plate=None):
    """
    performed unpaired t-stat score

    variance :
        - unequal : Welch t-test
        - equal : two sample t-test
    :param plate: Plate Object to analyze
    :param neg_control: negative control reference
    :param variance: unequal or equal variance
    :param data_c: use data with Systematic Error Corrected
    :param verbose: be verbose or not
    :return: score data
    """
    ttest_score = np.zeros(plate.platemap.platemap.shape)

    if control_plate is not None:
        neg_position = control_plate.platemap.search_coord(neg_control)
        if not neg_position:
            raise Exception("Not Well for control")
        neg_value = __search_unpaired_data(control_plate, neg_position, data_c)
        nb_neg_wells = len(neg_value)
    else:
        neg_position = plate.platemap.search_coord(neg_control)
        if not neg_position:
            raise Exception("Not Well for control")
        neg_value = __search_unpaired_data(plate, neg_position, data_c)
        nb_neg_wells = len(neg_value)

    nb_rep = len(plate.replica)

    if robust:
        mean_neg = np.median(neg_value)
    else:
        mean_neg = np.mean(neg_value)
    var_neg = np.var(neg_value)

    # search rep value for ith well
    for i in range(ttest_score.shape[0]):
        for j in range(ttest_score.shape[1]):
            well_value = []
            for key, value in plate.replica.items():
                if (i, j) in value.skip_well:
                    continue
                try:
                    if data_c:
                        well_value.append(value.array_c[i][j])
                    else:
                        well_value.append(value.array[i][j])
                except Exception:
                    raise Exception("Your desired datatype are not available")

            if robust:
                mean_rep = np.median(well_value)
            else:
                mean_rep = np.mean(well_value)
            var_rep = np.var(well_value)

            # # performed unpaired t-test
            if variance == 'unequal':
                ttest_score[i][j] = (mean_rep - mean_neg) / np.sqrt(
                    (var_rep**2 / nb_rep) + (var_neg**2 / nb_neg_wells))
            elif variance == 'equal':
                ttest_score[i][j] = (mean_rep - mean_neg) / np.sqrt((2 / (nb_rep + nb_neg_wells - 2)) * (
                    (nb_rep - 1) * var_rep**2 + (nb_neg_wells - 1) * var_neg**2) * ((1 / nb_rep) * (1 / nb_neg_wells)))
            else:
                raise ValueError('Variance attribute must be unequal or equal.')

    if verbose:
        print("Unpaired t-stat :")
        print("Perform on : {}".format(plate.name))
        print("Systematic Error Corrected Data : ", data_c)
        print("Data type : ", plate.datatype)
        print("variance parameter : ", variance)
        print("Robust version : ", robust)
        print("t-stat score :")
        print(ttest_score)
        print("")
    return ttest_score


def __paired_tstat_score(plate, neg_control, sec_data=True, verbose=False, robust=True):
    """
    performed paired t-stat score
    :param plate: Plate Object to analyze
    :param neg_control: negative control reference
    :param sec_data: use data with Systematic Error Corrected
    :param verbose: be verbose or not
    :return: score data
    """
    ttest_score = np.zeros(plate.platemap.platemap.shape)

    neg_position = plate.platemap.search_coord(neg_control)
    if not neg_position:
        raise Exception("Not Well for control")

    for i in range(ttest_score.shape[0]):
        for j in range(ttest_score.shape[1]):
            well_value = []
            for key, value in plate.replica.items():
                if (i, j) in value.skip_well:
                    continue
                neg_median = np.median(__search_paired_data(value, neg_position, sec_data))
                try:
                    if sec_data:
                        well_value.append(value.array_c[i][j] - neg_median)
                    else:
                        well_value.append(value.array[i][j] - neg_median)
                except Exception:
                    raise Exception("Your desired datatype are not available")
            if robust:
                ttest_score[i][j] = np.median(well_value) / (mad(well_value) / np.sqrt(len(plate.replica)))
            else:
                ttest_score[i][j] = np.mean(well_value) / (np.std(well_value) / np.sqrt(len(plate.replica)))

    if verbose:
        print("Paired t-stat :")
        print("Perform on : {}".format(plate.name))
        print("Systematic Error Corrected Data : ", sec_data)
        print("Data type : ", plate.datatype)
        print("Robust version : ", robust)
        print("t-stat score :")
        print(ttest_score)
        print("")
    return ttest_score
