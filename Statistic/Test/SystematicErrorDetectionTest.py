__author__ = 'Arnaud KOPP'

import TCA

def SystematicErrorDetectionTest(Plate):
    '''
    Search for systematic error in plate
    :param Plate:
    :return: nothing norm the value
    '''
    try:
        if isinstance(Plate, TCA.Plate):
            return 0
        else:
            raise TypeError
    except Exception as e:
        print(e)