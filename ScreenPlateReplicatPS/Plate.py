"""
Plate is designed for manipulating one or more replicat
"""

import numpy as np
import ScreenPlateReplicatPS.PlateSetup
import ScreenPlateReplicatPS.Replicat
import Statistic.ResultArray
import Statistic.Normalization.SystematicError

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


class Plate():
    """
    classdocs
    Class for manipuling plate and their replicat :

    self.replicat = {}  # Dict that contain all replicat, key are name and value are replicat object
    self.MetaInfo = {}  # Store some stuff
    self.Name = None  # Name of Plate
    self.PlateSetup = ScreenPlateReplicatPS.PlateSetup()  # Plate Setup object
    self.Threshold = None  # Threeshold for considering Cell as positive
    self.ControlPos = ((0, 11), (0, 23))  # column where control is positionned in plate (default pos)
    self.Neg = None  # Name of negative control
    self.Pos = None  # Name of positive control
    self.Tox = None  # Name of toxics control
    self.Result = None  # store result into result object (it's a pandas dataframe)
    self.isNormalized = False  # Are replicat data normalized
    self.isSpatialNormalized = False  # Systematic error removed from plate data ( resulting from replicat )
    self.DataType = "median" # median or mean data, default is median
    self.Data = None  # matrix that contain data from replicat of interested features to analyze
    self.SECData = None  # matrix that contain data corrected or from replicat data
    """

    def __init__(self):
        """
        Constructor
        """
        self.replicat = {}
        self.MetaInfo = {}
        self.Name = None

        self.PlateSetup = ScreenPlateReplicatPS.PlateSetup()
        self.Threshold = None
        self.ControlPos = ((0, 11), (0, 23))

        self.Neg = None
        self.Pos = None
        self.Tox = None

        self.Result = None

        self.isNormalized = False
        self.isSpatialNormalized = False

        self.DataType = "median"
        self.Data = None
        self.SECData = None

    def printMetaInfo(self):
        """
        Print all data contains in MetaInfo for Plate object
        :return: print some output
        """
        try:
            for keys, values in self.MetaInfo.items():
                print(keys, values)
        except Exception as e:
            print(e)

    def setName(self, name):
        """
        Set Name for plate
        :param name:
        """
        try:
            self.Name = name
        except Exception as e:
            print(e)

    def getName(self):
        """
        Get Name of plate
        :return: Name of plate
        """
        try:
            return self.Name
        except Exception as e:
            print(e)

    def setDataX(self, Array, type):
        """
        Set attribut data matrix into self.Data
        :param Array:
        :param type:
        :return:
        """
        try:
            if isinstance(Array, np.ndarray):
                self.Data = Array
                if type == 'median':
                    self.DataType = type
                elif type == 'mean':
                    self.DataType = type
                else:
                    raise AttributeError("\033[0;31m[ERROR]\033[0m Must provided data type")
            else:
                raise AttributeError("\033[0;31m[ERROR]\033[0m Must provied numpy ndarray")
        except Exception as e:
            print(e)

    def addReplicat(self, replicat):
        """
        Add replicat object to plate
        :param replicat: Give a replicat object
        """
        try:
            assert isinstance(replicat, ScreenPlateReplicatPS.Replicat)
            name = replicat.name
            self.replicat[name] = replicat
        except Exception as e:
            print(e)

    def getReplicat(self, name):
        """
        Get the replicat specified by name
        :param name: string : key of replicat in dict
        :return: Replicat object
        """
        try:
            return self.replicat[name]
        except Exception as e:
            print(e)

    def getAllReplicat(self):
        """
        Get all replicat from plate
        :return: dict of replicat
        """
        try:
            return self.replicat
        except Exception as e:
            print(e)

    def addInfo(self, key, value):
        """
        Add Info into the dict
        :param key: key of info
        :param value: text for info
        """
        try:
            self.MetaInfo.pop(key, value)
        except Exception as e:
            print(e)

    def getInfo(self, key):
        """
        Get desired info with key
        :param key: key of info
        :return: info value from key
        """
        try:
            return self.MetaInfo[key]
        except Exception as e:
            print(e)
            print('Error in getting info')

    def getAllDataFromReplicat(self, features, Well=False):
        """
        Return a dict with data of all dataframe, with feature specified
        :param features: which feature to get
        :param Well: add well position into data
        :return: return a dict with all dataframe from replicat
        """
        data = {}
        try:
            for rep in self.replicat:
                repTmp = self.replicat[rep]
                tmp = repTmp.getDataByFeatures(features, Well=Well)
                data[repTmp.getName()] = tmp
            return data
        except Exception as e:
            print(e)
            print('\033[0;31m[ERROR]\033[0m  Error in getAllDataFromReplicat')

    def getAllData(self):
        """
        return a dict which data of all dataframe without feature specified
        :return: dict
        """
        data = {}
        try:
            for rep in self.replicat:
                tmp = self.replicat[rep]
                datatmp = tmp.getData()
                data[tmp.getName()] = datatmp
            return data
        except Exception as e:
            print(e)

    def addPlateSetup(self, platesetup):
        """
        Add the platesetup to the plate
        :param platesetup:
        """
        try:
            assert isinstance(platesetup, ScreenPlateReplicatPS.PlateSetup)
            self.PlateSetup = platesetup
        except Exception as e:
            print(e)

    def getPlateSetup(self):
        """
        Get the platesetup from the plate
        :return: plateSetup
        """
        try:
            return self.PlateSetup
        except Exception as e:
            print(e)

    def addResult(self, result):
        """
        Set the result by giving a Result array
        :param result: result object
        """
        try:
            assert isinstance(result, Statistic.Result)
            self.Result = result
        except Exception as e:
            print(e)

    def getResult(self):
        """
        Get the result array
        :return: result object
        """
        try:
            return self.Result
        except Exception as e:
            print(e)

    def computeDataFromReplicat(self, feature, data_type="median"):
        """
        Compute the mean/median matrix data of all replicat
        If replicat data is SpatialNorm already, this function will fill spatDataMatrix
        :param feature: which feature to have into sum up data
        """
        try:
            tmp_array = None
            i = 0

            # we thinks that replicat are not spatial norm in first time
            isReplicatSpatNorm = False
            prev_check = None

            for key, replicat in self.replicat.items():
                i += 1
                if replicat.Data is None:
                    replicat.computeDataForFeature(feature, data_type=data_type)
                if tmp_array is None:
                    tmp_array = np.zeros(replicat.Data.shape)

                # Check replicat consistency with spat norm, if all rep is or not spat norm
                isReplicatSpatNorm = replicat.isSpatialNormalized
                if not i == 1:
                    if not prev_check == isReplicatSpatNorm:
                        raise Exception('\033[0;31m[ERROR]\033[0m  All replicat are uniform is spatial correction')
                prev_check = replicat.isSpatialNormalized
                tmp_array = tmp_array + replicat.Data

            if not isReplicatSpatNorm:
                self.Data = tmp_array / i
            else:
                self.SECData = tmp_array / i
                self.isSpatialNormalized = True
        except Exception as e:
            print(e)

    def Normalization(self, feature, technics='Zscore', log=True):
        """
        Apply Well correction on all replicat data
        call function like from replicat object
        :param feature: feature to normalize
        :param technics: which method to perform
        :param log:  Performed log2 Transformation
        """
        try:
            for key, value in self.replicat.items():
                value.Normalization(feature=feature, method=technics, log=log)
            self.isNormalized = True
        except Exception as e:
            print(e)

    def SystematicErrorCorrection(self, Algorithm='Bscore', method='median', apply_down=False, verbose=False,
                                  save=False,
                                  max_iterations=100):
        """
        Apply a spatial normalization for remove edge effect
        Resulting matrix are save in plate object if save = True
        Be careful !! if the replicat data was already be spatial norm, it will degrade data !!
        :param Algorithm: Bscore, MEA, PMP or diffusion model technics, default = Bscore
        :param method: for bscore : use median or average method
        :param apply_down: apply strategie to replicat, if true apply SEC on replicat !! not re-use function on plate
        :param verbose: verbose : output the result ?
        :param save: save: save the residual into self.SpatNormData , default = False
        :param max_iterations: max iterations for all technics
        """
        try:
            if apply_down:
                for key, value in self.replicat.items():
                    value.SystematicErrorCorrection(Algorithm=Algorithm, method=method, verbose=verbose, save=save,
                                                    max_iterations=max_iterations)
                return 0

            if self.Data is None:
                raise ValueError(
                    "\033[0;31m[ERROR]\033[0m  Compute Median of replicat first by using computeDataFromReplicat")
            elif self.isSpatialNormalized is True:
                raise ValueError(
                    "\033[0;31m[ERROR]\033[0m  SystematicErrorCorrection -> Systematics error have already been removed")
            else:
                if Algorithm == 'Bscore':
                    ge, ce, re, resid, tbl_org = Statistic.Normalization.MedianPolish(self.Data.copy(),
                                                                                      method=method,
                                                                                      max_iterations=max_iterations,
                                                                                      verbose=verbose)
                    if save:
                        self.SECData = resid
                        self.isSpatialNormalized = True
                if Algorithm == 'BZscore':
                    ge, ce, re, resid, tbl_org = Statistic.Normalization.BZMedianPolish(self.Data.copy(),
                                                                                        method=method,
                                                                                        max_iterations=max_iterations,
                                                                                        verbose=verbose)
                    if save:
                        self.SECData = resid
                        self.isSpatialNormalized = True

                if Algorithm == 'PMP':
                    CorrectedTable = Statistic.Normalization.PartialMeanPolish(self.Data.copy(),
                                                                               max_iteration=max_iterations,
                                                                               verbose=verbose)
                    if save:
                        self.SECData = CorrectedTable
                        self.isSpatialNormalized = True

                if Algorithm == 'MEA':
                    CorrectedTable = Statistic.Normalization.MatrixErrorAmendment(self.Data.copy(), verbose=verbose)
                    if save:
                        self.SECData = CorrectedTable
                        self.isSpatialNormalized = True

                if Algorithm == 'DiffusionModel':
                    CorrectedTable = Statistic.Normalization.diffusionModel(self.Data.copy(),
                                                                            max_iterations=max_iterations,
                                                                            verbose=verbose)
                    if save:
                        self.SECData = CorrectedTable
                        self.isSpatialNormalized = True

        except Exception as e:
            print(e)

    def __add__(self, object):
        """
        Add object object, use + operator
        :param object:
        """
        try:
            if isinstance(object, ScreenPlateReplicatPS.Replicat):
                name = object.name
                self.replicat[name] = object
            elif isinstance(object, ScreenPlateReplicatPS.PlateSetup):
                self.PlateSetup = object
            else:
                raise AttributeError("\033[0;31m[ERROR]\033[0m Unsupported Type")
        except Exception as e:
            print(e)

    def __getitem__(self, key):
        """
        Return replicat object, use [] operator
        :param key:
        :return: return replicat
        """
        try:
            return self.replicat[key]
        except Exception as e:
            print(e)

    def __len__(self):
        """
        Get len /number of replicat inside Plate, use len(object)
        :return: number of replicat
        """
        try:
            return len(self.replicat)
        except Exception as e:
            print(e)

    def __repr__(self):
        """
        Definition for the representation
        """
        try:
            return (
                "\n Plate : \n" + repr(self.Name) +
                "\n MetaInfo : \n" + repr(self.MetaInfo) +
                "\n PlateSetup : \n" + repr(self.PlateSetup) +
                "\n Array Result :\n" + repr(self.Result) +
                "\n Data normalized ? " + repr(self.isNormalized) +
                "\n Data systematic error removed ? : \n" + repr(self.isSpatialNormalized) +
                "\n Replicat List : \n" + repr(self.replicat))
        except Exception as e:
            print(e)

    def __str__(self):
        """
        Definition for the print
        """
        try:
            return (
                "\n Plate : \n" + repr(self.Name) +
                "\n MetaInfo : \n" + repr(self.MetaInfo) +
                "\n PlateSetup : \n" + repr(self.PlateSetup) +
                "\n Array Result :\n" + repr(self.Result) +
                "\n Data normalized ? " + repr(self.isNormalized) +
                "\n Data systematic error removed ? : \n" + repr(self.isSpatialNormalized) +
                "\n Replicat List : \n" + repr(self.replicat))
        except Exception as e:
            print(e)
