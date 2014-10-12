__author__ = 'Arnaud KOPP'
import numpy as np
import TCA


def WellCorrection(plate, feature, ZSCORE_EPSILON=0.000001):
    '''
    Well Correction technique introduce by Makarenkov et al. 2007 Statistical Analysis of Systematic Errors in HTS.
    Not so good so implementation will come later
    Apparently it's equivalent to zscore ?? so we can apply a z-score norm on single cell data
    :param plate: TCA.Plate object
    :return:
    '''
    try:
        if isinstance(plate, TCA.Plate):
            # # iterate on different replicat and apply Zscore normalization
            for key, value in plate.replicat.items():
                mean = np.mean(value.Data[feature])
                std = np.std(value.Data[feature])
                value.Data[feature] = (value.Data[feature] - mean) / std
        else:
            raise TypeError
    except Exception as e:
        print(e)