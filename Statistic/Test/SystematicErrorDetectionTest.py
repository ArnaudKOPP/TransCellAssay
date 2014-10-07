__author__ = 'Arnaud KOPP'

import TCA
import Statistic.Normalization


def SystematicErrorDetectionTest(Object):
    '''
    Search for systematic error in plate, and try to apply the best strategie
    :param Plate:
    :return:
    '''
    try:
        if isinstance(Object, TCA.Plate):
            print("Plate SEDT")
        # col of numpy array : array[:,x]
        # row of numpy array : array[x,:]
        if isinstance(Object, TCA.Replicat):
            print("Replicat SEDT")
        else:
            raise TypeError
    except Exception as e:
        print(e)