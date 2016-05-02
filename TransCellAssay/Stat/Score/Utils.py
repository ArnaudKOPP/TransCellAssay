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

def PlateAnalysisScoring(plate, channels, neg, pos=None, threshold=50, percent=True, fixed_threshold=True, robust=True,
                        data_c=False, verbose=False):
    """
    Function that analysis and scoring channels given
    :param plate: plate object
    :param channel: list of channels
    :param neg: negative control
    :param pos: positive control, is optional
    :param threshold: fixe the percent of positive well found in negative control well
    :param percent: True if threshold value is percent, False if we want to give a value
    :param fixed_threshold: use given threshold (value mode) for all well
    :param robust: use mean er median
    :param data_c: corrected data or not
    :param verbose: verbose or not
    :return: result into dataframe
    """
    assert isinstance(plate, TCA.Plate)

    df1, thres = TCA.PlateChannelsAnalysis(plate, channels=channels, neg=neg, pos=pos, threshold=threshold, percent=percent,
                                        fixed_threshold=fixed_threshold, clean=False)
    df2 = ScoringPlate(plate, channels=channels, neg=neg, robust=robust, data_c=data_c, verbose=verbose)

    return pd.concat([df1,df2], axis=1)


def ScoringPlate(plate, neg, channels=None, robust=False, data_c=False, verbose=False):
    """
    Function for easier making score of Plate
    :param plate: plate object
    :param channels: list format if channels to analysis
    :param neg: negative control
    :param robust: use mean or median
    :param data_c: corrected data (spatial norm)
    :param verbose: verbose or not
    :return: dataframe
    """
    assert isinstance(plate, TCA.Plate)
    DF = []
    ## if no channels provided, then make on cellscount
    if channels is None:
        plate.use_count_as_data()
        if len(plate) == 1:
            df = __singleReplicaPlate(plate=plate, neg=neg, robust=robust, data_c=data_c, verbose=verbose)
        else:
            df = __multipleReplicaPlate(plate=plate, neg=neg, robust=robust, data_c=data_c, verbose=verbose)
        df.columns = [np.repeat(str("CellsCount"), len(df.columns)), df.columns]
        DF.append(df)
        return pd.concat(DF, axis=1)
    else:
        for chan in channels:

            if plate._array_channel != chan:
                plate.agg_data_from_replica_channel(channel=chan, forced_update=True)

            if len(plate) == 1:
                df = __singleReplicaPlate(plate, neg, chan, robust, data_c, verbose)
            else:
                df = __multipleReplicaPlate(plate, neg, chan, robust, data_c, verbose)
            df.columns = [np.repeat(str(chan), len(df.columns)), df.columns]
            DF.append(df)
        return pd.concat(DF, axis=1)

def __singleReplicaPlate(plate, neg, chan=None, robust=False, data_c=False, verbose=False):
    __SIZE__ = len(plate.platemap.platemap.values.flatten())

    gene = plate.platemap.platemap.values.flatten().reshape(__SIZE__, 1)
    final_array = np.append(gene, plate.platemap._fill_empty(plate.platemap._generate_empty(__SIZE__)).values.flatten().reshape(__SIZE__, 1), axis=1)
    final_array = np.append(final_array, np.repeat([str(plate.name)], __SIZE__).reshape(__SIZE__, 1), axis=1)
    final_array = np.append(final_array, plate.array.flatten().reshape(__SIZE__, 1), axis=1)

    x = pd.DataFrame(final_array)
    x.columns = ['PlateMap', 'Well', 'PlateName', 'Well Mean']

    ssmd1 = TCA.plate_ssmd_score(plate, neg_control=neg, chan=chan, method='MM', robust_version=robust, sec_data=data_c,
                             verbose=verbose)
    ssmd2 = TCA.plate_ssmd_score(plate, neg_control=neg, chan=chan, robust_version=robust, sec_data=data_c,
                             verbose=verbose)

    x['SSMD MM'] = ssmd1.flatten().reshape(__SIZE__, 1)
    x['SSMD UMVUE'] = ssmd2.flatten().reshape(__SIZE__, 1)

    return x

def __multipleReplicaPlate(plate, neg, chan=None, robust=False, data_c=False, verbose=False):

    __SIZE__ = len(plate.platemap.platemap.values.flatten())

    gene = plate.platemap.platemap.values.flatten().reshape(__SIZE__, 1)
    final_array = np.append(gene, plate.platemap._fill_empty(plate.platemap._generate_empty(__SIZE__)).values.flatten().reshape(__SIZE__, 1), axis=1)
    final_array = np.append(final_array, np.repeat([str(plate.name)], __SIZE__).reshape(__SIZE__, 1), axis=1)
    final_array = np.append(final_array, plate.array.flatten().reshape(__SIZE__, 1), axis=1)

    x = pd.DataFrame(final_array)
    x.columns = ['PlateMap', 'Well', 'PlateName', 'Well Mean']

    ssmd1 = TCA.plate_ssmd_score(plate, neg_control=neg, chan=chan, paired=False, robust_version=robust, sec_data=data_c,
                             verbose=verbose)
    ssmd2 = TCA.plate_ssmd_score(plate, neg_control=neg, chan=chan, paired=False, robust_version=robust, sec_data=data_c,
                                 variance="equal", verbose=verbose)
    ssmd3 = TCA.plate_ssmd_score(plate, neg_control=neg, chan=chan, paired=True, robust_version=robust, sec_data=data_c,
                                 verbose=verbose)
    ssmd4 = TCA.plate_ssmd_score(plate, neg_control=neg, chan=chan, paired=True, robust_version=robust, sec_data=data_c,
                                 method='MM', verbose=verbose)
    tstat1 = TCA.plate_tstat_score(plate, neg_control=neg, chan=chan, paired=False, variance='equal', sec_data=data_c,
                                   verbose=verbose, robust=robust)
    tstat2 = TCA.plate_tstat_score(plate, neg_control=neg, chan=chan, paired=False, sec_data=data_c, verbose=verbose,
                                   robust=robust)
    tstat3 = TCA.plate_tstat_score(plate, neg_control=neg, chan=chan, paired=True, sec_data=data_c, verbose=verbose,
                                   robust=robust)

    ttest1, fdr1 = TCA.plate_ttest(plate, neg, chan=chan, verbose=verbose)
    ttest2, fdr2 = TCA.plate_ttest(plate, neg, chan=chan, equal_var=True, verbose=verbose)

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
