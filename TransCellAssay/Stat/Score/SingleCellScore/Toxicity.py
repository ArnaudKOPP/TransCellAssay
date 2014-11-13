"""
Viability and toxicity method
"""

import TransCellAssay as TCA
import numpy as np

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


def get_Toxicity_Viability(plate, cell_count, neg, pos):
    """
    Compute toxicity and viability
    :param plate:
    :param cell_count:
    :return: toxicit and viablity score in dict
    """
    if not isinstance(plate, TCA.Core.Plate):
        raise TypeError("\033[0;31m[ERROR]\033[0m  Take a Plate object in input")
    if not isinstance(cell_count, dict):
        raise TypeError("\033[0;31m[ERROR]\033[0m  Take a dict in input for cell count")
    else:
        try:
            neg_well = plate.PlateMap.getGeneWell(neg)
            pos_well = plate.PlateMap.getGeneWell(pos)

            toxicityIdx = _getToxicityIdx(cell_count)
            viability = _getViability(cell_count, neg_well, pos_well)

            return toxicityIdx, viability
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)


def _getToxicityIdx(cellcount):
    """
    determine a toxicity index
    :return: tox dict
    """
    try:
        max_cell = max(cellcount.values())
        min_cell = min(cellcount.values())

        txIdx = {}

        for key, item in cellcount.items():
            txIdx[key] = (max_cell - item) / (max_cell - min_cell)

        return txIdx
    except Exception as e:
        print(e)


def _getViability(cellcount, neg_well, pos_well):
    """
    get Viability, z-score like
    :return:
    """
    try:
        neg_val = [cellcount[x] for x in neg_well]
        pos_val = [cellcount[x] for x in pos_well]

        viability = {}
        for key, item in cellcount.items():
            viability[key] = (item - np.mean(pos_val) - 3 * np.std(pos_val)) / np.abs(
                np.mean(neg_val) - np.mean(pos_val))

        return viability
    except Exception as e:
        print(e)