# coding=utf-8
"""
Function that performed Zscore
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


def plate_zscore(plate, neg_control, chan=None, sec_data=True, control_plate=None, outlier=False):
    """
    Performed zscore on plate object
    unpaired is for plate with replica without great variance between them
    paired is for plate with replica with great variance between them
    :param outlier: remove outlier or not
    :param control_plate: use neg reference control in other plate
    :param chan:  on which chan to make it
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
            DF.loc[:, repname+" Mean"] = rep.array_c.flatten().reshape(__SIZE__, 1)
    else:
        DF.loc[:, "Well Mean"] = plate.array.flatten().reshape(__SIZE__, 1)
        for repname, rep in plate:
            DF.loc[:, repname+" Mean"] = rep.array.flatten().reshape(__SIZE__, 1)

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
    temp = DF.iloc[:, 4:4+n]
    if outlier:
        mask = temp.apply(TCA.without_outlier_std_based, axis=1)  # Exclude outlier
        VALUE = temp[mask]
        DF.iloc[:, 4:4+n] = VALUE
        DF.loc[:, "Well Mean"] = VALUE.mean(axis=1)

        mask = neg_data.apply(TCA.without_outlier_std_based, axis=1)
        temp = neg_data[mask]
        temp = temp.apply(lambda x: x.fillna(x.mean()), axis=1)
        neg_data = temp
    else:
        VALUE = temp

    negArray = neg_data.iloc[:, :].values.flatten()
    negArray = negArray[~np.isnan(negArray)]

    DF.loc[:, 'Well Std'] = VALUE.std(axis=1)

    DF.loc[:, "ZScore"] = (VALUE.mean(axis=1) - np.mean(negArray)) / np.std(negArray)
    DF.loc[:, "ZScore R"] = (VALUE.median(axis=1) - np.median(negArray)) / mad(negArray)

    return DF
