# coding=utf-8
"""
Screen is designed for manipulating screen that contain multiple different plate
This class is a bit useless because of you have many plate  you will need a lot of memory !!!
"""

import TransCellAssay as TCA
import collections

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


class Screen(object):
    """
    Class that defined a screen, and contain several plate
    """

    def __init__(self):
        """
        Constructor
        self.allPlate = {} # dict that contain all plate
        self.Info = {} # Dict that contain info
        self.type = None # type of screen : siRNA or compounds
        self.Threshold = None  # Threeshold for considering Cell as positive
        self.Neg = None # Negative reference for the screen
        self.Pos = None # Positive reference for the screen
        self.Tox = None  # Toxicity reference for the screen
        self.shape = (8, 12) # Default shape of plate
        """
        self.plate = collections.OrderedDict()
        self.Info = {}
        self.type = None
        self.Threshold = None
        self.Neg = None
        self.Pos = None
        self.Tox = None
        self.isNormalized = False
        self.isSpatialNormalized = False
        self.shape = (8, 12)

    def add_plate(self, plate):
        """
        Add plate to the screen
        :param plate: input plate
        """
        try:
            assert isinstance(plate, TCA.Core.Plate)
            self.plate[plate.Name] = plate
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def get_plate(self, name):
        """
        Return Plate specified by name
        :param name: name of plate
        :return: plate
        """
        try:
            return self.plate[name]
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def add_info(self, key, value):
        """
        Add Info
        :param key: key of info
        :param value: value of info
        """
        try:
            self.Info.pop(key, value)
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def get_info(self):
        """
        Get info with desired key
        :return: info (dict)
        """
        try:
            return self.Info
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def apply_normalization(self, feature, technics='Zscore', log=True, neg=None, pos=None):
        """
        Apply Well correction on all Plate data
        call function like from Plate object
        :param pos: positive control
        :param neg: negative control
        :param feature: feature to normalize
        :param technics: which method to perform
        :param log:  Performed log2 Transformation
        """
        try:
            if self.isNormalized:
                raise Exception("\033[0;33m[WARNING]\033[0m Data are already normalized")
            else:
                for key, value in self.plate.items():
                    value.normalization(feature=feature, method=technics, log=log, neg=neg, pos=pos)
                self.isNormalized = True
        except Exception as e:
            print(e)

    def apply_systematic_error_correction(self, algorithm='Bscore', method='median', apply_down=False, verbose=False,
                                          save=False, max_iterations=100):
        """
        Apply Systematic Error Corection on all plate of the screen
        :param algorithm:
        :param method:
        :param apply_down:
        :param verbose:
        :param save:
        :param max_iterations:
        :return:
        """
        try:
            if algorithm == 'WellCorrection':
                raise NotImplementedError('Use a lot of memory, for the moment this function is not activated')
            elif algorithm == 'BackgroundCorrection':
                raise NotImplementedError('Use a lot of memory, for the moment this function is not activated')
            elif algorithm == 'BackgroundSubstraction':
                raise NotImplementedError('Use a lot of memory, for the moment this function is not activated')
            else:
                if self.isSpatialNormalized:
                    raise Exception("\033[0;33m[WARNING]\033[0m Systematics error have already been removed")
                else:
                    for key, value in self.plate.items():
                        value.systematic_error_correction(algorithm=algorithm, method=method, apply_down=apply_down,
                                                          verbose=verbose, save=save, max_iterations=max_iterations)
                self.isSpatialNormalized = True
        except Exception as e:
            print(e)

    def __len__(self):
        """
        get number of plate
        :return: int
        """
        try:
            return len(self.plate)
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def __sub__(self, to_rm):
        """
        Remove plate from screen, use - operator
        :param to_rm:
        """
        try:
            del self.plate[to_rm]
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def __add__(self, to_add):
        """
        using + operator
        Add plate to the screen
        :param to_add: input plate
        """
        try:
            if isinstance(to_add, list):
                for elem in to_add:
                    assert isinstance(elem, TCA.Plate)
                    self.plate[elem.Name] = to_add
            if isinstance(to_add, TCA.Core.Plate):
                self.plate[to_add.Name] = to_add
            else:
                raise AttributeError
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def __getitem__(self, key):
        """
        get plate object, use [] operator
        :param key:
        :return: return plate
        """
        try:
            return self.plate[key]
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def __setitem__(self, key, value):
        """
        Set plate objet, use [] operator
        :param key: name of plate
        :param value: plate object
        """
        try:
            if not isinstance(value, TCA.Plate):
                raise AttributeError("\033[0;31m[ERROR]\033[0m Unsupported Type")
            else:
                self.plate[key] = value
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def __repr__(self):
        """
        Definition for the representation
        """
        try:
            return ("\n SCREEN OBJECT :\n" +
                    "\n Threshold : \n" + repr(self.Threshold) +
                    "\n Neg Control \n" + repr(self.Neg) +
                    "\n Pos Control \n" + repr(self.Pos) +
                    "\n Tox Control \n" + repr(self.Tox) + "\n")
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def __str__(self):
        """
        Definition for the print
        """
        try:
            return ("\n SCREEN OBJECT :\n" +
                    "\n Threshold : \n" + repr(self.Threshold) +
                    "\n Neg Control \n" + repr(self.Neg) +
                    "\n Pos Control \n" + repr(self.Pos) +
                    "\n Tox Control \n" + repr(self.Tox) + "\n")
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)
