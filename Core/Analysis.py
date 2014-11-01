"""
Score defined method for compute some score on data
"""

import Statistic.Score
import Core

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


def computePlateAnalyzis(Plate, feature, neg, threshold=50, direction='Up'):
    """
    Compute all score/carac implemented before, for plate
    :param Plate: Plate object
    :param feature: which feature to analyze
    :param neg: negative control reference
    :param threshold: threshold for defining % of positive cell in negative ref
    :param direction: which direction effect of target hit, Up effect or down effect
    :return: return a result object
    """
    try:
        if isinstance(Plate, Core.Plate):
            platesetup = Plate.getPlateSetup()
            size = platesetup.getSize()
            result = Core.Result(size=(size[0] * size[1]))
            x = platesetup.getPSasDict()
            result.initGeneWell(x)
            try:
                meanCount, sdvalue = Statistic.Score.getMeanSDCellCount(Plate)
                result.addDataDict(meanCount, 'CellsCount', by='Pos')
                result.addDataDict(sdvalue, 'SDCellsCunt', by='Pos')
                PercentCell, sdPercentCell = Statistic.Score.getPercentPosCell(Plate, feature, neg, threshold,
                                                                               direction)
                result.addDataDict(PercentCell, 'PositiveCells', by='Pos')
                result.addDataDict(sdPercentCell, 'SDPositiveCells', by='Pos')
                return result
            except Exception as e:
                print(e)
        else:
            print("\033[0;31m[ERROR]\033[0m")
            raise TypeError
    except Exception as e:
        print("\033[0;31m[ERROR]\033[0m")
        print(e)