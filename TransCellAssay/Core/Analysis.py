"""
Compute basics score for plate and store result into a Result object
"""

import TransCellAssay

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


def computePlateAnalyzis(Plate, feature, neg, pos, threshold=50):
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
        if isinstance(Plate, TransCellAssay.Plate):
            platemap = Plate.getPlateMap()
            size = platemap.getSize()
            result = TransCellAssay.Result(size=(size[0] * size[1]))
            x = platemap.getMapAsDict()
            result.initGeneWell(x)
            try:
                meanCount, sdvalue = TransCellAssay.getMeanSDCellCount(Plate)
                PercentCell, sdPercentCell = TransCellAssay.getPercentPosCell(Plate, feature, neg, threshold)
                mean, median, std, stdm = TransCellAssay.getVariability(Plate, feature)
                toxicity, viability = TransCellAssay.get_Toxicity_Viability(plate=Plate, cell_count=meanCount, neg=neg,
                                                                            pos=pos)

                # Add all result into Result Data Frame
                result.addDataDict(meanCount, 'CellsCount', by='Pos')
                result.addDataDict(sdvalue, 'SDCellsCunt', by='Pos')
                result.addDataDict(PercentCell, 'PositiveCells', by='Pos')
                result.addDataDict(sdPercentCell, 'SDPositiveCells', by='Pos')
                result.addDataDict(mean, 'mean', by='Pos')
                result.addDataDict(median, 'median', by='Pos')
                result.addDataDict(std, 'std', by='Pos')
                result.addDataDict(stdm, 'stdm', by='Pos')
                result.addDataDict(toxicity, 'Toxicity', by='Pos')
                result.addDataDict(viability, 'Viability', by='Pos')

                return result
            except Exception as e:
                print(e)
        else:
            raise TypeError("\033[0;31m[ERROR]\033[0m Input Plate Object")
    except Exception as e:
        print("\033[0;31m[ERROR]\033[0m", e)