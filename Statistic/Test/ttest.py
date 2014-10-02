__author__ = 'Arnaud KOPP'

import scipy
import numpy

def ttest(a, b):
    '''
    perform a t-test on a dataframe of replicat for testing if they contain systematic error
    :param a:
    :param b:
    :return Row, Col: return row and col p-value t-test
    '''

    Row = numpy.array()
    Col = numpy.array()
    TestArray, RemainingArray = numpy.array()

    x = scipy.stats.ttest_ind(TestArray, RemainingArray)
    return Row, Col