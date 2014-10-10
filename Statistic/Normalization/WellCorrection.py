__author__ = 'Arnaud KOPP'
import numpy as np


def WellCorrection(Array):
    '''
    Well Correction technique introduce by Makarenkov et al. 2007 Statistical Analysis of Systematic Errors in HTS.
    Not so good so implementation will come later
    :param array:
    :return:
    '''
    try:
        if isinstance(Array, np.ndarray):
            return 0
        else:
            raise TypeError
    except Exception as e:
        print(e)