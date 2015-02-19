# coding=utf-8
"""
Class for writing data of some well into a excel file
Save for defined reference (Genename/well) some stat like mean, median, std, sem
"""

import collections
import pandas as pd
import numpy as np
from scipy import stats
import TransCellAssay as TCA
import logging
log = logging.getLogger(__name__)

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


class ReferenceDataWriter(object):
    """
    Class for writing data of reference from plate into file
    """

    def __init__(self, plate, channels, ref, filepath=None):
        if filepath is None:
            log.warning('File path not provided, default will be used')
            self._writer = pd.ExcelWriter("ReferenceDataWriter.xlsx")
        else:
            self._writer = pd.ExcelWriter(filepath)
            log.info('Writing xlsx :', filepath)
        self._save_reference(plate, ref=ref, channels=channels)

    def _save_reference(self, plate, channels, ref):
        plt_list = []

        # # Grab all plate object
        if not isinstance(plate, TCA.Plate):
            raise ValueError('Take Plate in input')

        plt_col_idx = [str(x)+str(y)+str(z) for x in [t for t in plate.replica.keys()] for y in ref for z in ['Mean', 'Std', 'Sem']]

        for channel in channels:
            if channel not in plate.platemap.get_channel_list():
                raise ValueError('Wrong Channel')
            log.debug('Computation for channel :', channel)
            plt_name_index = []
            df = pd.DataFrame()
            i = 1
            for plate in plt_list:
                df = df.append(pd.DataFrame(self._get_plate_reference_data(plate, refs=ref, chan=channel)))
                plt_name_index.append(plate.name+str(i))
                i += 1
            df = df.set_index([plt_name_index])
            df.columns = plt_col_idx
            if self._writer is not None:
                df.to_excel(self._writer, sheet_name=channel)

    def _get_plate_reference_data(self, plate, refs, chan):
        well_ref = collections.OrderedDict()
        # # search all position for desired reference
        for ref in refs:
            try:
                well_ref[ref] = plate.platemap.search_coord(ref)
            except KeyError:
                log.erroe('Some Reference are non existing : ABORT')
                return 0

        plate_ref_data = None

        for key, value in plate.replicat.items():
            tmp = self._get_replicat_reference_data(value, well_ref, chan=chan)
            if plate_ref_data is not None:
                plate_ref_data = np.append(plate_ref_data, tmp, axis=1)
            else:
                plate_ref_data = tmp

        return plate_ref_data.reshape((1, -1))

    def _get_replicat_reference_data(self, replicat, refs, chan):
        ref_data = None
        # # we have a dict with key is ref name and value is well position
        for key, value in refs.items():
            tmp = self._ref_data_array([replicat.get_data_array(channel=chan)[x[0]][x[1]] for x in
                                        replicat.get_valid_well(value)])
            if ref_data is not None:
                ref_data = np.append(ref_data, tmp, axis=1)
            else:
                ref_data = tmp
        return ref_data

    @staticmethod
    def _ref_data_array(data):
        arr = np.zeros(3)
        arr[0] = np.mean(data)
        arr[1] = np.std(data)
        arr[2] = stats.sem(data)
        return arr