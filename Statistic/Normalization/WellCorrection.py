__author__ = 'Arnaud KOPP'
import numpy as np
import pandas as pd


def WellCorrection(data, feature, zscore_transformation=True, log2_transformation=True):
    '''
    Well Correction technique introduce by Makarenkov et al. 2007 Statistical Analysis of Systematic Errors in HTS.
    Not so good so implementation will come later
    Apparently it's equivalent to zscore ?? so we can apply a z-score norm on single cell data

    Take a Plate Object in input, and apply zscore transformation and or log2 transformation at all data (replicat)
    :param plate: TCA.Plate object
    :return:
    '''
    try:
        if isinstance(data, pd.DataFrame):
            # apply log2 transformation on data
            if log2_transformation:
                data[feature] = np.log2(data[feature])
            # apply a z-score transformation on data
            if zscore_transformation:
                data[feature] = (data[feature] - np.mean(data[feature])) / np.std(data[feature])
        else:
            raise TypeError
    except Exception as e:
        print(e)