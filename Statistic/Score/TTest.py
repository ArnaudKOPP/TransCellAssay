__author__ = 'Arnaud KOPP'
'''
Function that performed paired/unpaired T-Test
'''
import ScreenPlateReplicatPS
import numpy as np
import scipy.special
from Statistic.Stat import mad


def t_test_score(plate, cNeg, data='median', variance='unequal', unpaired=False, verbose=False):
    '''
    Performed t-test on plate object
    unpaired is for plate with replicat without great variance between them
    paired is for plate with replicat with great variance between them
    :param Plate:
    :return:
    '''
    try:
        if isinstance(plate, ScreenPlateReplicatPS.Plate):
            # if no neg was provided raise AttributeError
            if cNeg is None:
                raise AttributeError('Must provided negative control')
            if len(plate) > 1:
                return 0
            else:
                print("T-Test need at least two replicat")
                raise ValueError
        else:
            raise TypeError
    except Exception as e:
        print(e)


def _UnpairedTTestScore(plate, cNeg, data='median', variance='unequal', verbose=False):
    '''
    performed unpaired t-test score

    variance :
        - unequal : Welch t-test
        - equal : two sample t-test
    :return:
    '''
    try:
        if cNeg is None:
            raise AttributeError('Must provided negative control')
        if isinstance(plate, ScreenPlateReplicatPS.Plate):
            ttest_score = np.zeros(plate.PlateSetup.platesetup.shape)
            nb_rep = len(plate.replicat)
            rep_value = []
            neg_value = []
            neg_pos = plate.PlateSetup.getGenePos(cNeg)

            # search neg control value
            for i in range(ttest_score.shape[0]):
                for j in range(ttest_score.shape[1]):
                    for key, value in plate.replicat.items():
                        well_value = 0
                        try:
                            if data == "median":
                                well_value = value.SpatNormDataMedian[i][j]
                            elif data == "mean":
                                well_value = value.SpatNormDataMean[i][j]
                            else:
                                raise AttributeError('Data type must be mean or median')
                        except Exception as e:
                            print("Launch SystematicErrorCorrection before")
                            print(e)
                        # check if neg value
                        for neg_i in neg_pos:
                            if neg_i[0] == i and neg_i[1] == j:
                                neg_value.append(well_value)
            nb_neg_wells = len(neg_value)
            mean_neg = np.mean(neg_value)
            var_neg = np.var(neg_value)

            # search rep value for ith well
            for i in range(ttest_score.shape[0]):
                for j in range(ttest_score.shape[1]):
                    well_value = 0
                    for key, value in plate.replicat.items():
                        try:
                            if data == "median":
                                well_value = value.SpatNormDataMedian[i][j]
                            elif data == "mean":
                                well_value = value.SpatNormDataMean[i][j]
                            else:
                                raise AttributeError('Data type must be mean or median')
                        except Exception as e:
                            print("Launch SystematicErrorCorrection before")
                            print(e)
                        rep_value.append(well_value)
                    mean_rep = np.mean(rep_value)
                    var_rep = np.var(rep_value)

                    # # performed unpaired t-test
                    if variance == 'unequal':
                        ttest_score[i][j] = (mean_rep - mean_neg) / np.sqrt(
                            (var_rep / nb_rep) + (var_neg / nb_neg_wells))
                    elif variance == 'equal':
                        ttest_score[i][j] = (mean_rep - mean_neg) / np.sqrt((2 / (nb_rep + nb_neg_wells - 2)) * (
                            (nb_rep - 1) * var_rep + (nb_neg_wells - 1) * var_neg) * (
                                                                                (1 / nb_rep) * (1 / nb_neg_wells)))
                    else:
                        raise AttributeError('variance attribut must be unequal or equal.')
            if verbose:
                print("Unpaired t-test :")
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


def _PairedTTestScore(plate, cNeg, data='median', verbose=False):
    '''
    performed paired t-test score
    :return:
    '''
    try:
        if cNeg is None:
            raise AttributeError('Must provided negative control')
        if isinstance(plate, ScreenPlateReplicatPS.Plate):
            ttest_score = np.zeros(plate.PlateSetup.platesetup.shape)
            neg_value = []
            neg_pos = plate.PlateSetup.getGenePos(cNeg)
            # search neg control value
            for i in range(ttest_score.shape[0]):
                for j in range(ttest_score.shape[1]):
                    for key, value in plate.replicat.items():
                        well_value = 0
                        try:
                            if data == "median":
                                well_value = value.SpatNormDataMedian[i][j]
                            elif data == "mean":
                                well_value = value.SpatNormDataMean[i][j]
                            else:
                                raise AttributeError('Data type must be mean or median')
                        except Exception as e:
                            print("Launch SystematicErrorCorrection before")
                            print(e)
                        # check if neg value
                        for neg_i in neg_pos:
                            if neg_i[0] == i and neg_i[1] == j:
                                neg_value.append(well_value)
            neg_median = np.median(neg_value)

            try:
                if data == 'median':
                    for i in range(ttest_score.shape[0]):
                        for j in range(ttest_score.shape[1]):
                            well_value = []
                            for key, value in plate.replicat.items():
                                well_value.append(value.SpatNormDataMedian[i][j] - neg_median)
                            ttest_score[i][j] = np.mean(well_value) / (
                            np.std(well_value) / np.sqrt(len(plate.replicat)))
                elif data == 'mean':
                    for i in range(ttest_score.shape[0]):
                        for j in range(ttest_score.shape[1]):
                            well_value = []
                            for key, value in plate.replicat.items():
                                well_value.append(value.SpatNormDataMedian[i][j] - neg_median)
                            ttest_score[i][j] = np.mean(well_value) / (
                            np.std(well_value) / np.sqrt(len(plate.replicat)))
                else:
                    raise AttributeError('Data type must be mean or median')
            except Exception as e:
                print(e)
            if verbose:
                print("Paired t-test :")
                print("Data type : ", data)
                print("t-test score :")
                print(ttest_score)
                print("")
            return ttest_score
        else:
            raise TypeError
    except Exception as e:
        print(e)