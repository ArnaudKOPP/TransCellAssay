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


def ScoringPlate(plate, channels, neg, robust=False, data_c=False, verbose=False):
    """
    Function for easier making score of Plate
    :param plate:
    :param channels: list format if channels to analysis
    :param neg:
    :param robust:
    :param data_c:
    :param verbose:
    :return:
    """
    assert isinstance(plate, TCA.Plate)
    DF = []
    for chan in channels:
        plate.agg_data_from_replica_channel(channel=chan, forced_update=True)
        if len(plate) == 1:
            df = __singleReplicaPlate(plate, neg, robust, data_c, verbose)
        else:
            df = __multipleReplicaPlate(plate, neg, robust, data_c, verbose)
        df.columns = [np.repeat(str(chan), len(df.columns)), df.columns]
        DF.append(df)
    return pd.concat(DF, axis=1)

def __singleReplicaPlate(plate, neg, robust=False, data_c=False, verbose=False):
    __SIZE__ = len(plate.platemap.platemap.values.flatten())

    gene = plate.platemap.platemap.values.flatten().reshape(__SIZE__, 1)
    final_array = np.append(gene, plate.platemap._fill_empty(plate.platemap._generate_empty(__SIZE__)).values.flatten().reshape(__SIZE__, 1), axis=1)
    final_array = np.append(final_array, np.repeat([str(plate.name)], __SIZE__).reshape(__SIZE__, 1), axis=1)
    final_array = np.append(final_array, plate.array.flatten().reshape(__SIZE__, 1), axis=1)

    x = pd.DataFrame(final_array)
    x.columns = ['PlateMap', 'Well', 'PlateName', 'Well Mean']

    ssmd1 = TCA.plate_ssmd_score(plate, neg_control=neg, method='MM', robust_version=robust, sec_data=data_c,
                             verbose=verbose)
    ssmd2 = TCA.plate_ssmd_score(plate, neg_control=neg, robust_version=robust, sec_data=data_c,
                             verbose=verbose)

    x['SSMD MM'] = ssmd1.flatten().reshape(__SIZE__, 1)
    x['SSMD UMVUE'] = ssmd2.flatten().reshape(__SIZE__, 1)

    return x

def __multipleReplicaPlate(plate, neg, robust=False, data_c=False, verbose=False):

    __SIZE__ = len(plate.platemap.platemap.values.flatten())

    gene = plate.platemap.platemap.values.flatten().reshape(__SIZE__, 1)
    final_array = np.append(gene, plate.platemap._fill_empty(plate.platemap._generate_empty(__SIZE__)).values.flatten().reshape(__SIZE__, 1), axis=1)
    final_array = np.append(final_array, np.repeat([str(plate.name)], __SIZE__).reshape(__SIZE__, 1), axis=1)
    final_array = np.append(final_array, plate.array.flatten().reshape(__SIZE__, 1), axis=1)

    x = pd.DataFrame(final_array)
    x.columns = ['PlateMap', 'Well', 'PlateName', 'Well Mean']

    ssmd1 = TCA.plate_ssmd_score(plate, neg_control=neg, paired=False, robust_version=robust, sec_data=data_c,
                             verbose=verbose)
    ssmd2 = TCA.plate_ssmd_score(plate, neg_control=neg, paired=False, robust_version=robust, sec_data=data_c,
                                 variance="equal", verbose=verbose)
    ssmd3 = TCA.plate_ssmd_score(plate, neg_control=neg, paired=True, robust_version=robust, sec_data=data_c,
                                 verbose=verbose)
    ssmd4 = TCA.plate_ssmd_score(plate, neg_control=neg, paired=True, robust_version=robust, sec_data=data_c,
                                 method='MM', verbose=verbose)
    tstat1 = TCA.plate_tstat_score(plate, neg_control=neg, paired=False, variance='equal', sec_data=data_c,
                                   verbose=verbose, robust=robust)
    tstat2 = TCA.plate_tstat_score(plate, neg_control=neg, paired=False, sec_data=data_c, verbose=verbose,
                                   robust=robust)
    tstat3 = TCA.plate_tstat_score(plate, neg_control=neg, paired=True, sec_data=data_c, verbose=verbose,
                                   robust=robust)

    ttest1, fdr1 = TCA.plate_ttest(plate, neg, verbose=verbose)
    ttest2, fdr2 = TCA.plate_ttest(plate, neg, equal_var=True, verbose=verbose)

    for key, value in plate.replica.items():
        x[value.name] = value.array.flatten().reshape(__SIZE__, 1)

    x['SSMD Unpaired Unequal'] = ssmd1.flatten().reshape(__SIZE__, 1)
    x['SSMD Unpaired Equal'] = ssmd2.flatten().reshape(__SIZE__, 1)
    x['SSMD Paired UMVUE'] = ssmd3.flatten().reshape(__SIZE__, 1)
    x['SSMD Paired MM'] = ssmd4.flatten().reshape(__SIZE__, 1)
    x['TStat Unpaired Equal'] = tstat1.flatten().reshape(__SIZE__, 1)
    x['TStat Unpaired Unequal'] = tstat2.flatten().reshape(__SIZE__, 1)
    x['TStat Paired'] = tstat3.flatten().reshape(__SIZE__, 1)
    x['TTest UnequalVar'] = ttest1.flatten().reshape(__SIZE__, 1)
    x['FDR UnequalVar'] = fdr1.flatten().reshape(__SIZE__, 1)
    x['TTest EqualVar'] = ttest2.flatten().reshape(__SIZE__, 1)
    x['FDR EqualVar'] = fdr2.flatten().reshape(__SIZE__, 1)

    return x
