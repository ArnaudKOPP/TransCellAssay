__author__ = 'Arnaud KOPP'
"""
Plate is designed for manipulating one or more replicat
"""
import TCA.PlateSetup
import TCA.Replicat
import Math.Result
import pandas as pd


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
        self.IsSingleCell = True  # If Single Cell data, default is True because design for this data
        self.Result = None

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

    def printName(self):
        '''
        Print Name of plate
        :return:
        '''
        try:
            print(self.Name)
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

    def printReplicat(self):
        '''
        Print replicat list
        :return: print replicat list
        '''
        try:
            for item in self.replicat:
                print(item)
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
        Return a dict with data of all dataframe
        :return:
        '''
        data = {}
        try:
            # TODO don't work, only on first iteration
            for rep in self.replicat:
                repTmp = self.replicat[rep]
                tmp = repTmp.getDataByFeatures(features)
                data[repTmp.getInfo()] = tmp
            return data
        except Exception as e:
            print(e)
            print('Error in getAllDataFromReplicat')


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
            assert isinstance(result, Math.Result)
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