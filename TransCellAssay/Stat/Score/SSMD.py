# coding=utf-8
"""
Function that performed paired/unpaired SSMD and for plate without replica

SSMD is the mean of differences divided bu the standard deviation of the differences between an siRNA and a negative
reference. In other words, SSMD is the average fold change (on the log scale) penalized by the variability of fold
change (on the log scale).

In a screen without replicas, we cannot directly calculate the variability of each siRNA. Thus, like z-score, we have
to assume that each siRNA has the same variability as a negative reference and then calculate the variability based
on the negative reference and/or all investigated siRNAs. On the basis of this assumption, we can calculate SSMD using
method-of-moment(MM) method or the uniformly minimal variance unbiased estimate(UMVUE) method. The use of robust version
is highly recommended.

In a screen with replicas:
For the paired case, a measured value for an siRNA is paired with a median value of a negative reference in the same
plate. The mean and variability of the difference of all these pairs across all plates are used to calculate SSMD.
For the unpaired case, all the measured value of an siRNA are formed as a group and all the measured value of a negative
reference in the whole screen are formed as another group. The means and variability of these two separate groups are
used to calculate the SSMD.
"""

import numpy as np
import scipy.special
import TransCellAssay as TCA
from TransCellAssay.Utils.Stat import mad
import logging
log = logging.getLogger(__name__)


__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2016 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "GPLv3"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"


def plate_ssmd_score(plate, neg_control, chan=None, paired=True, robust_version=True, method='UMVUE', variance='unequal',
                     sec_data=True, control_plate=None, inplate_data=False, verbose=False):
    """
    Performed SSMD on plate object
        unpaired is for plate with replica without great variance between them
        paired is for plate with replica with great variance between them
    :param plate: Plate Object to analyze
    :param neg_control: negative control reference
    :param chan: on which channel tested
    :param paired: paired or unpaired statistic
    :param robust_version: use robust version or not
    :param method: which method to use MM or UMVUE
    :param variance: unequal or equal
    :param sec_data: use data with Systematic Error Corrected
    :param inplate_data: compute SSMD on plate.Data, for plate without replica in preference
    :param verbose: be verbose or not
    :return: Corrected data
    """
    assert isinstance(plate, TCA.Plate)
    if neg_control is None:
        raise ValueError('Must provided negative control')

    if plate._array_channel != chan and chan is not None:
        plate.agg_data_from_replica_channel(channel=chan, forced_update=True)

    log.info('Perform SSMD on plate : {0} over channel {1}'.format(plate.name, chan))
    if len(plate) > 1 and not inplate_data:
        if not paired:
            score = __unpaired_ssmd(plate, neg_control, variance=variance, sec_data=sec_data,
                                        verbose=verbose, robust=robust_version, control_plate=control_plate)
        else:
            score = __paired_ssmd(plate, neg_control, method=method, sec_data=sec_data, verbose=verbose,
                                      robust=robust_version)
    else:
        score = __ssmd(plate, neg_control, method=method, sec_data=sec_data, verbose=verbose, robust=robust_version,
                           control_plate=control_plate)
    return score


def __search_unpaired_data(plate, ref, sec_data):
    assert isinstance(plate, TCA.Plate)
    neg_value = []
    for key, value in plate.replica.items():
        # # remove skipped Wells
        if len(value.skip_well) > 0:
            valid_neg_position = [x for x in ref if (x not in value.skip_well)]
        else:
            valid_neg_position = ref
        for neg in valid_neg_position:
            try:
                if sec_data:
                    neg_value.append(value.array_c[neg[0]][neg[1]])
                else:
                    neg_value.append(value.array[neg[0]][neg[1]])
            except Exception:
                raise Exception("Your desired datatype are not available")
    return neg_value


def __unpaired_ssmd(plate, neg_control, variance='unequal', sec_data=True, control_plate=None, verbose=False,
                    robust=True):
    """
    performed unpaired SSMD for plate with replica
    :param plate: Plate Object to analyze
    :param neg_control: negative control reference
    :param variance: unequal or equal
    :param sec_data: use data with Systematic Error Corrected
    :param verbose: be verbose or not
    :param robust: if robust, use median, else use mean
    :return:score data
    """
    if variance not in ['unequal', 'equal']:
        raise ValueError('Wrong variance choice')

    ssmd = np.zeros(plate.platemap.platemap.shape)

    if control_plate is not None:
        neg_position = control_plate.platemap.search_coord(neg_control)
        if not neg_position:
            raise Exception("Not Well for control")
        neg_value = __search_unpaired_data(control_plate, neg_position, sec_data)
    else:
        neg_position = plate.platemap.search_coord(neg_control)
        if not neg_position:
            raise Exception("Not Well for control")
        neg_value = __search_unpaired_data(plate, neg_position, sec_data)

    nb_neg_wells = len(neg_value)

    if robust:
        mean_median_neg = np.median(neg_value)
    else:
        mean_median_neg = np.mean(neg_value)
    var_neg = np.var(neg_value)

    n = len(plate)
    N = len(neg_value)
    k = 2 * (scipy.special.gamma(((n + N) - 2) / 2) / scipy.special.gamma(((n + N) - 3) / 2)) ** 2
    # k = len(plate) + len(neg_value) - 3.48

    # search rep value for ith well
    for i in range(ssmd.shape[0]):
        for j in range(ssmd.shape[1]):
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
            if robust:
                mean_rep = np.median(well_value)
            else:
                mean_rep = np.mean(well_value)
            var_rep = np.var(well_value)

            if variance == 'unequal':
                ssmd[i][j] = (mean_rep - mean_median_neg) / np.sqrt(var_rep**2 + var_neg**2)
            elif variance == 'equal':
                ssmd[i][j] = (mean_rep - mean_median_neg) / np.sqrt(
                    (2 / k) * ((n - 1) * var_rep**2 + (nb_neg_wells - 1) * var_neg**2))

    if verbose:
        print("Unpaired SSMD :")
        print("Perform on : {}".format(plate.name))
        print("Robust version : ", robust)
        print("Systematic Error Corrected Data : ", sec_data)
        print("Data type : ", plate.datatype)
        print("variance parameter : ", variance)
        print("SSMD score :")
        print(ssmd)
        print("")
    return ssmd


def __search_paired_data(replica, ref, sec_data):
    assert isinstance(replica, TCA.Replica)
    # # remove skipped Wells
    if len(replica.skip_well) > 0:
        valid_neg_pos = [x for x in ref if (x not in replica.skip_well)]
    else:
        valid_neg_pos = ref
    neg_value = []
    for neg_i in valid_neg_pos:
        try:
            if sec_data:
                well_value = replica.array_c[neg_i[0]][neg_i[1]]
            else:
                well_value = replica.array[neg_i[0]][neg_i[1]]
            neg_value.append(well_value)
        except Exception:
            raise Exception("Your desired datatype are not available")
    return neg_value


def __paired_ssmd(plate, neg_control, method='UMVUE', sec_data=True, verbose=False, robust=True):
    """
    performed paired ssmd for plate with replica
    :param plate: Plate Object to analyze
    :param neg_control: negative control reference
    :param method: which method to use MM or UMVUE
    :param sec_data: use data with Systematic Error Corrected
    :param verbose: be verbose or not
    :param robust: if robust, use median, else use mean
    :return:score data
    """
    if method not in ['UMVUE', 'MM']:
        raise ValueError('Wrong method choice')

    ssmd = np.zeros(plate.platemap.platemap.shape)

    neg_position = plate.platemap.search_coord(neg_control)
    if not neg_position:
        raise Exception("Not Well for control")

    n = len(plate)
    x = (scipy.special.gamma((n - 1) / 2) / scipy.special.gamma((n - 2) / 2)) * np.sqrt(2 / (n - 1))

    try:
        for i in range(ssmd.shape[0]):
            for j in range(ssmd.shape[1]):
                well_value = []
                for key, value in plate.replica.items():
                    if (i, j) in value.skip_well:
                        continue
                    if robust:
                        neg = np.median(__search_paired_data(value, neg_position, sec_data))
                    else:
                        neg = np.mean(__search_paired_data(value, neg_position, sec_data))
                    if sec_data:
                        well_value.append(value.array_c[i][j] - neg)
                    else:
                        well_value.append(value.array[i][j] - neg)
                if robust:
                    if method == 'UMVUE':
                        ssmd[i][j] = x * (np.median(well_value) / mad(well_value))
                    elif method == 'MM':
                        ssmd[i][j] = np.median(well_value) / mad(well_value)
                else:
                    if method == 'UMVUE':
                        ssmd[i][j] = x * (np.mean(well_value) / np.std(well_value))
                    elif method == 'MM':
                        ssmd[i][j] = np.mean(well_value) / np.std(well_value)

        if verbose:
            print("Paired SSMD :")
            print("Perform on : {}".format(plate.name))
            print("Robust version : ", robust)
            print("Systematic Error Corrected Data : ", sec_data)
            print("Data type : ", plate.datatype)
            print("method parameter : ", method)
            print("SSMD score :")
            print(ssmd)
            print("")
    except Exception as e:
        print(e)
    return ssmd


def __ssmd(plate, neg_control, method='UMVUE', sec_data=True, control_plate=None, verbose=False, robust=True):
    """
    performed SSMD for plate without replica
    take dataMean/Median or SECDatadata from plate object
    :param plate: Plate Object to analyze
    :param neg_control: negative control reference
    :param method: which method to use MM or UMVUE
    :param sec_data: use data with Systematic Error Corrected
    :param verbose: be verbose or not
    :param robust: if robust, use median, else use mean
    :return:score data
    """
    # TODO make using a control_plate

    if method not in ['UMVUE', 'MM']:
        raise ValueError('Wrong method choice')

    ps = plate.platemap
    ssmd = np.zeros(ps.platemap.shape)

    neg_well = ps.search_coord(neg_control)
    # # remove skipped Wells
    if len(plate.skip_well) > 0:
        valid_neg_pos = [x for x in neg_well if (x not in plate.skip_well)]
    else:
        valid_neg_pos = neg_well
    if not valid_neg_pos:
        raise Exception("Not Well for control")
    neg_data = []

    try:
        if sec_data:
            data = plate.array_c
        else:
            data = plate.array
    except Exception as e:
        raise Exception("Your desired datatype are not available")

    # grab all neg data
    for neg_pos in valid_neg_pos:
        neg_data.append(data[neg_pos[0]][neg_pos[1]])
    # check if len is sufficient
    if len(neg_data) < 2:
        raise ValueError('Insuficient negative data')

    n = len(neg_data)
    # k = 2 * (scipy.special.gamma(((n - 1) / 2) / scipy.special.gamma((n - 2) / 2))) ** 2
    k = n-2.48

    if robust:
        if method == 'MM':
            ssmd = (data - np.median(neg_data)) / (np.sqrt(2) * mad(neg_data))
        elif method == 'UMVUE':
            ssmd = (data - np.median(neg_data)) / (np.sqrt((2 / k) * (len(neg_data))) * mad(neg_data))
    else:
        if method == 'MM':
            ssmd = (data - np.mean(neg_data)) / (np.sqrt(2) * np.std(neg_data))
        elif method == 'UMVUE':
            ssmd = (data - np.mean(neg_data)) / (np.sqrt((2 / k) * (len(neg_data))) * np.std(neg_data))

    if verbose:
        print('SSMD without replica, or inplate data from plate')
        print("Perform on : {}".format(plate.name))
        print("Robust version : ", robust)
        print("Systematic Error Corrected Data : ", sec_data)
        print("Data type : ", plate.datatype)
        print("method parameter : ", method)
        print("SSMD score :")
        print(ssmd)
        print("")
    return ssmd
