__author__ = 'Arnaud KOPP'
"""
Controls based normalization : Percent Of Control and Normalized percent of inhibition
Non controls based normalization : Z-score and robust Z-score
"""
import numpy as np
import pandas as pd
from Statistic.Stat import mad


def VariabilityNormalization(data, feature, method=False, log2_transformation=True, Cneg=None, Cpos=None):
    '''
    Take a dataframe from replicat object
    :param data: pd.dataframe to normalize
    :param method: which method to apply
    :param log2_transformation: apply log2 transformation
    :param Cneg: list of well for negative control
    :param Cpos: list of well for positive control
    :return: normalized data
    '''
    try:
        if isinstance(data, pd.DataFrame):
            # apply log2 transformation on data
            if log2_transformation:
                data[feature] = np.log2(data[feature])

            if not method:
                print("No method selected for Variability Normalization")
                return data

            # apply a z-score transformation on data
            if method == 'Zscore':
                data[feature] = (data[feature] - np.mean(data[feature])) / np.std(data[feature])

            # apply a Robust z-score transformation on data
            if method == 'RobustZscore':
                data[feature] = (data[feature] - np.median(data[feature])) / mad(data[feature])

            # apply a percent of control transformation on data
            if method == 'PercentOfControl':
                if Cneg is None:
                    if Cpos is None:
                        print("Need Negative or Positive control")
                        raise AttributeError
                    else:
                        # Using positive control
                        CposData = getDataByWells(data, feature=feature, wells=Cneg)
                        data = ((data[feature]) / (np.mean(CposData))) * 100
                else:
                    # Using negative control
                    CnegData = getDataByWells(data, feature=feature, wells=Cneg)
                    data = ((data[feature]) / (np.mean(CnegData))) * 100

            # apply a normalized percent inhibition transformation on data
            if method == 'NormalizedPercentInhibition':
                if Cneg is None:
                    if Cpos is None:
                        print("Need Negative and Positive control")
                        raise AttributeError
                    print("Need Negative Control")
                    raise AttributeError
                CnegData = getDataByWells(data, feature=feature, wells=Cneg)
                CposData = getDataByWells(data, feature=feature, wells=Cpos)
                data = ((np.mean(CposData) - data[feature]) / (np.mean(CposData) - np.mean(CnegData))) * 100

            # return transformed data
            return data
        else:
            raise TypeError
    except Exception as e:
        print(e)


def getDataByWells(dataframe, feature, wells):
    '''
    get all data for specified wellS
    :param wells: list of wells
    :return: return dataframe with data specified wells
    '''
    try:
        data = pd.DataFrame()
        for i in wells:
            if data.empty:
                data = dataframe[feature][dataframe['Well'] == i]
            data.append(dataframe[feature][dataframe['Well'] == i])
        return data
    except Exception as e:
        print(e)
        print('Error in exporting data for wells')