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
__copyright__ = "© 2014-2016 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "GPLv3"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"


def plate_kzscore(plate, chan=None, sec_data=True, outlier=False):
    """
    Performed zscore on plate object
    unpaired is for plate with replica without great variance between them
    paired is for plate with replica with great variance between them
    :param outlier: remove or not outlier
    :param chan: which chan to use
    :param plate: Plate Object to analyze
    :param sec_data: use data with Systematic Error Corrected
    :return: score data
    """
    assert isinstance(plate, TCA.Plate)
    assert len(plate) > 1

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

    # Outlier removing part
    temp = DF.iloc[:, 4:4+n]
    if outlier:
        mask = temp.apply(TCA.without_outlier_std_based, axis=1)  # Exclude outlier
        VALUE = temp[mask]
        DF.iloc[:, 4:4+n] = VALUE
        DF.loc[:, "Well Mean"] = VALUE.mean(axis=1)

    else:
        VALUE = temp

    DF.loc[:, 'Well Std'] = VALUE.std(axis=1)

    DF.loc[:, "K ZScore"] = ( VALUE.mean(axis=1) - DF.loc[:, "Well Mean"].mean()) / DF.loc[:, "Well Mean"].std()
    DF.loc[:, "K ZScore R"] = ( VALUE.median(axis=1) - DF.loc[:, "Well Mean"].median()) / TCA.mad(DF.loc[:, "Well Mean"].values.flatten())

    return DF
