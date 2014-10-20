__author__ = 'Arnaud KOPP'
'''
Function that performed paired/unpaired T-Test
'''
import ScreenPlateReplicatPS
import numpy as np
import scipy.special
from Statistic.Stat import mad


def t_test_score(plate, cNeg, unpaired=False):
    '''
    Performed t-test on plate object
    unpaired is for plate with replicat without great variance between them
    paired is for plate with replicat with great variance between them
    :param Plate:
    :return:
    '''
    try:
        if isinstance(plate, ScreenPlateReplicatPS.Plate):
            if len(plate) > 1:
                return 0
            else:
                print("T-Test need at least two replicat")
                raise ValueError
        else:
            raise TypeError
    except Exception as e:
        print(e)


def _UnpairedTTestScore(plate):
    '''
    performed unpaired t-test score
    :return:
    '''
    try:
        if isinstance(plate, ScreenPlateReplicatPS.Plate):
            return 0
        else:
            raise TypeError
    except Exception as e:
        print(e)


def _PairedTTestScore(plate, data='median', verbose=False):
    '''
    performed paired t-test score
    :return:
    '''
    try:
        if isinstance(plate, ScreenPlateReplicatPS.Plate):
            ttest = np.zeros(plate.PlateSetup.platesetup.shape)
            try:
                if data == 'median':
                    for i in range(ttest.shape[0]):
                        for j in range(ttest.shape[1]):
                            well_value = []
                            for key, value in plate.replicat.items():
                                well_value.append(value.SpatNormDataMedian[i][j])
                            ttest[i][j] = np.mean(well_value) / (np.std(well_value) / np.sqrt(len(plate.replicat)))
                else:
                    for i in range(ttest.shape[0]):
                        for j in range(ttest.shape[1]):
                            well_value = []
                            for key, value in plate.replicat.items():
                                well_value.append(value.SpatNormDataMedian[i][j])
                            ttest[i][j] = np.mean(well_value) / (np.std(well_value) / np.sqrt(len(plate.replicat)))
            except Exception as e:
                print(e)
            return ttest
        else:
            raise TypeError
    except Exception as e:
        print(e)