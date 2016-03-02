# coding=utf-8
"""
Usefull function

1536 well is only supported in 'simple' format from A to AF for row and 1 to 48 for columns  (begin by 0 in python)
"""

import re
import numpy as np
import pandas as pd

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2016 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "GPLv3"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"

regexWellConv = re.compile(pattern="([a-zA-Z]+)([0-9]+)")

lettereq = {'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7, 'I':8, 'J':9, 'K':10, 'L':11, 'M':12,
            'N':13, 'O':14, 'P':15, 'Q':16, 'R':17, 'S':18, 'T':19, 'U':20, 'V':21, 'W':22, 'X':23, 'Y':24,
            'Z':25, 'AA':26, 'AB':27, 'AC':28, 'AD':29, 'AE':30, 'AF':31}
numbeq = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L',
            12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T', 20: 'U', 21: 'V', 22: 'W',
            23: 'X', 24: 'Y', 25: 'Z', 26: 'AA', 27: 'AB', 28: 'AC', 29: 'AD', 30: 'AE', 31: 'AF'}

def get_opposite_well_format(to_conv, bignum=False):
    """
    Change Well Format
    A1 to (0,0) or (1,3) to B4
    :param to_conv: tuple or str
    :param bignum: 1536 well plate format
    :return: opposite well format
    """
    try:
        if bignum:
            if isinstance(to_conv, tuple):
                new_form = "{0}{1}".format(str(numbeq[to_conv[0]]), to_conv[1] + 1)
                return new_form
            elif isinstance(to_conv, str):
                m = regexWellConv.match(to_conv)
                new_form = lettereq[m.group(1)], int(m.group(2)) - 1
                return new_form
            else:
                raise ValueError
        else:
            if isinstance(to_conv, tuple):
                new_form = "{0}{1}".format(str(numbeq[to_conv[0]]), to_conv[1] + 1)
                return new_form
            elif isinstance(to_conv, str):
                new_form = lettereq[to_conv[0]], int(to_conv[1:]) - 1
                return new_form
            else:
                raise ValueError
    except Exception as e:
        print(e)


def get_masked_array(data_arr, plate_array, to_keep):
    """
    Return an array with data to keep and set to 0 other
    :param data_arr: array data with value
    :param plate_array: numpy array from PlateMap
    :param to_keep: gene name to keep
    :return: numpy array with data keeped and 0 to other
    """
    data = data_arr.copy()
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            if not plate_array[i][j] == to_keep:
                data[i][j] = 0
    return data


def dict_to_df(input_dict):
    name = np.array(list(input_dict))
    name = name.flatten().reshape(len(name), 1)
    ar = np.concatenate(list(input_dict.values()))
    ar = np.append(ar, name, axis=1)
    return pd.DataFrame(ar)
