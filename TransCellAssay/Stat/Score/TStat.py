# coding=utf-8
"""
Function that performed paired/unpaired T-Statistics

For the paired case, a measured value for an siRNA is paired with a median value of a negative reference in the same
plate. The mean and variability of the difference of all these pairs accross all plates are used to calculate t stat.
For the unpaired case, all the measured value of an siRNA are formed as a group and all the measured value of a negative
reference in the whole screen are formed as another group. The means and variability of these two separate groups are
used to calculate the t stat.

A large and positive T statistics indicates that three activity readings are consistently higher than the threshold
value µ by a large margin, giving a high degree of confidence that the compound i is highly potent inhibitor. On the
other hand, inconsistency among the three readings, reflected by a small t statistic and high p value as a result of the
large standart deviation, weakens one's belief that the compound i is truly active even when the average of tripilcates
may be greater than the cutoff value.
"""

import numpy as np
import TransCellAssay as TCA
from TransCellAssay.Stat.Score.SSMD import __search_paired_data, __search_unpaired_data
import logging
log = logging.getLogger(__name__)


__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


def plate_tstat_score(plate, neg_control, variance='unequal', paired=False, sec_data=True, verbose=False):
    """
    Performed t-stat on plate object
    unpaired is for plate with replicat without great variance between them
    paired is for plate with replicat with great variance between them
    :param plate: Plate Object to analyze
    :param neg_control:  negative control reference
    :param variance: unequal or equal variance
    :param paired: paired or unpaired
    :param sec_data: use data with Systematic Error Corrected
    :param verbose: be verbose or not
    :return: score data
    """
    try:
        if isinstance(plate, TCA.Plate):
            # if no neg was provided raise AttributeError
            if neg_control is None:
                raise ValueError('Must provided negative control')
            log.info('Perform T-Stat on plate : {}'.format(plate.name))
            if len(plate) > 1:
                if paired:
                    score = __paired_tstat_score(plate, neg_control, sec_data=sec_data, verbose=verbose)
                else:
                    score = __unpaired_tstat_score(plate, neg_control, variance=variance, sec_data=sec_data,
                                                   verbose=verbose)
            else:
                raise ValueError("T-Stat need at least two replicat")
            return score
        else:
            raise TypeError('Take only plate')
    except Exception as e:
        log.error(e)


def __unpaired_tstat_score(plate, neg_control, variance='unequal', sec_data=True, verbose=False):
    """
    performed unpaired t-stat score

    variance :
        - unequal : Welch t-test
        - equal : two sample t-test
    :param plate: Plate Object to analyze
    :param neg_control: negative control reference
    :param variance: unequal or equal variance
    :param sec_data: use data with Systematic Error Corrected
    :param verbose: be verbose or not
    :return: score data
    """
    ttest_score = np.zeros(plate.platemap.platemap.shape)

    neg_position = plate.platemap.search_coord(neg_control)
    if not neg_position:
        raise Exception("Not Well for control")

    nb_rep = len(plate.replica)
    neg_value = __search_unpaired_data(plate, neg_position, sec_data)

    nb_neg_wells = len(neg_value)
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
                    if sec_data:
                        well_value.append(value.sec_array[i][j])
                    else:
                        well_value.append(value.array[i][j])
                except Exception:
                    raise Exception("Your desired datatype are not available")
            mean_rep = np.mean(well_value)
            var_rep = np.var(well_value)

            # # performed unpaired t-test
            if variance == 'unequal':
                ttest_score[i][j] = (mean_rep - mean_neg) / np.sqrt(
                    (var_rep / nb_rep) + (var_neg / nb_neg_wells))
            elif variance == 'equal':
                ttest_score[i][j] = (mean_rep - mean_neg) / np.sqrt((2 / (nb_rep + nb_neg_wells - 2)) * (
                    (nb_rep - 1) * var_rep + (nb_neg_wells - 1) * var_neg) * ((1 / nb_rep) * (1 / nb_neg_wells)))
            else:
                raise ValueError('Variance attribut must be unequal or equal.')

    if verbose:
        print("Unpaired t-stat :")
        print("Systematic Error Corrected Data : ", sec_data)
        print("Data type : ", plate.datatype)
        print("variance parameter : ", variance)
        print("t-stat score :")
        print(ttest_score)
        print("")
    return ttest_score


def __paired_tstat_score(plate, neg_control, sec_data=True, verbose=False):
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
                        well_value.append(value.sec_array[i][j] - neg_median)
                    else:
                        well_value.append(value.array[i][j] - neg_median)
                except Exception:
                    raise Exception("Your desired datatype are not available")
            ttest_score[i][j] = np.mean(well_value) / (
                np.std(well_value) / np.sqrt(len(plate.replica)))

    if verbose:
        print("Paired t-stat :")
        print("Systematic Error Corrected Data : ", sec_data)
        print("Data type : ", plate.datatype)
        print("t-stat score :")
        print(ttest_score)
        print("")
    return ttest_score