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


def compute_plate_analyzis(plate, feature, neg, pos, threshold=50):
    """
    Compute all score/carac implemented before, for plate
    :param plate: Plate object
    :param feature: which feature to analyze
    :param neg: negative control reference
    :param threshold: threshold for defining % of positive cell in negative ref
    :param direction: which direction effect of target hit, Up effect or down effect
    :return: return a result object
    """
    try:
        if isinstance(plate, TransCellAssay.Plate):
            platemap = plate.get_platemap()
            size = platemap.get_platemape_shape()
            result = TransCellAssay.Result(size=(size[0] * size[1]))
            x = platemap.get_map_as_dict()
            result.init_gene_well(x)
            try:
                meanCount, sdvalue = TransCellAssay.get_cell_count(plate)
                PercentCell, sdPercentCell = TransCellAssay.get_percent_positive_cell(plate, feature, neg, threshold)
                mean, median, std, stdm = TransCellAssay.get_variability(plate, feature)
                toxicity, viability = TransCellAssay.get_toxicity_viability(plate=plate, cell_count=meanCount, neg=neg,
                                                                            pos=pos)

                # Add all result into Result Data Frame
                result.add_data(meanCount, 'CellsCount', by='Pos')
                result.add_data(sdvalue, 'SDCellsCunt', by='Pos')
                result.add_data(PercentCell, 'PositiveCells', by='Pos')
                result.add_data(sdPercentCell, 'SDPositiveCells', by='Pos')
                result.add_data(mean, 'Mean', by='Pos')
                result.add_data(median, 'Median', by='Pos')
                result.add_data(std, 'Std', by='Pos')
                result.add_data(stdm, 'Stdm', by='Pos')
                result.add_data(toxicity, 'Toxicity', by='Pos')
                result.add_data(viability, 'Viability', by='Pos')

                return result
            except Exception as e:
                print(e)
        else:
            raise TypeError("\033[0;31m[ERROR]\033[0m Input Plate Object")
    except Exception as e:
        print("\033[0;31m[ERROR]\033[0m", e)