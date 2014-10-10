__author__ = 'Arnaud KOPP'

import numpy as np


def MatrixErrorAmendment(Array):
    '''
    Implementation of Matrix Error Amendment , published in 'Two effective methods for correcting experimental
    HTS data ' Dragiev, et al 2012
    :param: Array: numpy array represent plate
    :return:
    '''
    try:
        if isinstance(Array, np.ndarray):
            return 0
        else:
            raise TypeError
    except Exception as e:
        print(e)