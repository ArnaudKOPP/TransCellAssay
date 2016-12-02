# coding=utf-8
"""
Function for making all test more easier
"""

import TransCellAssay as TCA
import numpy as np
import pandas  as pd

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2016 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "GPLv3"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"


def __get_skelleton(plate):

    assert isinstance(plate, TCA.Plate)

    __SIZE__ = len(plate.platemap.platemap.values.flatten())

    gene = plate.platemap.platemap.values.flatten().reshape(__SIZE__, 1)
    final_array = np.append(gene, plate.platemap._fill_empty(plate.platemap._generate_empty(__SIZE__)).values.flatten().reshape(__SIZE__, 1), axis=1)
    final_array = np.append(final_array, np.repeat([str(plate.name)], __SIZE__).reshape(__SIZE__, 1), axis=1)

    x = pd.DataFrame(final_array)
    x.columns = ['PlateMap', 'Well', 'PlateName']
    return x


def __get_negfrom_array(array, neg):
    return array[array['PlateMap'] == neg].iloc[:, 4:]


def ScoringPlate(plate, neg, channel=None, data_c=False, outlier=False):
    """
    Function for easier making score of Plate
    :param plate: plate object
    :param channel: list format if channels to analysis
    :param neg: negative control
    :param data_c: corrected data (spatial norm)
    :param outlier: remove outlier of not
    :return: dataframe
    """
    assert isinstance(plate, TCA.Plate)

    # if no channels provided, then make on cellscount
    if channel is None:
        plate.use_count_as_data()
        if len(plate) == 1:
            df = TCA.plate_ssmd(plate=plate, neg_control=neg, sec_data=data_c, outlier=outlier)
        else:
            df = __multipleReplicaPlate(plate=plate, neg=neg, data_c=data_c, outlier=outlier)
        return df
    else:
        if plate._array_channel != channel:
            plate.agg_data_from_replica_channel(channel=channel, forced_update=True)

        if len(plate) == 1:
            df = TCA.plate_ssmd(plate=plate, neg_control=neg, chan=channel, sec_data=data_c, outlier=outlier)
        else:
            df = __multipleReplicaPlate(plate, neg, channel, data_c, outlier=outlier)
        return df


def __multipleReplicaPlate(plate, neg, chan=None, data_c=False, outlier=False):
    # SSMD
    df = TCA.plate_ssmd(plate=plate, neg_control=neg, chan=chan, sec_data=data_c, outlier=outlier)
    # TStat
    x = TCA.plate_tstat(plate=plate, neg_control=neg, chan=chan, sec_data=data_c, outlier=outlier)
    df = pd.concat([df, x.iloc[:, 5+len(plate):]], axis=1)
    # TTest
    x = TCA.plate_ttest(plate=plate, neg_control=neg, chan=chan, sec_data=data_c, outlier=outlier)
    df = pd.concat([df, x.iloc[:, 5 + len(plate):]], axis=1)
    # KZscore
    x = TCA.plate_kzscore(plate=plate, chan=chan, sec_data=data_c, outlier=outlier)
    df = pd.concat([df, x.iloc[:, 5 + len(plate):]], axis=1)
    # Zscore
    x = TCA.plate_zscore(plate=plate, neg_control=neg, chan=chan, sec_data=data_c, outlier=outlier)
    df = pd.concat([df, x.iloc[:, 5 + len(plate):]], axis=1)
    return df
