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
from TransCellAssay.Stat.Score.SSMD import __search_paired_data, __search_unpaired_data
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


def plate_tstatTEST(plate, neg_control, chan=None, sec_data=False, control_plate=None):
    """
    Performed t-stat on plate object
    unpaired is for plate with replica without great variance between them
    paired is for plate with replica with great variance between them
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


    DF.loc[:, "TStat UnPaired Equal"] = ( DF.iloc[:, 4:4+n+1].mean(axis=1) - np.mean(neg_data.iloc[:, 1:].values.flatten())) / np.sqrt((DF.iloc[:, 4:4+n+1].var(axis=1)**2 / n) + (np.var(neg_data.iloc[:, 1:].values.flatten())**2)/len(neg_data.iloc[:, 1:].values.flatten()))
    DF.loc[:, "TStat UnPaired Equal R"] = ( DF.iloc[:, 4:4+n+1].median(axis=1) - np.median(neg_data.iloc[:, 1:].values.flatten())) / np.sqrt((DF.iloc[:, 4:4+n+1].var(axis=1)**2 / n) + (np.var(neg_data.iloc[:, 1:].values.flatten())**2)/len(neg_data.iloc[:, 1:].values.flatten()))


    nb_rep = n
    nb_neg_wells = len(neg_data.iloc[:, 1:].values.flatten())
    var_neg = np.var(neg_data.iloc[:, 1:].values.flatten())
    var_rep = DF.iloc[:, 4:4+n+1].var(axis=1)

    DF.loc[:, "TStat UnPaired UnEqual"] = ( DF.iloc[:, 4:4+n+1].mean(axis=1) - np.mean(neg_data.iloc[:, 1:].values.flatten())) / np.sqrt((2 / (nb_rep + nb_neg_wells - 2)) * ((nb_rep - 1) * var_rep**2 + (nb_neg_wells - 1) * var_neg**2) * ((1 / nb_rep) * (1 / nb_neg_wells)))
    DF.loc[:, "TStat UnPaired UnEqual R"] = ( DF.iloc[:, 4:4+n+1].median(axis=1) - np.median(neg_data.iloc[:, 1:].values.flatten())) / np.sqrt((2 / (nb_rep + nb_neg_wells - 2)) * ((nb_rep - 1) * var_rep**2 + (nb_neg_wells - 1) * var_neg**2) * ((1 / nb_rep) * (1 / nb_neg_wells)))

    x = (DF.iloc[:, 4:4+n+1] - neg_data.iloc[:, 1:].mean())
    DF.loc[:, "TStat Paired "] = x.mean(axis=1) / (x.std(axis=1) / np.sqrt(n))

    x = (DF.iloc[:, 4:4+n+1] - neg_data.iloc[:, 1:].median())
    DF.loc[:, "TStat Paired R"] = x.median(axis=1) / (x.apply(mad, axis=1) / np.sqrt(n))

    return DF
