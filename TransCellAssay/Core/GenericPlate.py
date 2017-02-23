# coding=utf-8
"""
plate is bass class for Plate and Replica
"""

import numpy as np
import TransCellAssay as TCA
import logging
log = logging.getLogger(__name__)


__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2017 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "GPLv3"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"


class GenericPlate(object):
    """
    Generic class for Plate and Replica
    """

    def __init__(self, name, datatype='mean', skip=()):
        """
        Constructor
        """
        self.name = name                    # Name of plate
        self.array = None                   # Array contain mean or median of all well, represent data
        self.array_c = None                 # Array of data that are corrected (spatial norm)
        self._array_channel = None          # On which channel data are based
        self.datatype = datatype            # Data type -> Mean or Median
        self.isNormalized = False           # Are raw data normalized
        self.isSpatialNormalized = False    # Are array spatialy corrected
        self.RawDataNormMethod = None       # Which method are used for raw data normalization
        self.SECNormMethod = None           # Which method are used for spatial correction
        self.skip_well = skip               # List of skipped well (not so used)
        self._is_cutted = False             # Are plate cutted
        self._rb = None
        self._re = None
        self._cb = None
        self._ce = None
        self.WellKey = 'Well'

    def set_name(self, name):
        """
        Set Name for plate
        :param name:
        """
        self.name = name

    def get_name(self):
        """
        Get Name of plate
        :return: Name of plate
        """
        return self.name

    def set_data(self, array):
        """
        Set data matrix into self.array
        This method is designed for 1Data/Well or for manual analysis
        :param array: numpy array with good shape
        """
        assert isinstance(array, np.ndarray)
        self.array = array

    def set_skip_well(self, to_skip):
        """
        Set the well to skip in neg or pos control
        :param to_skip: list of well to skip (1,3) or B3
        """
        well_list = list()
        for elem in to_skip:
            if isinstance(elem, tuple):
                well_list.append(elem)
            elif isinstance(elem, str):
                well_list.append(TCA.get_opposite_well_format(elem))
            else:
                pass
        self.skip_well = well_list

    def get_skip_well(self):
        """
        get the well to skip in neg or pos control
        """
        return self.skip_well

    def cut(self, rb, re, cb, ce):
        """
        Cut the replica to 'zoom' into a defined zone, for avoiding crappy effect during SEC process
        :param rb: row begin
        :param re: row end
        :param cb: col begin
        :param ce: col end
        """
        if self._is_cutted:
            raise AttributeError('Already cutted')
        if self.array is not None:
            self.array = self.array[rb: re, cb: ce]
        if self.array_c is not None:
            self.array_c = self.array_c[rb: re, cb: ce]
        log.debug('Cutting operation : {0} (param {1}:{2},{3}:{4})'.format(self.name, rb, re, cb, ce))
        self._is_cutted = True
        self._rb = rb
        self._re = re
        self._cb = cb
        self._ce = ce

    def systematic_error_correction(self, algorithm='Bscore', verbose=False, save=True, max_iterations=100, alpha=0.05,
                                    epsilon=0.01, skip_col=[], skip_row=[], poly_deg=4, low_max_iter=3, f=2./3.):
        """
        Apply a spatial normalization for remove edge effect
        The Bscore method showed a more stable behavior than MEA and PMP only when the number of rows and columns
        affected by the systematics error, hit percentage and systematic error variance were high (mainly du to a
        mediocre performance of the t-test in this case). MEA was generally the best method for correcting
        systematic error within 96-well plates, whereas PMP performed better for 384 /1526 well plates.

        :param alpha: alpha for some algorithm
        :param algorithm: Bscore, MEA, PMP or diffusion model technics, default = Bscore
        :param verbose: Output in console
        :param save: save the result into self.SECData, default = False
        :param max_iterations: maximum iterations loop, default = 100
        :param epsilon: epsilon parameters for PMP
        :param skip_col: index of col to skip in MEA or PMP
        :param skip_row: index of row to skip in MEA or PMP
        :param poly_deg: polynomial degree 4 or 5
        :param low_max_iter: lowess max iteration
        :param f: lowess smotting span
        """
        global corrected_data_array
        __valid_sec_algo = ['Bscore', 'BZscore', 'PMP', 'MEA', 'DiffusionModel', 'Lowess', 'Polynomial']

        if algorithm not in __valid_sec_algo:
            log.error('Algorithm is not good choose : {}'.format(__valid_sec_algo))
            raise ValueError()

        if self.array is None:
            log.error("Use first : compute_data_for_channel")
            raise AttributeError()

        else:
            if self.isSpatialNormalized:
                log.warning('SEC already performed -> overwriting previous sec data')

            log.debug('Systematic Error Correction processing : {} -> replica {}'.format(algorithm, self.name))

            if algorithm == 'Bscore':
                ge, ce, re, corrected_data_array, tbl_org = TCA.bscore(self.array.copy(), max_iterations=max_iterations,
                                                                       eps=epsilon, verbose=verbose)

            if algorithm == 'BZscore':
                ge, ce, re, corrected_data_array, tbl_org = TCA.bzscore(self.array.copy(),
                                                                        max_iterations=max_iterations, eps=epsilon,
                                                                        verbose=verbose)

            if algorithm == 'PMP':
                corrected_data_array = TCA.partial_mean_polish(self.array.copy(), max_iteration=max_iterations,
                                                               verbose=verbose, alpha=alpha, epsilon=epsilon,
                                                               skip_col=skip_col, skip_row=skip_row)

            if algorithm == 'MEA':
                corrected_data_array = TCA.matrix_error_amendmend(self.array.copy(), verbose=verbose, alpha=alpha,
                                                                  skip_col=skip_col, skip_row=skip_row)

            if algorithm == 'DiffusionModel':
                corrected_data_array = TCA.diffusion_model(self.array.copy(), max_iterations=max_iterations,
                                                           verbose=verbose)

            if algorithm == 'Lowess':
                corrected_data_array = TCA.lowess_fitting(self.array.copy(), max_iteration=low_max_iter,
                                                          skip_col=skip_col, skip_row=skip_row, f=f)

            if algorithm == 'Polynomial':
                corrected_data_array = TCA.polynomial_fitting(self.array.copy(), degree=poly_deg, skip_col=skip_row,
                                                              skip_row=skip_col)

            if save:
                self.array_c = corrected_data_array
                self.isSpatialNormalized = True
                self.SECNormMethod = algorithm
            else:
                return corrected_data_array
