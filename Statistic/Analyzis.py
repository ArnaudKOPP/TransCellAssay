__author__ = 'Arnaud KOPP'
"""
Score defined method for compute some score on data
"""

import Statistic.Result
import Statistic.Score as score
import TCA

def computePlateAnalyzis(Plate, feature):
    '''
    Compute all score/carac implemented before, for plate
    :param Plate: Plate object
    :return: return a result object
    '''
    if isinstance(Plate, TCA.Plate):
        platesetup = Plate.getPlateSetup()
        size = platesetup.getSize()
        result = Statistic.Result(size=(size[0] * size[1]))
        x = platesetup.getPSasDict()
        result.initGeneWell(x)
        try:

            data = Plate.getAllData()
            meanCount, sdvalue = score.getMeanSDCellCount(data)
            result.addDict(meanCount, 'CellsCount', by='Pos')
            result.addDict(sdvalue, 'SDCellsCunt', by='Pos')
            return result
        except Exception as e:
            print(e)
    else:
        print("Not TCA.Plate Class object")