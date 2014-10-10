__author__ = 'Arnaud KOPP'

import numpy as np


def PartialMeanPolish(Array):
    '''
    Implementation of Partial Mean Polish , published in 'Two effective methods for correcting experimental
    HTS data ' Dragiev, et al 2012
    :param: Array: numpy array represent plate
    :param Array:
    :return:
    '''
    try:
        if isinstance(Array, np.ndarray):
            return 0
        else:
            raise TypeError
    except Exception as e:
        print(e)