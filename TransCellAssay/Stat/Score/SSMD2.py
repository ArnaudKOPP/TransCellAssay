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
import pandas as pd
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

def __get_skelleton(plate):
    __SIZE__ = len(plate.platemap.platemap.values.flatten())

    gene = plate.platemap.platemap.values.flatten().reshape(__SIZE__, 1)
    final_array = np.append(gene, plate.platemap._fill_empty(plate.platemap._generate_empty(__SIZE__)).values.flatten().reshape(__SIZE__, 1), axis=1)
    final_array = np.append(final_array, np.repeat([str(plate.name)], __SIZE__).reshape(__SIZE__, 1), axis=1)

    x = pd.DataFrame(final_array)
    x.columns = ['PlateMap', 'Well', 'PlateName']
    return x

def __get_negfrom_array(array, neg):
    return array[array['PlateMap'] == neg].iloc[:, 3:]


def plate_ssmdTEST(plate, neg_control, chan=None, sec_data=True, control_plate=None, inplate_data=False):
    """
    Performed SSMD on plate object
        unpaired is for plate with replica without great variance between them
        paired is for plate with replica with great variance between them
    :param plate: Plate Object to analyze
    :param neg_control: negative control reference
    :param chan: on which channel tested
    :param sec_data: use data with Systematic Error Corrected
    :param inplate_data: compute SSMD on plate.Data, for plate without replica in preference
    :return: Corrected data
    """
    assert isinstance(plate, TCA.Plate)
    if neg_control is None:
        raise ValueError('Must provided negative control')

    if plate._array_channel != chan and chan is not None:
        plate.agg_data_from_replica_channel(channel=chan, forced_update=True)

    log.info('Perform SSMD on plate : {0} over channel {1}'.format(plate.name, chan))
    if len(plate) > 1 and not inplate_data:
        score = _ssmd_rep(plate, neg_control, sec_data=sec_data,
                                        control_plate=control_plate)
    else:
        score = _ssmd_norep(plate, neg_control, method=method, sec_data=sec_data,
                           control_plate=control_plate)
    return score

def _ssmd_rep(plate, neg_control, sec_data=True, control_plate=None):
    """
    performed unpaired SSMD for plate with replica
    :param plate: Plate Object to analyze
    :param neg_control: negative control reference
    :param sec_data: use data with Systematic Error Corrected
    :return:score data
    """
    __SIZE__ = len(plate.platemap.platemap.values.flatten())
    DF = __get_skelleton(plate)

    if sec_data:
        if plate.array_c is None:
            sec_data = False
            log.warning("sec_data set to False -> data not available")

    if plate.array is None:
        raise ValueError("Set value first")

    ## put wells value into df
    if sec_data:
        DF.loc[:, "Well Mean"] = plate.array_c.flatten().reshape(__SIZE__, 1)
        for repname, rep in plate:
            DF.loc[:, repname+" Mean"] = rep.array_c.flatten().reshape(__SIZE__, 1)
    else:
        DF.loc[:, "Well Mean"] = plate.array.flatten().reshape(__SIZE__, 1)
        for repname, rep in plate:
            DF.loc[:, repname+" Mean"] = rep.array.flatten().reshape(__SIZE__, 1)

    ## search neg data
    if control_plate is not None:
        DF_ctrl = __get_skelleton(plate)
        if sec_data:
            DF_ctrl.loc[:, "Well Value"] = control_plate.array_c.flatten().reshape(__SIZE__, 1)
        else:
            DF_ctrl.loc[:, "Well Value"] = control_platee.array.flatten().reshape(__SIZE__, 1)

        neg_data = __get_negfrom_array(DF_ctrl, neg_control)
    else:
        neg_data = __get_negfrom_array(DF, neg_control)


    ## computed constant
    n = len(plate)
    N = len(neg_data.values.flatten())
    paired_cst = (scipy.special.gamma((n - 1) / 2) / scipy.special.gamma((n - 2) / 2)) * np.sqrt(2 / (n - 1))
    unpaired_cst = 2 * (scipy.special.gamma(((n + N) - 2) / 2) / scipy.special.gamma(((n + N) - 3) / 2)) ** 2


    DF.loc[:, "SSMD UnPaired UnEqual"] = (DF.iloc[:, 4:4+n+1].mean(axis=1) - np.mean(neg_data.iloc[:, 1:].values.flatten())) / np.sqrt(DF.iloc[:, 4:4+n+1].var(axis=1)**2 + np.var(neg_data.iloc[:, 1:].values.flatten())**2)
    DF.loc[:, "SSMD UnPaired Equal"] = (DF.iloc[:, 4:4+n+1].mean(axis=1) - np.mean(neg_data.iloc[:, 1:].values.flatten())) / np.sqrt((2/unpaired_cst) * ((n-1) * DF.iloc[:, 4:4+n+1].var(axis=1)**2 + (len(neg_data.iloc[:, 1:].values.flatten())+1) * np.var(neg_data.iloc[:, 1:].values.flatten())**2 ))
    DF.loc[:, "SSMD UnPaired UnEqual R"] = (DF.iloc[:, 4:4+n+1].median(axis=1) - np.median(neg_data.iloc[:, 1:].values.flatten())) / np.sqrt(DF.iloc[:, 4:4+n+1].var(axis=1)**2 + np.var(neg_data.iloc[:, 1:].values.flatten())**2)
    DF.loc[:, "SSMD UnPaired Equal R"] = (DF.iloc[:, 4:4+n+1].median(axis=1) - np.median(neg_data.iloc[:, 1:].values.flatten())) / np.sqrt((2/unpaired_cst) * ((n-1) * DF.iloc[:, 4:4+n+1].var(axis=1)**2 + (len(neg_data.iloc[:, 1:].values.flatten())+1) * np.var(neg_data.iloc[:, 1:].values.flatten())**2 ))


    x = (DF.iloc[:, 4:4+n+1] - neg_data.iloc[:, 1:].mean())

    DF.loc[:, "SSMD Paired UMVUE"] = paired_cst * (x.mean(axis=1) / x.std(axis=1))
    DF.loc[:, "SSMD Paired MM"]  =(x.mean(axis=1) / x.std(axis=1))

    x = (DF.iloc[:, 4:4+n+1] - neg_data.iloc[:, 1:].median())

    DF.loc[:, "SSMD Paired UMVUE R"] = paired_cst * (x.median(axis=1) / x.apply(mad, axis=1))
    DF.loc[:, "SSMD Paired MM R"] = x.median(axis=1) / x.apply(mad, axis=1)

    return DF

def _ssmd_norep(plate, neg_control, sec_data=False, control_plate=None):
    """
    performed SSMD for plate without replica
    take dataMean/Median or SECDatadata from plate object
    :param plate: Plate Object to analyze
    :param neg_control: negative control reference
    :param sec_data: use data with Systematic Error Corrected
    :return:score data
    """
    __SIZE__ = len(plate.platemap.platemap.values.flatten())
    DF = __get_skelleton(plate)

    if sec_data:
        if plate.array_c is None:
            sec_data = False
            log.warning("sec_data set to False -> data not available")

    if plate.array is None:
        raise ValueError("Set value first")

    ## put wells value into df
    if sec_data:
        DF.loc[:, "Well Value"] = plate.array_c.flatten().reshape(__SIZE__, 1)
    else:
        DF.loc[:, "Well Value"] = plate.array.flatten().reshape(__SIZE__, 1)

    ## search neg data
    if control_plate is not None:
        DF_ctrl = __get_skelleton(plate)
        if sec_data:
            DF_ctrl .loc[:, "Well Value"] = control_plate.array_c.flatten().reshape(__SIZE__, 1)
        else:
            DF_ctrl .loc[:, "Well Value"] =control_platee.array.flatten().reshape(__SIZE__, 1)

        neg_data = __get_negfrom_array(DF_ctrl, neg_control).values.flatten()
    else:
        neg_data = __get_negfrom_array(DF, neg_control).values.flatten()


    n = len(neg_data)
    # k = 2 * (scipy.special.gamma(((n - 1) / 2) / scipy.special.gamma((n - 2) / 2))) ** 2
    k = n-2.48


    DF.loc[:, "SSMD Robust MM"] = (DF.loc[:, "Well Value"] - np.median(neg_data)) / (np.sqrt(2) * mad(neg_data))
    DF.loc[:, "SSMD Robust UMVUE"] = (DF.loc[:, "Well Value"] - np.median(neg_data)) / (np.sqrt((2 / k) * (len(neg_data))) * mad(neg_data))
    DF.loc[:, "SSMD MM"] = (DF.loc[:, "Well Value"] - np.mean(neg_data)) / (np.sqrt(2) * np.std(neg_data))
    DF.loc[:, "SSMD UMVUE"] = (DF.loc[:, "Well Value"] - np.mean(neg_data)) / (np.sqrt((2 / k) * (len(neg_data))) * np.std(neg_data))

    return DF
