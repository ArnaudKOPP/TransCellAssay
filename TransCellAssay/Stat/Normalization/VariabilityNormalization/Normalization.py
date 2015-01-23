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
from TransCellAssay.Utils.Stat import mad


__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


def plate_feature_scaling(plate, feature, mean_scaling=False):
    """
    Feature Scaling to [0,1] or [0, mean of max] if mean_scaling is True
    :param plate: Plate object
    :param feature: Which feature to scale
    :param mean_scaling: if True, the max is the mean of max accross all replicat (instead of 1)
    """
    try:
        if isinstance(plate, TCA.Plate):
            min_lst = []
            max_lst = []

            # search min and max accross all replicat
            for key, value in plate.replicat.items():
                min_lst.append(np.min(value.rawdata.df[feature]))
                max_lst.append(np.max(value.rawdata.df[feature]))

            # apply feature scaling accross all replicat
            for key, value in plate.replicat.items():
                value.rawdata.df = _df_scaling(value.rawdata.df, min_lst, max_lst, feature, mean_scaling)
                value.isNormalized = True

            plate.isNormalized = True
        else:
            raise TypeError('Take a plate object in input')
    except Exception as e:
        print("\033[0;31m[ERROR]\033[0m", e)


def _df_scaling(df, min_val, max_val, feature, mean=False):
        df.loc[:, feature] = (df.loc[:, feature] - min(min_val)) / (max(max_val) - min(min_val))
        if mean:
            df.loc[:, feature] *= (sum(max_val) / len(max_val))
        return df


def rawdata_variability_normalization(obj, feature, method=None, log2_transf=True, neg_control=None, pos_control=None):
    """
    Take a dataframe from replicat object and apply desired strategy of variability normalization
    :param obj: pd.dataframe to normalize
    :param feature: on which feature to normalize
    :param method: which method to apply
    :param log2_transf: apply log2 transformation
    :param neg_control: list of well for negative control A1 A2 ...
    :param pos_control: list of well for positive control A1 A2 ...
    :return: normalized data
    """
    try:
        if isinstance(obj, TCA.Plate):
            for key, value in obj.replicat.items():
                value.rawdata.df = _df_norm(value.rawdata.df, feature, method, log2_transf, neg_control, pos_control)
        elif isinstance(obj, TCA.Replicat):
            obj.rawdata.df = _df_norm(obj.rawdata.df, feature, method, log2_transf, neg_control, pos_control)
        elif isinstance(obj, TCA.RawData):
            obj.df = _df_norm(obj.df, feature, method, log2_transf, neg_control, pos_control)
            return obj
        else:
            raise TypeError("Don't take this object, only plate, replica or raw data")
    except Exception as e:
        print("\033[0;31m[ERROR]\033[0m", e)


def _df_norm(df, feature, method=None, log2_transf=True, neg_control=None, pos_control=None):
    if log2_transf:
        df = _log2_transformation(df, feature)
    if method == 'Zscore':
        df = _zscore_(df, feature)
    elif method == 'RobustZscore':
        df = _robustzscore(df, feature)
    elif method == 'PercentOfSample':
        df = _percentofsample(df, feature)
    elif method == 'RobustPercentOfSample':
        df = _robustpercentofsample(df, feature)
    elif method == 'PercentOfControl':
        df = _percentofcontrol(df, feature, neg_control, pos_control)
    elif method == 'NormalizedPercentInhibition':
        df = _normalizedpercentinhibition(df, feature, neg_control, pos_control)
    else:
        print("\033[0;33m[WARNING]\033[0m  No method selected for Variability Normalization, choose :\n-Zscore "
              "\n-RobustZscore \n-PercentOfControl \n-PercentOfSample \n-RobustPercentOfSample \n"
              "-NormalizedPercentInhibition")
        return df
        # return transformed data
    return df


def _log2_transformation(df, feature):
    df.loc[:] = df[df[feature] > 0]
    df.loc[:, feature] = np.log2(df[feature])
    return df


def _zscore_(df, feature):
    df.loc[:, feature] = (df.loc[:, feature] - np.mean(df[feature])) / np.std(df[feature])
    return df


def _robustzscore(df, feature):
    df.loc[:, feature] = (df.loc[:, feature] - np.median(df[feature])) / mad(df[feature])
    return df


def _percentofsample(df, feature):
    df.loc[:, feature] = (df.loc[:, feature] / np.mean(df[feature])) * 100
    return df


def _robustpercentofsample(df, feature):
    df.loc[:, feature] = (df.loc[:, feature] / np.median(df[feature])) * 100
    return df


def _percentofcontrol(df, feature, neg=None, pos=None):
    if neg is None:
        if pos is None:
            raise AttributeError("\033[0;31m[ERROR]\033[0m Need Negative or Positive control")
        else:
            # Using positive control
            pos_data = _get_data_by_wells(df, feature=feature, wells=neg)
            df.loc[:, feature] = (df.loc[:, feature] / np.mean(pos_data)) * 100
    else:
        # Using negative control
        neg_data = _get_data_by_wells(df, feature=feature, wells=neg)
        df.loc[:, feature] = (df.loc[:, feature] / np.mean(neg_data)) * 100
    return df


def _normalizedpercentinhibition(df, feature, neg=None, pos=None):
    if neg is None:
        if pos is None:
            raise AttributeError("\033[0;31m[ERROR]\033[0m Need Negative and Positive control")
        raise AttributeError("\033[0;31m[ERROR]\033[0m Need Negative Control")
    neg_data = _get_data_by_wells(df, feature=feature, wells=neg)
    pos_data = _get_data_by_wells(df, feature=feature, wells=pos)
    df.loc[:, feature] = ((np.mean(pos_data) - df[feature]) / (np.mean(pos_data) - np.mean(neg_data))) * 100
    return df


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
        print("\033[0;31m[ERROR]\033[0m", e)