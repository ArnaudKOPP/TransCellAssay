# coding=utf-8
"""
Controls based normalization : Percent Of Control and Normalized percent of inhibition
Non controls based normalization : Percent of Sample, Robust Percent of Sample, Z-score and robust Z-score

Use this with caution, if you want to keep some event with 0 in value, don't normalize

Add Feature Scaling normalization :
http://en.wikipedia.org/wiki/Feature_scaling
"""

import numpy as np
import pandas as pd
import TransCellAssay as TCA
from TransCellAssay.Utils.stat_misc import mad


__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


def feature_scaling(plate, feature, mean_scaling=False):
    """
    Feature Scaling to [0,1] or [0, mean of max] if mean_scaling is True
    :param plate: Plate object
    :param feature: Which feature to scale
    :param mean_scaling: if True, the max is the mean of max accross all replicat (instead of 1)
    """
    if isinstance(plate, TCA.Plate):
        min_lst = []
        max_lst = []

        # search min and max accross all replicat
        for key, value in plate.replicat.items():
            min_lst.append(np.min(value.RawData[feature]))
            max_lst.append(np.max(value.RawData[feature]))

        # apply feature scaling accross all replicat
        for key, value in plate.replicat.items():
            value.RawData.loc[:, feature] = (
                (value.RawData.loc[:, feature] - min(min_lst)) / (max(max_lst) - min(min_lst)))
            if mean_scaling:
                value.RawData.loc[:, feature] *= (sum(max_lst) / len(max_lst))
            value.isNormalized = True

        plate.isNormalized = True
    else:
        raise TypeError


def variability_normalization(data, feature, method=None, log2_transf=True, neg_control=None, pos_control=None):
    """
    Take a dataframe from replicat object and apply desired strategy of variability normalization
    :param data: pd.dataframe to normalize
    :param feature: on which feature to normalize
    :param method: which method to apply
    :param log2_transf: apply log2 transformation
    :param neg_control: list of well for negative control
    :param pos_control: list of well for positive control
    :return: normalized data
    """
    try:
        if isinstance(data, pd.DataFrame):
            # apply log2 transformation on data
            if log2_transf:
                data.loc[:] = data[data[feature] > 0]
                data.loc[:, feature] = np.log2(data[feature])
            # apply a z-score transformation on data
            if method == 'Zscore':
                data.loc[:, feature] = (data.loc[:, feature] - np.mean(data[feature])) / np.std(data[feature])
            # apply a Robust z-score transformation on data
            elif method == 'RobustZscore':
                data.loc[:, feature] = (data.loc[:, feature] - np.median(data[feature])) / mad(data[feature])
            # apply a percent of control transformation on data
            elif method == 'PercentOfSample':
                data.loc[:, feature] = (data.loc[:, feature] / np.mean(data[feature])) * 100
            elif method == 'RobustPercentOfSample':
                data.loc[:, feature] = (data.loc[:, feature] / np.median(data[feature])) * 100
            elif method == 'PercentOfControl':
                if neg_control is None:
                    if pos_control is None:
                        raise AttributeError("\033[0;31m[ERROR]\033[0m Need Negative or Positive control")
                    else:
                        # Using positive control
                        pos_data = _get_data_by_wells(data, feature=feature, wells=neg_control)
                        data.loc[:, feature] = (data.loc[:, feature] / np.mean(pos_data)) * 100
                else:
                    # Using negative control
                    neg_data = _get_data_by_wells(data, feature=feature, wells=neg_control)
                    data.loc[:, feature] = (data.loc[:, feature] / np.mean(neg_data)) * 100
            # apply a normalized percent inhibition transformation on data
            elif method == 'NormalizedPercentInhibition':
                if neg_control is None:
                    if pos_control is None:
                        raise AttributeError("\033[0;31m[ERROR]\033[0m Need Negative and Positive control")
                    raise AttributeError("\033[0;31m[ERROR]\033[0m Need Negative Control")
                neg_data = _get_data_by_wells(data, feature=feature, wells=neg_control)
                pos_data = _get_data_by_wells(data, feature=feature, wells=pos_control)
                data.loc[:, feature] = ((np.mean(pos_data) - data[feature]) /
                                        (np.mean(pos_data) - np.mean(neg_data))) * 100
            else:
                print("\033[0;33m[WARNING]\033[0m  No method selected for Variability Normalization, choose :\n-Zscore "
                      "\n-RobustZscore \n-PercentOfControl \n-PercentOfSample \n-RobustPercentOfSample \n"
                      "-NormalizedPercentInhibition")
                return data

            # return transformed data
            return data
        else:
            raise TypeError
    except Exception as e:
        print(e)


def _get_data_by_wells(dataframe, feature, wells):
    """
    get all data for specified wellS
    :param wells: list of wells
    :return: return dataframe with data specified wells
    """
    try:
        data = pd.DataFrame()
        for i in wells:
            if data.empty:
                data = dataframe[feature][dataframe['Well'] == i]
            data = data.append(dataframe[feature][dataframe['Well'] == i])
        return data
    except Exception as e:
        print(e)