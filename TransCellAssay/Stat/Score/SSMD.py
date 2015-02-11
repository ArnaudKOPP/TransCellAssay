# coding=utf-8
"""
Function that performed paired/unpaired SSMD and for plate without replicat

SSMD is the mean of differences divided bu the standard deviation of the differences between an siRNA and a negative
reference. In other words, SSMD is the average fold change (on the log scale) penalized by the variability of fold
change (on the log scsale).

In a screen without replicats, we cannot directly calculate the variability of each siRNA. Thus, like z-score, we have
to assume that each siRNA has the same variability as a negative reference and then calculate the variability based
on the negative reference and/or all investiged siRNAs. On the basis of this assumption, we can calculate SSMD using
method-of-moment(MM) method or the uniformy minimal variance unbiased estimate(UMVUE) method. The use of rebust version
is highly recommended.

In a screen with replicats:
For the paired case, a measured value for an siRNA is paired with a median value of a negative reference in the same
plate. The mean and variability of the difference of all these pairs accross all plates are used to calculate SSMD.
For the unpaired case, all the measured value of an siRNA are formed as a group and all the measured value of a negative
reference in the whole screen are formed as another group. The means and variability of these two separate groups are
used to calculate the ssmd.
"""

import numpy as np
import scipy.special
import TransCellAssay as TCA
from TransCellAssay.Utils.Stat import mad


__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


def plate_ssmd_score(plate, neg_control, paired=True, robust_version=True, method='UMVUE', variance='unequal',
                     sec_data=True, inplate_data=False, verbose=False):
    """
    Performed SSMD on plate object
        unpaired is for plate with replicat without great variance between them
        paired is for plate with replicat with great variance between them
    :param plate: Plate Object to analyze
    :param neg_control: negative control reference
    :param paired: paired or unpaired statistic
    :param robust_version: use robust version or not
    :param method: which method to use MM or UMVUE
    :param variance: unequal or equal
    :param sec_data: use data with Systematic Error Corrected
    :param inplate_data: compute SSMD on plate.Data, for plate without replicat in preference
    :param verbose: be verbose or not
    :return: Corrected data
    """
    try:
        if isinstance(plate, TCA.Plate):
            # if no neg was provided raise AttributeError
            if neg_control is None:
                raise ValueError('Must provided negative control')
            print('\033[0;32m[INFO]\033[0m Performe SSMD')
            if len(plate) > 1 and not inplate_data:
                if not paired:
                    if robust_version:
                        score = __unpaired_ssmdr(plate, neg_control, variance=variance, sec_data=sec_data,
                                                 verbose=verbose)
                    else:
                        score = __unpaired_ssmd(plate, neg_control, variance=variance, sec_data=sec_data,
                                                verbose=verbose)
                else:
                    if robust_version:
                        score = __paired_ssmdr(plate, neg_control, method=method, sec_data=sec_data, verbose=verbose)
                    else:
                        score = __paired_ssmd(plate, neg_control, method=method, sec_data=sec_data, verbose=verbose)
            else:
                if robust_version:
                    score = __ssmdr(plate, neg_control, method=method, sec_data=sec_data, verbose=verbose)
                else:
                    score = __ssmd(plate, neg_control, method=method, sec_data=sec_data, verbose=verbose)
            return score
        else:
            raise TypeError('Take only plate')
    except Exception as e:
        print(e)


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
                    neg_value.append(value.sec_array[neg[0]][neg[1]])
                else:
                    neg_value.append(value.array[neg[0]][neg[1]])
            except Exception:
                raise Exception("Your desired datatype are not available")
    return neg_value


def __unpaired_ssmd(plate, neg_control, variance='unequal', sec_data=True, verbose=False):
    """
    performed unpaired SSMD for plate with replicat
    :param plate: Plate Object to analyze
    :param neg_control: negative control reference
    :param variance: unequal or equal
    :param sec_data: use data with Systematic Error Corrected
    :param verbose: be verbose or not
    :return:score data
    """
    ssmd = np.zeros(plate.platemap.platemap.shape)

    neg_position = plate.platemap.search_coord(neg_control)
    if not neg_position:
        raise Exception("Not Well for control")

    nb_rep = len(plate.replica)
    neg_value = __search_unpaired_data(plate, neg_position, sec_data)

    nb_neg_wells = len(neg_value)
    mean_neg = np.mean(neg_value)
    var_neg = np.var(neg_value)

    k = 2 * (scipy.special.gamma(
        ((len(neg_value) - 1) / 2) / scipy.special.gamma((len(neg_value) - 2) / 2))) ** 2
    # search rep value for ith well
    for i in range(ssmd.shape[0]):
        for j in range(ssmd.shape[1]):
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
                ssmd[i][j] = (mean_rep - mean_neg) / np.sqrt(var_rep + var_neg)
            elif variance == 'equal':
                ssmd[i][j] = (mean_rep - mean_neg) / np.sqrt(
                    (2 / k) * ((nb_rep - 1) * var_rep + (nb_neg_wells - 1) * var_neg))
            else:
                raise ValueError('Variance attribut must be unequal or equal.')

    if verbose:
        print("Unpaired SSMD :")
        print("Systematic Error Corrected Data : ", sec_data)
        print("Data type : ", plate.datatype)
        print("variance parameter : ", variance)
        print("SSMD score :")
        print(ssmd)
        print("")
    return ssmd


def __unpaired_ssmdr(plate, neg_control, variance='unequal', sec_data=True, verbose=False):
    """
    performed unpaired SSMDr for plate with replicat
    :param plate: Plate Object to analyze
    :param neg_control: negative control reference
    :param variance: unequal or equal
    :param sec_data: use data with Systematic Error Corrected
    :param verbose: be verbose or not
    :return:score data
    """
    ssmd = np.zeros(plate.platemap.platemap.shape)

    neg_position = plate.platemap.search_coord(neg_control)
    if not neg_position:
        raise Exception("Not Well for control")

    nb_rep = len(plate.replica)
    neg_value = __search_unpaired_data(plate, neg_position, sec_data)

    nb_neg_wells = len(neg_value)
    median_neg = np.median(neg_value)
    var_neg = np.var(neg_value)

    k = 2 * (scipy.special.gamma(
        ((len(neg_value) - 1) / 2) / scipy.special.gamma((len(neg_value) - 2) / 2))) ** 2
    # search rep value for ith well
    for i in range(ssmd.shape[0]):
        for j in range(ssmd.shape[1]):
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
            median_rep = np.median(well_value)
            var_rep = np.var(well_value)

            # # performed unpaired t-test
            if variance == 'unequal':
                ssmd[i][j] = (median_rep - median_neg) / np.sqrt(var_rep + var_neg)
            elif variance == 'equal':
                ssmd[i][j] = (median_rep - median_neg) / np.sqrt(
                    (2 / k) * ((nb_rep - 1) * var_rep + (nb_neg_wells - 1) * var_neg))
            else:
                raise ValueError('Variance attribut must be unequal or equal.')

    if verbose:
        print("Unpaired SSMDr :")
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
                well_value = replica.sec_array[neg_i[0]][neg_i[1]]
            else:
                well_value = replica.array[neg_i[0]][neg_i[1]]
            neg_value.append(well_value)
        except Exception:
            raise Exception("Your desired datatype are not available")
    return neg_value


def __paired_ssmd(plate, neg_control, method='UMVUE', sec_data=True, verbose=False):
    """
    performed paired ssmd for plate with replicat
    :param plate: Plate Object to analyze
    :param neg_control: negative control reference
    :param method: which method to use MM or UMVUE
    :param sec_data: use data with Systematic Error Corrected
    :param verbose: be verbose or not
    :return:score data
    """
    ssmd = np.zeros(plate.platemap.platemap.shape)

    neg_position = plate.platemap.search_coord(neg_control)
    if not neg_position:
        raise Exception("Not Well for control")

    x = (scipy.special.gamma((len(plate.replica) - 1) / 2) / scipy.special.gamma(
        (len(plate.replica) - 2) / 2)) * np.sqrt(2 / (len(plate.replica) - 1))

    try:
        for i in range(ssmd.shape[0]):
            for j in range(ssmd.shape[1]):
                well_value = []
                for key, value in plate.replica.items():
                    if (i, j) in value.skip_well:
                        continue
                    neg_mean = np.mean(__search_paired_data(value, neg_position, sec_data))
                    if sec_data:
                        well_value.append(value.sec_array[i][j] - neg_mean)
                    else:
                        well_value.append(value.array[i][j] - neg_mean)
                if method == 'UMVUE':
                    ssmd[i][j] = x * (np.mean(well_value) / np.std(well_value))
                elif method == 'MM':
                    ssmd[i][j] = np.mean(well_value) / np.std(well_value)
                else:
                    raise ValueError('Method must me UMVUE or MM')

        if verbose:
            print("Paired SSMD :")
            print("Systematic Error Corrected Data : ", sec_data)
            print("Data type : ", plate.datatype)
            print("method parameter : ", method)
            print("SSMD score :")
            print(ssmd)
            print("")
    except Exception as e:
        print(e)
    return ssmd


def __paired_ssmdr(plate, neg_control, method='UMVUE', sec_data=True, verbose=False):
    """
    performed paired SSMDr for plate with replicat
    :param plate: Plate Object to analyze
    :param neg_control: negative control reference
    :param method: which method to use MM or UMVUE
    :param sec_data: use data with Systematic Error Corrected
    :param verbose: be verbose or not
    :return:score data
    """
    ssmdr = np.zeros(plate.platemap.platemap.shape)

    neg_position = plate.platemap.search_coord(neg_control)
    if not neg_position:
        raise Exception("Not Well for control")

    x = (scipy.special.gamma((len(plate.replica) - 1) / 2) / scipy.special.gamma(
        (len(plate.replica) - 2) / 2)) * np.sqrt(2 / (len(plate.replica) - 1))

    print(x)

    try:
        for i in range(ssmdr.shape[0]):
            for j in range(ssmdr.shape[1]):
                well_value = []
                for key, value in plate.replica.items():
                    if (i, j) in value.skip_well:
                        continue
                    neg_median = np.median(__search_paired_data(value, neg_position, sec_data))
                    if sec_data:
                        well_value.append(value.sec_array[i][j] - neg_median)
                    else:
                        well_value.append(value.array[i][j] - neg_median)
                if method == 'UMVUE':
                    ssmdr[i][j] = x * (np.median(well_value) / mad(well_value))
                elif method == 'MM':
                    ssmdr[i][j] = np.median(well_value) / mad(well_value)
                else:
                    raise ValueError('Method must me UMVUE or MM')

        if verbose:
            print("Paired SSMDr :")
            print("Systematic Error Corrected Data : ", sec_data)
            print("Data type : ", plate.datatype)
            print("method parameter : ", method)
            print("SSMDr score :")
            print(ssmdr)
            print("")
    except Exception as e:
        print(e)
    return ssmdr


def __ssmd(plate, neg_control, method='UMVUE', sec_data=True, verbose=False):
    """
    performed SSMD for plate without replicat
    take dataMean/Median or SECDatadata from plate object
    :param plate: Plate Object to analyze
    :param neg_control: negative control reference
    :param method: which method to use MM or UMVUE
    :param sec_data: use data with Systematic Error Corrected
    :param verbose: be verbose or not
    :return:score data
    """
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
    data = None
    try:
        if sec_data:
            data = plate.sec_array
        else:
            data = plate.array
    except Exception as e:
        print(e)
    if data is None:
        raise Exception("Your desired datatype are not available")
    # grab all neg data
    for neg_pos in valid_neg_pos:
        neg_data.append(data[neg_pos[0]][neg_pos[1]])
    # check if len is sufficient
    if len(neg_data) < 2:
        raise ValueError('Insuficient negative data')

    if method == 'MM':
        ssmd = (data - np.mean(neg_data)) / (np.sqrt(2) * np.std(neg_data))
    elif method == 'UMVUE':
        k = 2 * (scipy.special.gamma(
            ((len(neg_data) - 1) / 2) / scipy.special.gamma((len(neg_data) - 2) / 2))) ** 2
        ssmd = (data - np.mean(neg_data)) / (np.sqrt((2 / k) * (len(neg_data))) * np.std(neg_data))
    else:
        raise ValueError('Method must be MM or UMVUE')

    if verbose:
        print('SSMD without replicat, or inplate data from plate')
        print("Systematic Error Corrected Data : ", sec_data)
        print("Data type : ", plate.datatype)
        print("method parameter : ", method)
        print("SSMD score :")
        print(ssmd)
        print("")
    return ssmd


def __ssmdr(plate, neg_control, method='UMVUE', sec_data=True, verbose=False):
    """
    perfored  SSMDr for plate without replicat
    take dataMean/Median or SECDatadata from plate object
    :param plate: Plate Object to analyze
    :param neg_control: negative control reference
    :param method: which method to use MM or UMVUE
    :param sec_data: use data with Systematic Error Corrected
    :param verbose: be verbose or not
    :return:score data
    """
    ps = plate.platemap
    ssmdr = np.zeros(ps.platemap.shape)

    neg_well = ps.search_coord(neg_control)
    # # remove skipped Wells
    if len(plate.skip_well) > 0:
        valid_neg_pos = [x for x in neg_well if (x not in plate.skip_well)]
    else:
        valid_neg_pos = neg_well
    if not valid_neg_pos:
        raise Exception("Not Well for control")
    neg_data = []
    data = None
    try:
        if sec_data:
            data = plate.sec_array
        else:
            data = plate.array
    except Exception as e:
        print(e)
    if data is None:
        raise Exception("Your desired datatype are not available")
    # grab all neg data
    for neg_pos in valid_neg_pos:
        neg_data.append(data[neg_pos[0]][neg_pos[1]])
    # check if len is sufficient
    if len(neg_data) < 2:
        raise ValueError('Insuficient negative data')

    if method == 'MM':
        ssmdr = (data - np.median(neg_data)) / (np.sqrt(2) * mad(neg_data))
    elif method == 'UMVUE':
        k = 2 * (scipy.special.gamma(
            ((len(neg_data) - 1) / 2) / scipy.special.gamma((len(neg_data) - 2) / 2))) ** 2
        ssmdr = (data - np.median(neg_data)) / (np.sqrt((2 / k) * (len(neg_data))) * mad(neg_data))
    else:
        raise ValueError('Method must be MM or UMVUE')

    if verbose:
        print('SSMDr without replicat')
        print("Systematic Error Corrected Data : ", sec_data)
        print("Data type : ", plate.datatype)
        print("method parameter : ", method)
        print("SSMD score :")
        print(ssmdr)
        print("")
    return ssmdr