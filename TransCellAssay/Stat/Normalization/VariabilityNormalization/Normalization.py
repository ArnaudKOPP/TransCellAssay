# coding=utf-8
"""
Controls based normalization : Percent Of Control and Normalized percent of inhibition
Non controls based normalization : Z-score and robust Z-score

Use this with caution, if you want to keep some event with 0 in value, don't normalize
"""

import numpy as np
import pandas as pd
from TransCellAssay.Stat.stat_misc import mad


__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


def variability_normalization(data, feature, method=False, log2_transf=True, neg_control=None, pos_control=None):
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
                data.loc[:, feature] = (data.loc[:, feature] - np.nanmean(data[feature])) / np.nanstd(data[feature])
            # apply a Robust z-score transformation on data
            elif method == 'RobustZscore':
                data.loc[:, feature] = (data.loc[:, feature] - np.nanmedian(data[feature])) / mad(data[feature])
            # apply a percent of control transformation on data
            elif method == 'PercentOfControl':
                if neg_control is None:
                    if pos_control is None:
                        raise AttributeError("\033[0;31m[ERROR]\033[0m Need Negative or Positive control")
                    else:
                        # Using positive control
                        pos_data = _get_data_by_wells(data, feature=feature, wells=neg_control)
                        data.loc[:, feature] = ((data[feature]) / (np.mean(pos_data))) * 100
                else:
                    # Using negative control
                    neg_data = _get_data_by_wells(data, feature=feature, wells=neg_control)
                    data.loc[:, feature] = ((data[feature]) / (np.mean(neg_data))) * 100
            # apply a normalized percent inhibition transformation on data
            elif method == 'NormalizedPercentInhibition':
                if neg_control is None:
                    if pos_control is None:
                        raise AttributeError("\033[0;31m[ERROR]\033[0m Need Negative and Positive control")
                    raise AttributeError("\033[0;31m[ERROR]\033[0m Need Negative Control")
                neg_data = _get_data_by_wells(data, feature=feature, wells=neg_control)
                pos_data = _get_data_by_wells(data, feature=feature, wells=pos_control)
                data.loc[:, feature] = ((np.mean(pos_data) - data[feature]) / (
                    np.mean(pos_data) - np.mean(neg_data))) * 100
            else:
                print("\033[0;33m[WARNING]\033[0m  No method selected for Variability Normalization, choose : Zscore, "
                      "RobustZscore, PercentOfControl, NormalizedPercentInhibition")
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
            data.append(dataframe[feature][dataframe['Well'] == i])
        return data
    except Exception as e:
        print(e)