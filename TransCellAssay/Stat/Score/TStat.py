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
import pandas as pd
import TransCellAssay as TCA
from TransCellAssay.Utils.Stat import mad
from TransCellAssay.Stat.Score.Utils import __get_skelleton, __get_negfrom_array
import logging

log = logging.getLogger(__name__)

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2017 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "GPLv3"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"


def plate_tstat(plate, neg_control, chan=None, sec_data=True, control_plate=None, outlier=False):
    """
    Performed t-stat on plate object
    unpaired is for plate with replica without great variance between them
    paired is for plate with replica with great variance between them
    :param outlier: remove or not outlier
    :param control_plate: use neg reference control from other plate
    :param chan: which chan to use
    :param plate: Plate Object to analyze
    :param neg_control:  negative control reference
    :param sec_data: use data with Systematic Error Corrected
    :return: score data
    """
    assert isinstance(plate, TCA.Plate)
    assert len(plate) > 1

    # if no neg was provided raise AttributeError
    if neg_control is None:
        raise ValueError('Must provided negative control')

    if plate._array_channel != chan and chan is not None:
        plate.agg_data_from_replica_channel(channel=chan, forced_update=True)

    n = len(plate)
    __SIZE__ = len(plate.platemap.platemap.values.flatten())
    DF = __get_skelleton(plate)

    if sec_data:
        if plate.array_c is None:
            sec_data = False
            log.warning("sec_data set to False -> data not available")
    else:
        if plate.array is None:
            raise ValueError("Set value first")

    # put wells value into df
    if sec_data:
        DF.loc[:, "Well Mean"] = plate.array_c.flatten().reshape(__SIZE__, 1)
        for repname, rep in plate:
            DF.loc[:, repname + " Mean"] = rep.array_c.flatten().reshape(__SIZE__, 1)
    else:
        DF.loc[:, "Well Mean"] = plate.array.flatten().reshape(__SIZE__, 1)
        for repname, rep in plate:
            DF.loc[:, repname + " Mean"] = rep.array.flatten().reshape(__SIZE__, 1)

    # search neg data
    if control_plate is not None:
        DF_ctrl = __get_skelleton(plate)
        if sec_data:
            DF_ctrl.loc[:, "Well Value"] = control_plate.array_c.flatten().reshape(__SIZE__, 1)
        else:
            DF_ctrl.loc[:, "Well Value"] = control_plate.array.flatten().reshape(__SIZE__, 1)

        neg_data = __get_negfrom_array(DF_ctrl, neg_control)
    else:
        neg_data = __get_negfrom_array(DF, neg_control)

    # Outlier removing part
    temp = DF.iloc[:, 4:4 + n]
    if outlier:
        mask = temp.apply(TCA.without_outlier_std_based, axis=1)  # Exclude outlier
        VALUE = temp[mask]
        DF.iloc[:, 4:4 + n] = VALUE
        DF.loc[:, "Well Mean"] = VALUE.mean(axis=1)

        mask = neg_data.apply(TCA.without_outlier_std_based, axis=1)
        temp = neg_data[mask]
        temp = temp.apply(lambda x: x.fillna(x.mean()), axis=1)
        neg_data = temp
    else:
        VALUE = temp

    negArray = neg_data.iloc[:, :].values.flatten()
    negArray = negArray[~np.isnan(negArray)]
    nb_neg_wells = len(negArray)

    DF.loc[:, 'Well Std'] = VALUE.std(axis=1)

    DF.loc[:, "TStat UnPaired Equal"] = (VALUE.mean(axis=1) - np.mean(negArray)) / np.sqrt(
        (VALUE.var(axis=1) ** 2 / n) + (np.var(negArray) ** 2) / nb_neg_wells)
    DF.loc[:, "TStat UnPaired Equal R"] = (VALUE.median(axis=1) - np.median(negArray)) / np.sqrt(
        (VALUE.var(axis=1) ** 2 / n) + (np.var(negArray) ** 2) / nb_neg_wells)

    nb_rep = n
    var_neg = np.var(neg_data.iloc[:, :].values.flatten())
    var_rep = VALUE.var(axis=1)

    DF.loc[:, "TStat UnPaired UnEqual"] = (VALUE.mean(axis=1) - np.mean(negArray)) / np.sqrt(
        (2 / (nb_rep + nb_neg_wells - 2)) * ((nb_rep - 1) * var_rep ** 2 + (nb_neg_wells - 1) * var_neg ** 2) * (
            (1 / nb_rep) * (1 / nb_neg_wells)))
    DF.loc[:, "TStat UnPaired UnEqual R"] = (VALUE.median(axis=1) - np.median(negArray)) / np.sqrt(
        (2 / (nb_rep + nb_neg_wells - 2)) * ((nb_rep - 1) * var_rep ** 2 + (nb_neg_wells - 1) * var_neg ** 2) * (
            (1 / nb_rep) * (1 / nb_neg_wells)))

    x = (VALUE - neg_data.iloc[:, :].mean())
    DF.loc[:, "TStat Paired "] = x.mean(axis=1) / (x.std(axis=1) / np.sqrt(n))

    x = (VALUE - neg_data.iloc[:, :].median())
    DF.loc[:, "TStat Paired R"] = x.median(axis=1) / (x.apply(mad, axis=1) / np.sqrt(n))

    return DF
