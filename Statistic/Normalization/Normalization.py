__author__ = 'Arnaud KOPP'

import numpy as np
import pandas as pd
from Statistic.Stat import mad


def VariabilityNormalization(data, feature, method, log2_transformation=True):
    '''
    Take a dataframe from replicat object
    :param plate: pd.dataframe
    :return:
    '''
    try:
        if isinstance(data, pd.DataFrame):
            # apply log2 transformation on data
            if log2_transformation:
                data[feature] = np.log2(data[feature])

            # apply a z-score transformation on data
            if method == 'Zscore':
                data[feature] = (data[feature] - np.mean(data[feature])) / np.std(data[feature])
            if method == 'RobustZscore':
                data[feature] = (data[feature] - np.mean(data[feature])) / mad(data[feature])
            if method == 'PercentOfControl' or 'PC':
                return 0
            if method == 'NormalizedPercentInhibition' or 'NPI':
                return 0
        else:
            raise TypeError
    except Exception as e:
        print(e)