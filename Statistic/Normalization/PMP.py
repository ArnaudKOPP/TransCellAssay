__author__ = 'Arnaud KOPP'

import numpy as np
import TCA


def PartialMeanPolish(plate, feature, epsilon=0.01, max_iteration=50):
    '''
    Implementation of Partial Mean Polish , published in 'Two effective methods for correcting experimental
    HTS data ' Dragiev, et al 2012
    :param: plate: TCA.Plate object
    :param: feature: feature to normalize
    :return:
    '''
    try:
        if isinstance(plate, TCA.Plate):
            return 0
        else:
            raise TypeError
    except Exception as e:
        print(e)