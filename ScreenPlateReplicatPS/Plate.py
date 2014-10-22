__author__ = 'Arnaud KOPP'
"""
Plate is designed for manipulating one or more replicat
"""
import numpy as np
import ScreenPlateReplicatPS.PlateSetup
import ScreenPlateReplicatPS.Replicat
import Statistic.ResultArray
import Statistic.Normalization.SystematicError


class Plate():
    '''
    classdocs
    Class for manipuling plate
    '''

    def __init__(self, ):
        '''
        Constructor
        :return: nothing
        '''
        self.replicat = {}  # Dict that contain all replicat, key are name and value are replicat object
        self.MetaInfo = {}  # Store some stuff
        self.Name = None  # Name of Plate
        self.PlateSetup = ScreenPlateReplicatPS.PlateSetup()  # Plate Setup
        self.Threshold = None  # Threeshold for considering Cell as positive
        self.ControlPos = (1, 12)  # column where control is positionned in plate (default pos)
        self.Neg = None  # Name of negative control
        self.Pos = None  # Name of positive control
        self.Tox = None  # Name of toxics control
        self.Result = None  # store result dataframe
        self.isNormalized = False  # Are replicat data normalized
        self.isSpatialNormalized = False  # Systematic error removed from plate data ( resulting from replicat )
        self.DataMean = None  # matrix that contain mean from replicat of interested features to analyze
        self.DataMedian = None  # matrix that contain median from replicat of interested feature to analyze
        self.SpatNormDataMean = None  # matrix that contain data corrected by median polish (bscore) or others technics
        self.SpatNormDataMedian = None  # matrix that contain data corrected by median polish (bscore) or others technics

    def printMetaInfo(self):
        '''
        Print MetaInfo for Plate object
        :return: print some output
        '''
        try:
            for keys, values in self.MetaInfo.items():
                print(keys, values)
        except Exception as e:
            print(e)

    def setName(self, name):
        '''
        Set Name of plate
        :param name:
        :return:
        '''
        try:
            self.Name = name
        except Exception as e:
            print(e)

    def getName(self):
        '''
        Get Name of plate
        :return:
        '''
        try:
            return self.Name
        except Exception as e:
            print(e)

    def addReplicat(self, replicat):
        '''
        Add replicat to plate
        :param replicat: Give a replicat object
        :return: nothing
        '''
        try:
            assert isinstance(replicat, ScreenPlateReplicatPS.Replicat)
            name = replicat.info
            self.replicat[name] = replicat
        except Exception as e:
            print(e)

    def getReplicat(self, name):
        '''
        Get the replicat specified by name
        :param name: string
        :return: TCA.Replicat
        '''
        try:
            return self.replicat[name]
        except Exception as e:
            print(e)

    def getAllReplicat(self):
        '''
        Get all replicat
        :return: TCA.Replicat
        '''
        try:
            return self.replicat
        except Exception as e:
            print(e)

    def getNumberReplicat(self):
        '''
        return number of replicat
        :return: int
        '''
        try:
            return len(self.replicat)
        except Exception as e:
            print(e)
            print('Error in getting number of replicat')

    def addInfo(self, key, value):
        '''
        Add Info into the dict
        :param key:
        :param value:
        :return: nothing
        '''
        try:
            self.MetaInfo.pop(key, value)
        except Exception as e:
            print(e)

    def getInfo(self):
        '''
        Get info
        :return: info (dict)
        '''
        try:
            return self.MetaInfo
        except Exception as e:
            print(e)
            print('Error in getting info')

    def getAllDataFromReplicat(self, features, Well=False):
        '''
        Return a dict with data of all dataframe, with feature specified
        :return:
        '''
        data = {}
        try:
            for rep in self.replicat:
                repTmp = self.replicat[rep]
                tmp = repTmp.getDataByFeatures(features, Well=Well)
                data[repTmp.getInfo()] = tmp
            return data
        except Exception as e:
            print(e)
            print('Error in getAllDataFromReplicat')

    def getAllData(self):
        '''
        return a dict which data of all dataframe without feature specified
        :return:
        '''
        data = {}
        try:
            for rep in self.replicat:
                tmp = self.replicat[rep]
                datatmp = tmp.getData()
                data[tmp.getInfo()] = datatmp
            return data
        except Exception as e:
            print(e)

    def addPlateSetup(self, platesetup):
        '''
        Add the platesetup to the plate
        :param platesetup:
        :return:
        '''
        try:
            assert isinstance(platesetup, ScreenPlateReplicatPS.PlateSetup)
            self.PlateSetup = platesetup
        except Exception as e:
            print(e)

    def getPlateSetup(self):
        '''
        Get the platesetup from the plate
        :return: plateSetup
        '''
        try:
            return self.PlateSetup
        except Exception as e:
            print(e)

    def addResult(self, result):
        '''
        Set the result by giving a TCA.Result array
        :param result:
        :return:
        '''
        try:
            assert isinstance(result, Statistic.Result)
            self.Result = result
        except Exception as e:
            print(e)

    def getResult(self):
        '''
        Get the result array
        :return:
        '''
        try:
            return self.Result
        except Exception as e:
            print(e)

    def computeDataFromReplicat(self, feature):
        '''
        Compute the mean/median matrix data of all replicat
        If replicat data is SpatialNorm already, this function will fill spatDataMatrix
        :return:
        '''
        try:
            mean_tmp = None
            median_tmp = None
            i = 0

            # we thinks that replicat are not spatial norm in first time
            isReplicatSpatNorm = False
            prev_check = None

            for key, replicat in self.replicat.items():
                i += 1
                if replicat.DataMean is None or replicat.DataMedian is None:
                    replicat.computeDataForFeature(feature)
                if mean_tmp is None or median_tmp is None:
                    mean_tmp = np.zeros(replicat.DataMean.shape)
                    median_tmp = np.zeros(replicat.DataMedian.shape)

                # Check replicat consistency with spat norm, if all rep is or not spat norm
                isReplicatSpatNorm = replicat.isSpatialNormalized
                if not i == 1:
                    if not prev_check == isReplicatSpatNorm:
                        raise Exception('All replicat are uniform is spatial correction')
                prev_check = replicat.isSpatialNormalized
                mean_tmp = mean_tmp + replicat.DataMean
                median_tmp = median_tmp + replicat.DataMedian

            if not isReplicatSpatNorm:
                self.DataMean = mean_tmp / i
                self.DataMedian = median_tmp / i
            else:
                self.SpatNormDataMean = mean_tmp / i
                self.SpatNormDataMedian = median_tmp / i
                self.isSpatialNormalized = True
        except Exception as e:
            print(e)

    def Normalization(self, feature, technics, log=True):
        '''
        Apply Well correction on all replicat data
        :param feature: feature to normalize
        :param technics: which method to perform
        :param log:  Performed log2 Transformation
        '''
        try:
            for key, value in self.replicat.items():
                value.Normalization(feature=feature, method=technics, log=log)
            self.isNormalized = True
        except Exception as e:
            print(e)

    def SystematicErrorCorrection(self, Methods='Bscore', apply_down=False, verbose=False, save=False,
                                  max_iterations=100):
        '''
        Apply a spatial normalization for remove edge effect
        Resulting matrix are save in plate object if save = True
        Be careful !! if the replicat data was already be spatial norm, it will degrade data !!
        :param Methods: Bscore, MEA, PMP or diffusion model technics, default = Bscore
        :param apply_down: apply strategie to replicat, if true apply SEC on replicat !! not re-use function on plate
        :param verbose: verbose : output the result ?
        :param save: save: save the residual into self.SpatNormData , default = False
        :param max_iterations: max iterations for all technics
        '''
        try:
            if apply_down:
                for key, value in self.replicat.items():
                    value.SystematicErrorCorrection(Methods=Methods, verbose=verbose, save=save,
                                                    max_iterations=max_iterations)
                return 0

            if Methods == 'Bscore':
                if self.DataMedian is None:
                    raise ValueError("Compute Median of replicat first by using computeDataFromReplicat")
                elif self.isSpatialNormalized is True:
                    raise ValueError('SystematicErrorCorrection -> Systematics error have already been removed')
                else:
                    ge, ce, re, resid, tbl_org = Statistic.Normalization.MedianPolish(self.DataMedian.copy(),
                                                                                      max_iterations=max_iterations,
                                                                                      verbose=verbose)
                    if save:
                        self.SpatNormDataMedian = resid

                if self.DataMean is None:
                    raise ValueError("Compute Mean of replicat first by using computeDataFromReplicat")
                elif self.isSpatialNormalized is True:
                    raise ValueError('SystematicErrorCorrection -> Systematics error have already been removed')
                else:
                    ge, ce, re, resid, tbl_org = Statistic.Normalization.MedianPolish(self.DataMean.copy(),
                                                                                      max_iterations=max_iterations,
                                                                                      verbose=verbose)
                    if save:
                        self.SpatNormDataMean = resid
                        self.isSpatialNormalized = True
            if Methods == 'BZscore':
                if self.DataMedian is None:
                    raise ValueError("Compute Median of replicat first by using computeDataFromReplicat")
                elif self.isSpatialNormalized is True:
                    raise ValueError('SystematicErrorCorrection -> Systematics error have already been removed')
                else:
                    ge, ce, re, resid, tbl_org = Statistic.Normalization.BZMedianPolish(self.DataMedian.copy(),
                                                                                        max_iterations=max_iterations,
                                                                                        verbose=verbose)
                    if save:
                        self.SpatNormDataMedian = resid

                if self.DataMean is None:
                    raise ValueError("Compute Mean of replicat first by using computeDataFromReplicat")
                elif self.isSpatialNormalized is True:
                    raise ValueError('SystematicErrorCorrection -> Systematics error have already been removed')
                else:
                    ge, ce, re, resid, tbl_org = Statistic.Normalization.BZMedianPolish(self.DataMean.copy(),
                                                                                        max_iterations=max_iterations,
                                                                                        verbose=verbose)
                    if save:
                        self.SpatNormDataMean = resid
                        self.isSpatialNormalized = True

            if Methods == 'PMP':
                if self.DataMedian is None:
                    raise ValueError("Compute Median of replicat first by using computeDataFromReplicat")
                elif self.isSpatialNormalized is True:
                    raise ValueError('SystematicErrorCorrection -> Systematics error have already been removed')
                else:
                    resid = Statistic.Normalization.PartialMeanPolish(self.DataMedian.copy(),
                                                                      max_iteration=max_iterations, verbose=verbose)
                    if save:
                        self.SpatNormDataMedian = resid

                if self.DataMean is None:
                    raise ValueError("Compute Mean of replicat first by using computeDataFromReplicat")
                elif self.isSpatialNormalized is True:
                    raise ValueError('SystematicErrorCorrection -> Systematics error have already been removed')
                else:
                    resid = Statistic.Normalization.PartialMeanPolish(self.DataMean.copy(),
                                                                      max_iteration=max_iterations, verbose=verbose)
                    if save:
                        self.SpatNormDataMean = resid
                        self.isSpatialNormalized = True

            if Methods == 'MEA':
                if self.DataMedian is None:
                    raise ValueError("Compute Median of replicat first by using computeDataFromReplicat")
                elif self.isSpatialNormalized is True:
                    raise ValueError('SystematicErrorCorrection -> Systematics error have already been removed')
                else:
                    resid = Statistic.Normalization.MatrixErrorAmendment(self.DataMedian.copy(), verbose=verbose)
                    if save:
                        self.SpatNormDataMedian = resid

                if self.DataMean is None:
                    raise ValueError("Compute Mean of replicat first by using computeDataFromReplicat")
                elif self.isSpatialNormalized is True:
                    raise ValueError('SystematicErrorCorrection -> Systematics error have already been removed')
                else:
                    resid = Statistic.Normalization.MatrixErrorAmendment(self.DataMean.copy(), verbose=verbose)
                    if save:
                        self.SpatNormDataMean = resid
                        self.isSpatialNormalized = True

            if Methods == 'DiffusionModel':
                if self.DataMedian is None:
                    raise ValueError("Compute Median of replicat first by using computeDataFromReplicat")
                elif self.isSpatialNormalized is True:
                    raise ValueError('SystematicErrorCorrection -> Systematics error have already been removed')
                else:
                    CorrectedTable = Statistic.Normalization.diffusionModel(self.DataMedian,
                                                                            max_iterations=max_iterations,
                                                                            verbose=verbose)

                    if save:
                        self.SpatNormDataMedian = CorrectedTable

                if self.DataMean is None:
                    raise ValueError("Compute Mean of replicat first by using computeDataFromReplicat")
                elif self.isSpatialNormalized is True:
                    raise ValueError('SystematicErrorCorrection -> Systematics error have already been removed')
                else:
                    CorrectedTable = Statistic.Normalization.diffusionModel(self.DataMean,
                                                                            max_iterations=max_iterations,
                                                                            verbose=verbose)

                    if save:
                        self.SpatNormDataMean = CorrectedTable
                        self.isSpatialNormalized = True

        except Exception as e:
            print(e)

    def __add__(self, replicat):
        '''
        Add replicat object
        :param replicat:
        '''
        try:
            assert isinstance(replicat, ScreenPlateReplicatPS.Replicat)
            name = replicat.info
            self.replicat[name] = replicat
        except Exception as e:
            print(e)

    def __getitem__(self, key):
        '''
        Return replicat object
        :param key:
        :return: return replicat
        '''
        try:
            return self.replicat[key]
        except Exception as e:
            print(e)

    def __len__(self):
        '''
        Get len /number of replicat inside Plate
        :return: number of replicat
        '''
        try:
            return len(self.replicat)
        except Exception as e:
            print(e)

    def __repr__(self):
        '''
        Definition for the representation
        :return:
        '''
        try:
            return (
                "\n Plate : \n" + repr(self.Name) + "\n MetaInfo : \n" + repr(
                    self.MetaInfo) + "\n PlateSetup : \n" + repr(self.PlateSetup) + "\n Array Result :\n" + repr(
                    self.Result) + "\n Data systematic error removed ? : \n" + repr(self.isSpatialNormalized) +
                "\n Replicat List : \n" + repr(self.replicat))
        except Exception as e:
            print(e)

    def __str__(self):
        '''
        Definition for the print
        :return:
        '''
        try:
            return (
                "\n Plate : \n" + repr(self.Name) + "\n MetaInfo : \n" + repr(
                    self.MetaInfo) + "\n PlateSetup : \n" + repr(self.PlateSetup) + "\n Array Result :\n" + repr(
                    self.Result) + "\n Data systematic error removed ? : \n" + repr(self.isSpatialNormalized) +
                "\n Replicat List : \n" + repr(self.replicat))
        except Exception as e:
            print(e)
