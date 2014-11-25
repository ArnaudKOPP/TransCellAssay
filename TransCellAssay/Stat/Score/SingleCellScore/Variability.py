"""
Variability method
"""

import numpy as np
import TransCellAssay as TCA

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


def get_variability(plate, feature):
    """

    :param plate:
    :param feature:
    :param verbose:
    :return:
    """
    if not isinstance(plate, TCA.Core.Plate):
        raise TypeError("\033[0;31m[ERROR]\033[0m  Take a Plate object in input")
    else:
        try:
            mean = {}
            median = {}

            for key, item in plate.replicat.items():
                datagp = item.RawData.groupby('Well')

                # get all well from data
                well_list = item.RawData.Well.unique()
                # iterate on well
                for well in well_list:
                    mean.setdefault(well, []).append(np.mean(datagp.get_group(well)[feature]))
                    median.setdefault(well, []).append(np.median(datagp.get_group(well)[feature]))
            std = [(i, np.std(v)) for i, v in mean.items()]
            stdm = [(i, np.std(v)) for i, v in median.items()]
            std = dict(std)
            stdm = dict(stdm)

            mean = [(i, sum(v) / len(v)) for i, v in mean.items()]
            median = [(i, sum(v) / len(v)) for i, v in median.items()]
            mean = dict(mean)
            median = dict(median)

            return mean, median, std, stdm
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)