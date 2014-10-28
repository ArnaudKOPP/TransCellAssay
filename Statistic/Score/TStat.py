"""
Function that performed paired/unpaired T-Statistics

For the paired case, a measured value for an siRNA is paired with a median value of a negative reference in the same
plate. The mean and variability of the difference of all these pairs accross all plates are used to calculate t stat.
For the unpaired case, all the measured value of an siRNA are formed as a group and all the measured value of a negative
reference in the whole screen are formed as another group. The means and variability of these two separate groups are
used to calculate the t stat.

A large and positive T statistics indicates that three activity readings are consistently higher than the threshold
value µ by a large margin, giving a high degree of confidence that the compound i is highly potent inhibitor. On the
other hand, inconsistency among the three readings, reflected by a small t statistic and high p value as a result of the
large standart deviation, weakens one's belief that the compound i is truly active even when the average of tripilcates
may be greater than the cutoff value.
"""

import ScreenPlateReplicatPS
import numpy as np

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


def t_stat_score(plate, cNeg, data='median', variance='unequal', paired=False, SECData=True, verbose=False):
    """
    Performed t-stat on plate object
    unpaired is for plate with replicat without great variance between them
    paired is for plate with replicat with great variance between them
    :param plate: Plate Object to analyze
    :param cNeg:  negative control reference
    :param data: median or mean data to use
    :param variance: unequal or equal variance
    :param paired: paired or unpaired
    :param SECData: use data with Systematic Error Corrected
    :param verbose: be verbose or not
    :return: score data
    """
    try:
        if isinstance(plate, ScreenPlateReplicatPS.Plate):
            # if no neg was provided raise AttributeError
            if cNeg is None:
                raise AttributeError('\033[0;31m[ERROR]\033[0m  Must provided negative control')
            if len(plate) > 1:
                if paired:
                    score = _PairedTStatScore(plate, cNeg, data=data, SECData=SECData, verbose=verbose)
                else:
                    score = _UnpairedTStatScore(plate, cNeg, data=data, variance=variance, SECData=SECData,
                                                verbose=verbose)
            else:
                raise ValueError("\033[0;31m[ERROR]\033[0m  T-Test need at least two replicat")
            return score
        else:
            raise TypeError
    except Exception as e:
        print(e)


def _UnpairedTStatScore(plate, cNeg, data='median', variance='unequal', SECData=True, verbose=False):
    """
    performed unpaired t-stat score

    variance :
        - unequal : Welch t-test
        - equal : two sample t-test
    :param plate: Plate Object to analyze
    :param cNeg: negative control reference
    :param data: median or mean data to use
    :param variance: unequal or equal variance
    :param SECData: use data with Systematic Error Corrected
    :param verbose: be verbose or not
    :return: score data
    """
    try:
        if cNeg is None:
            raise AttributeError('\033[0;31m[ERROR]\033[0m  Must provided negative control')
        if isinstance(plate, ScreenPlateReplicatPS.Plate):
            ttest_score = np.zeros(plate.PlateSetup.platesetup.shape)

            # # replace 0 with NaN
            ttest_score[ttest_score == 0] = np.NaN

            nb_rep = len(plate.replicat)

            neg_value = []
            neg_pos = plate.PlateSetup.getGenePos(cNeg)
            if not neg_pos:
                raise Exception
            # search neg control value
            for i in range(ttest_score.shape[0]):
                for j in range(ttest_score.shape[1]):
                    for key, value in plate.replicat.items():
                        well_value = 0
                        try:
                            if data == "median":
                                if SECData:
                                    well_value = value.SECMedian[i][j]
                                else:
                                    well_value = value.DataMedian[i][j]
                            elif data == "mean":
                                if SECData:
                                    well_value = value.SECDataMean[i][j]
                                else:
                                    well_value = value.DataMean[i][j]
                            else:
                                raise AttributeError('\033[0;31m[ERROR]\033[0m  Data type must be mean or median')
                        except Exception:
                            raise Exception("\033[0;31m[ERROR]\033[0m  Your desired datatype are not available")
                        # check if neg value
                        for neg_i in neg_pos:
                            if neg_i[0] == i:
                                if neg_i[1] == j:
                                    neg_value.append(well_value)
            nb_neg_wells = len(neg_value)
            mean_neg = np.nanmean(neg_value)
            var_neg = np.nanvar(neg_value)

            # search rep value for ith well
            for i in range(ttest_score.shape[0]):
                for j in range(ttest_score.shape[1]):
                    well_value = []
                    for key, value in plate.replicat.items():
                        try:
                            if data == "median":
                                if SECData:
                                    well_value.append(value.SECDataMedian[i][j])
                                else:
                                    well_value.append(value.DataMedian[i][j])
                            elif data == "mean":
                                if SECData:
                                    well_value.append(value.SECDataMean[i][j])
                                else:
                                    well_value.append(value.DataMean[i][j])
                            else:
                                raise AttributeError('\033[0;31m[ERROR]\033[0m  Data type must be mean or median')
                        except Exception:
                            raise Exception("\033[0;31m[ERROR]\033[0m  Your desired datatype are not available")
                    mean_rep = np.nanmean(well_value)
                    var_rep = np.nanvar(well_value)

                    # # performed unpaired t-test
                    if variance == 'unequal':
                        ttest_score[i][j] = (mean_rep - mean_neg) / np.sqrt(
                            (var_rep / nb_rep) + (var_neg / nb_neg_wells))
                    elif variance == 'equal':
                        ttest_score[i][j] = (mean_rep - mean_neg) / np.sqrt((2 / (nb_rep + nb_neg_wells - 2)) * (
                            (nb_rep - 1) * var_rep + (nb_neg_wells - 1) * var_neg) * (
                                                                                (1 / nb_rep) * (1 / nb_neg_wells)))
                    else:
                        raise AttributeError('\033[0;31m[ERROR]\033[0m  variance attribut must be unequal or equal.')

            # # replace NaN with 0
            ttest_score = np.nan_to_num(ttest_score)

            if verbose:
                print("Unpaired t-test :")
                print("Systematic Error Corrected Data : ", SECData)
                print("Data type : ", data)
                print("variance parameter : ", variance)
                print("t-test score :")
                print(ttest_score)
                print("")
            return ttest_score
        else:
            raise TypeError
    except Exception as e:
        print(e)


def _PairedTStatScore(plate, cNeg, data='median', SECData=True, verbose=False):
    """
    performed paired t-stat score
    :param plate: Plate Object to analyze
    :param cNeg: negative control reference
    :param data: median or mean data to use
    :param SECData: use data with Systematic Error Corrected
    :param verbose: be verbose or not
    :return: score data
    """
    try:
        if cNeg is None:
            raise AttributeError('\033[0;31m[ERROR]\033[0m  Must provided negative control')
        if isinstance(plate, ScreenPlateReplicatPS.Plate):
            ttest_score = np.zeros(plate.PlateSetup.platesetup.shape)

            # # replace 0 with NaN
            ttest_score[ttest_score == 0] = np.NaN

            neg_pos = plate.PlateSetup.getGenePos(cNeg)
            if not neg_pos:
                raise Exception

            # search neg control value
            def _search_neg_data(replicat, Neg_Pos, Type):
                neg_value = []
                try:
                    for i in range(ttest_score.shape[0]):
                        for j in range(ttest_score.shape[1]):
                            try:
                                if data == "median":
                                    if SECData:
                                        well_value.append(replicat.SECDataMedian[i][j])
                                    else:
                                        well_value.append(replicat.DataMedian[i][j])
                                elif data == "mean":
                                    if SECData:
                                        well_value.append(replicat.SECDataMean[i][j])
                                    else:
                                        well_value.append(replicat.DataMean[i][j])
                                else:
                                    raise AttributeError('\033[0;31m[ERROR]\033[0m  Data type must be mean or median')
                            except Exception:
                                raise Exception("\033[0;31m[ERROR]\033[0m  Your desired datatype are not available")
                            # check if neg value
                            for neg_i in Neg_Pos:
                                if neg_i[0] == i:
                                    if neg_i[1] == j:
                                        neg_value.append(well_value)
                    return np.nanmedian(neg_value)
                except Exception as e:
                    print(e)

            for i in range(ttest_score.shape[0]):
                for j in range(ttest_score.shape[1]):
                    well_value = []
                    for key, value in plate.replicat.items():
                        neg_median = _search_neg_data(value, neg_pos, data)
                        try:
                            if data == "median":
                                if SECData:
                                    well_value.append(value.SECDataMedian[i][j] - neg_median)
                                else:
                                    well_value.append(value.DataMedian[i][j] - neg_median)
                            elif data == "mean":
                                if SECData:
                                    well_value.append(value.SECDataMean[i][j] - neg_median)
                                else:
                                    well_value.append(value.DataMean[i][j] - neg_median)
                            else:
                                raise AttributeError('\033[0;31m[ERROR]\033[0m  Data type must be mean or median')
                        except Exception:
                            raise Exception("\033[0;31m[ERROR]\033[0m  Your desired datatype are not available")
                    ttest_score[i][j] = np.nanmean(well_value) / (
                        np.nanstd(well_value) / np.sqrt(len(plate.replicat)))


            # # replace NaN with 0
            ttest_score = np.nan_to_num(ttest_score)

            if verbose:
                print("Paired t-test :")
                print("Systematic Error Corrected Data : ", SECData)
                print("Data type : ", data)
                print("t-test score :")
                print(ttest_score)
                print("")
            return ttest_score
        else:
            raise TypeError
    except Exception as e:
        print(e)