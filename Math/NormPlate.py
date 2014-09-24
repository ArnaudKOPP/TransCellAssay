__author__ = 'Arnaud KOPP'

import numpy as np
import TCA

def normalizeEdgeEffect():
    '''
    Apply a median polish for remove edge effect
    :return:
    '''
    return 0


def normalizeBetweenReplicat(Plate):
    '''
    Apply a norm between replicat
    :return:
    '''
    if (Plate.replicat.getNBreplicat()) < 2:
        print('Can\'t apply this normalization because under two replicats, need at least two replicats ')
    else:
        print('Normalization not yet implememted')