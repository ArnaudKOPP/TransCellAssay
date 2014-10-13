__author__ = 'Arnaud KOPP'
"""
Plate is designed for manipulating one or more replicat
"""
import numpy as np
import TCA.PlateSetup
import TCA.Replicat
import Statistic.ResultArray
import Statistic.Normalization.PlateNorm


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
        self.replicat = {}
        self.MetaInfo = {}
        self.Name = None
        self.PlateSetup = TCA.PlateSetup()
        self.NormBetweenRep = False
        self.ControlPos = (1, 12)  # column where control is positionned in plate (default pos)
        self.Result = None
        self.isNormalized = False
        self.isSpatialNormalized = False
        self.DataMatrixMean = None  # matrix that contain mean from replicat of interested features to analyze
        self.DataMatrixMedian = None  # matrix that contain median from replicat of interested feature to analyze
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
        :param name:  Give a name for added replicat object
        :return: nothing
        '''
        try:
            assert isinstance(replicat, TCA.Replicat)
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

    def getAllDataFromReplicat(self, features):
        '''
        Return a dict with data of all dataframe, with feature specified
        :return:
        '''
        data = {}
        try:
            for rep in self.replicat:
                repTmp = self.replicat[rep]
                tmp = repTmp.getDataByFeatures(features)
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
            assert isinstance(platesetup, TCA.PlateSetup)
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
        :return:
        '''
        try:
            mean_tmp = None
            median_tmp = None
            i = 0
            for key, replicat in self.replicat.items():
                if replicat.DataMatrixMean is None or replicat.DataMatrixMedian is None:
                    replicat.computeDataForFeature(feature)
                if mean_tmp is None or median_tmp is None:
                    mean_tmp = np.zeros(replicat.DataMatrixMean.shape)
                    median_tmp = np.zeros(replicat.DataMatrixMedian.shape)
                mean_tmp = mean_tmp + replicat.DataMatrixMean
                median_tmp = median_tmp + replicat.DataMatrixMedian
                i += 1
            self.DataMatrixMean = mean_tmp / i
            self.DataMatrixMedian = median_tmp / i
        except Exception as e:
            print(e)

    def WellCorrection(self, feature, zscore=True, log=True):
        '''
        Apply Well correction on all replicat data
        :param feature: feature to normalize
        :param zscore: Performed zscore Transformation
        :param log:  Performed log2 Transformation
        '''
        try:
            for key, value in self.replicat.items():
                value.WellCorrection(feature=feature, zscore=zscore, log=log)
            self.isNormalized = True
        except Exception as e:
            print(e)

    def SpatialNormalization(self, Methods='Bscore', apply_down=False, verbose=False, save=False, max_iterations=100):
        '''
        Apply a spatial normalization for remove edge effect
        Resulting matrix are save in plate object if save = True
        Be careful !! if the replicat data was already be spatial norm, it will degrade data !!
        :param Methods: Bscore, MEA or PMP technics
        :param apply_down: apply strategie to replicat ??
        :param verbose: verbose : output the result ?
        :param save: save: save the residual into self.SpatNormData , default = False
        :param max_iterations: max iterations for all technics
        '''
        try:
            if apply_down:
                for key, value in self.replicat.items():
                    value.SpatialNormalization(Methods=Methods, verbose=verbose, save=save,
                                               max_iterations=max_iterations)
                return

            if Methods == 'Bscore':
                if self.DataMatrixMean is None or self.isSpatialNormalized is True:
                    print(
                        "Compute Mean of replicat first by using computeDataFromReplicat, or data are already spatial Normalized")
                    return 0
                else:
                    ge, ce, re, resid, tbl_org = Statistic.Normalization.MedianPolish(self.DataMatrixMean,
                                                                                      max_iterations=max_iterations,
                                                                                      verbose=verbose)
                    if save:
                        self.SpatNormDataMean = resid
                        self.isSpatialNormalized = True

                if self.DataMatrixMedian is None or self.isSpatialNormalized is True:
                    print(
                        "Compute Median of replicat first by using computeDataMatrixForFeature, or data are already spatial Normalized")
                    return 0
                else:
                    ge, ce, re, resid, tbl_org = Statistic.Normalization.MedianPolish(self.DataMatrixMean,
                                                                                      max_iterations=max_iterations,
                                                                                      verbose=verbose)
                    if save:
                        self.SpatNormDataMedian = resid
                        self.isSpatialNormalized = True
            if Methods == 'PMP':
                if self.DataMatrixMean is None or self.isSpatialNormalized is True:
                    print(
                        "Compute Mean of replicat first by using computeDataForFeature, or data are already spatial Normalized")
                    return 0
                else:
                    resid = Statistic.Normalization.PartialMeanPolish(self.DataMatrixMean,
                                                                      max_iterations=max_iterations)
                    if save:
                        self.SpatNormDataMean = resid
                        self.isSpatialNormalized = True

                if self.DataMatrixMedian is None or self.isSpatialNormalized is True:
                    print(
                        "Compute Median of replicat first by using computeDataForFeature, or data are already spatial Normalized")
                    return 0
                else:
                    resid = Statistic.Normalization.PartialMeanPolish(self.DataMatrixMedian,
                                                                      max_iterations=max_iterations)
                    if save:
                        self.SpatNormDataMedian = resid
                        self.isSpatialNormalized = True

            if Methods == 'MEA':
                if self.DataMatrixMean is None or self.isSpatialNormalized is True:
                    print(
                        "Compute Mean of replicat first by using computeDataForFeature, or data are already spatial Normalized")
                    return 0
                else:
                    resid = Statistic.Normalization.MatrixErrorAmendment(self.DataMatrixMean)
                    if save:
                        self.SpatNormDataMean = resid
                        self.isSpatialNormalized = True

                if self.DataMatrixMedian is None or self.isSpatialNormalized is True:
                    print(
                        "Compute Median of replicat first by using computeDataForFeature, or data are already spatial Normalized")
                    return 0
                else:
                    resid = Statistic.Normalization.MatrixErrorAmendment(self.DataMatrixMedian)
                    if save:
                        self.SpatNormDataMedian = resid
                        self.isSpatialNormalized = True
        except Exception as e:
            print(e)


    def normalizeReplicat(self, zscore=True, log=True):
        '''
        Apply a norm between replicat
        Z score Transformation by default
        :return:
        '''
        try:
            if (self.getNBreplicat()) < 2:
                print('Can\'t apply this normalization because under two replicats, need at least two replicats ')
            else:
                print('Normalization not yet implemented')
                self.NormBetweenRep = True

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


    def __repr__(self):
        '''
        Definition for the representation
        :return:
        '''
        try:
            return (
                "\n Plate : \n" + repr(self.Name) + "\n MetaInfo : \n" + repr(
                    self.MetaInfo) + "\n PlateSetup : \n" + repr(self.PlateSetup) + "\n Array Result :\n" + repr(
                    self.Result) + "\n Replicat List : \n" + repr(self.replicat))
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
                    self.Result) + "\n Replicat List : \n" + repr(self.replicat))
        except Exception as e:
            print(e)
