"""
Plate is designed for manipulating one or more replicat
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


class Plate(object):
    """
    classdocs
    Class for manipuling plate and their replicat :

    self.replicat = {}  # Dict that contain all replicat, key are name and value are replicat object
    self.MetaInfo = {}  # Store some stuff
    self.Name = None  # Name of Plate
    self.PlateMap = ScreenPlateReplicatPS.PlateMap()  # Plate Setup object
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

    def __init__(self, name=None):
        """
        Constructor
        """
        self.replicat = {}
        self.MetaInfo = {}
        self.Name = name

        self.PlateMap = TCA.Core.PlateMap()
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
            print("\033[0;31m[ERROR]\033[0m", e)

    def setName(self, name):
        """
        Set Name for plate
        :param name:
        """
        try:
            self.Name = name
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def getName(self):
        """
        Get Name of plate
        :return: Name of plate
        """
        try:
            return self.Name
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def setDataX(self, Array, type):
        """
        Set attribut data matrix into self.Data
        This method is designed for 1Data/Well or for manual analysis
        :param Array: numpy array with good shape
        :param type: median or mean data
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
            print("\033[0;31m[ERROR]\033[0m", e)

    def addReplicat(self, replicat):
        """
        Add replicat object to plate
        :param replicat: Give a replicat object
        """
        try:
            assert isinstance(replicat, TCA.Core.Replicat)
            name = replicat.name
            self.replicat[name] = replicat
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def getReplicat(self, name):
        """
        Get the replicat specified by name
        :param name: string : key of replicat in dict
        :return: Replicat object
        """
        try:
            return self.replicat[name]
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def getAllReplicat(self):
        """
        Get all replicat from plate
        :return: dict of replicat
        """
        try:
            return self.replicat
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def addInfo(self, key, value):
        """
        Add Info into the dict
        :param key: key of info
        :param value: text for info
        """
        try:
            self.MetaInfo.pop(key, value)
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def getInfo(self, key):
        """
        Get desired info with key
        :param key: key of info
        :return: info value from key
        """
        try:
            return self.MetaInfo[key]
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m ", e)

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
            print('\033[0;31m[ERROR]\033[0m  Error in getAllDataFromReplicat ', e)

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
            print("\033[0;31m[ERROR]\033[0m", e)

    def addPlateMap(self, platemap):
        """
        Add the platemap to the plate
        :param platemap:
        """
        try:
            assert isinstance(platemap, TCA.Core.PlateMap)
            self.PlateMap = platemap
        except Exception as e:
            print(e)

    def getPlateMap(self):
        """
        Get the platemap from the plate
        :return: platemap
        """
        try:
            return self.PlateMap
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def addResult(self, result):
        """
        Set the result by giving a Result array
        :param result: result object
        """
        try:
            assert isinstance(result, TCA.Core.Result)
            self.Result = result
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def getResult(self):
        """
        Get the result array
        :return: result object
        """
        try:
            return self.Result
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def computeAllcomponentFromReplicat(self):
        """
        compute all component mean from all replicat for each well
        :return: dataframe
        """
        try:
            df = None
            for key, rep in self.replicat.items():
                assert isinstance(rep, TCA.Replicat)
                tmp = rep.Dataframe.groupby("Well")
                if df is None:
                    df = tmp.median()
                else:
                    df += tmp.median()
            return df / len(self.replicat)
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def computeDataFromReplicat(self, feature, SECData=False):
        """
        Compute the mean/median matrix data of all replicat
        If replicat data is SpatialNorm already, this function will fill spatDataMatrix
        :param feature: which feature to have into sum up data
        """
        try:
            tmp_array = np.zeros(self.PlateMap.platemap.shape)
            i = 0

            for key, replicat in self.replicat.items():
                i += 1
                if replicat.Data is None:
                    replicat.computeDataForFeature(feature)

                if not SECData:
                    tmp_array = tmp_array + replicat.Data
                else:
                    tmp_array = tmp_array + replicat.SECData

            if not SECData:
                self.Data = tmp_array / i
            else:
                self.SECData = tmp_array / i
                self.isSpatialNormalized = True
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def Normalization(self, feature, technics='Zscore', log=True, neg=None, pos=None):
        """
        Apply Well correction on all replicat data
        call function like from replicat object
        :param feature: feature to normalize
        :param technics: which method to perform
        :param log:  Performed log2 Transformation
        """
        try:
            for key, value in self.replicat.items():
                value.Normalization(feature=feature, method=technics, log=log, neg=neg, pos=pos)
            self.isNormalized = True
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

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
                    ge, ce, re, resid, tbl_org = TCA.MedianPolish(self.Data, method=method,
                                                                  max_iterations=max_iterations,
                                                                  verbose=verbose)
                    if save:
                        self.SECData = resid
                        self.isSpatialNormalized = True
                if Algorithm == 'BZscore':
                    ge, ce, re, resid, tbl_org = TCA.BZMedianPolish(self.Data, method=method,
                                                                    max_iterations=max_iterations,
                                                                    verbose=verbose)
                    if save:
                        self.SECData = resid
                        self.isSpatialNormalized = True

                if Algorithm == 'PMP':
                    CorrectedTable = TCA.PartialMeanPolish(self.Data, max_iteration=max_iterations, verbose=verbose)
                    if save:
                        self.SECData = CorrectedTable
                        self.isSpatialNormalized = True

                if Algorithm == 'MEA':
                    CorrectedTable = TCA.MatrixErrorAmendment(self.Data, verbose=verbose)
                    if save:
                        self.SECData = CorrectedTable
                        self.isSpatialNormalized = True

                if Algorithm == 'DiffusionModel':
                    CorrectedTable = TCA.diffusionModel(self.Data, max_iterations=max_iterations, verbose=verbose)
                    if save:
                        self.SECData = CorrectedTable
                        self.isSpatialNormalized = True

        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def __add__(self, object):
        """
        Add object object, use + operator
        :param object:
        """
        try:
            if isinstance(object, TCA.Core.Replicat):
                name = object.name
                self.replicat[name] = object
            elif isinstance(object, TCA.Core.PlateMap):
                self.PlateMap = object
            elif isinstance(object, list):
                for elem in object:
                    assert isinstance(elem, TCA.Core.Replicat)
                    self.replicat[elem.name] = elem
            else:
                raise AttributeError("\033[0;31m[ERROR]\033[0m Unsupported Type")
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def __getitem__(self, key):
        """
        Return replicat object, use [] operator
        :param key:
        :return: return replicat
        """
        try:
            return self.replicat[key]
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def __setitem__(self, key, value):
        """
        Set replicat objet, use [] operator
        :param key: name of replicat
        :param value: replicat object
        """
        try:
            if not isinstance(value, TCA.Replicat):
                raise AttributeError("\033[0;31m[ERROR]\033[0m Unsupported Type")
            else:
                self.replicat[key] = value
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def __len__(self):
        """
        Get len /number of replicat inside Plate, use len(object)
        :return: number of replicat
        """
        try:
            return len(self.replicat)
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def __repr__(self):
        """
        Definition for the representation
        """
        try:
            return (
                "\n Plate : " + repr(self.Name) +
                "\n MetaInfo : \n" + repr(self.MetaInfo) +
                "\n PlateMap : \n" + repr(self.PlateMap) +
                "\n Array Result :\n" + repr(self.Result) +
                "\n Data normalized ? " + repr(self.isNormalized) +
                "\n Data systematic error removed ? " + repr(self.isSpatialNormalized) +
                "\n Replicat List : \n" + repr(self.replicat))
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def __str__(self):
        """
        Definition for the print
        """
        try:
            return (
                "\n Plate : " + repr(self.Name) +
                "\n MetaInfo : \n" + repr(self.MetaInfo) +
                "\n PlateMap : \n" + repr(self.PlateMap) +
                "\n Array Result :\n" + repr(self.Result) +
                "\n Data normalized ? " + repr(self.isNormalized) +
                "\n Data systematic error removed ? " + repr(self.isSpatialNormalized) +
                "\n Replicat List : \n" + repr(self.replicat))
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)
