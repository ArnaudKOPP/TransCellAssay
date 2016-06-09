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
import numpy as np
import pandas as pd
from TransCellAssay.Stat.Score.Utils import __get_skelleton, __get_negfrom_array
import logging
log = logging.getLogger(__name__)

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2016 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "GPLv3"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"



def plate_ttestTEST(plate, neg_control, chan=None, sec_data=True, control_plate=None, outlier=False):
    """
    Perform t-test against neg reference for all well of plate/replica
    :param plate: Plate object
    :param neg: negative reference
    :param sec_data: use sec data
    :return: numpy array with result
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


    ## Outlier removing part
    temp = DF.iloc[:, 4:4+n]
    if outlier:
        mask = temp.apply(TCA.without_outlier_std_based, axis=1) ##Exclude outlier
        VALUE = temp[mask]
        DF.iloc[:, 4:4+n] = VALUE
        DF.loc[:, "Well Mean"] = VALUE.mean(axis=1)

        mask = neg_data.apply(TCA.without_outlier_std_based, axis=1)
        temp = neg_data[mask]
        temp = temp.apply(lambda x: x.fillna(x.mean()), axis=1)
        neg_data = temp
    else:
        VALUE = temp

    neg_values = neg_data.iloc[:,:].values.flatten()

    DF.loc[:, 'Well Std'] = VALUE .std(axis=1)

    DF.loc[:, "TTest EqualVar P-Val"] = VALUE .apply(lambda x : stats.ttest_ind(a=x, b=neg_values, equal_var=True)[1], axis=1)
    DF.loc[:, "TTest EqualVar FDR"] = TCA.adjustpvalues(pvalues=DF.loc[:, "TTest EqualVar P-Val"])
    DF.loc[:, "TTest UnEqualVar P-Val"] = VALUE .apply(lambda x : stats.ttest_ind(a=x, b=neg_values, equal_var=False)[1], axis=1)
    DF.loc[:, "TTest UnEqualVar FDR"] = TCA.adjustpvalues(pvalues=DF.loc[:, "TTest UnEqualVar P-Val"])

    return DF
