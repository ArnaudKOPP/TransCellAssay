__author__ = 'Arnaud KOPP'

import TCA.PlateSetup
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
        self.replicat = list()
        self.MetaInfo = dict()
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

        :return:
        '''
        try:
            print(self.Name)
        except Exception as e:
            print(e)

    def setName(self, name):
        '''

        :param name:
        :return:
        '''
        try:
            self.Name = name
        except Exception as e:
            print(e)

    def getName(self):
        '''

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
        for item in self.replicat:
            item.printInfo()

    def addReplicat(self, replicat):
        '''
        Add replicat to plate
        :param replicat: Give a replicat object
        :param name:  Give a name for added replicat object
        :return: nothing
        '''
        try:
            assert isinstance(replicat, object)
            self.replicat.append(replicat)
        except Exception as e:
            print(e)

    def getNumReplicat(self):
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
        Add Info
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
        :return: infor (dict)
        '''
        try:
            return self.MetaInfo
        except Exception as e:
            print(e)
            print('Error in getting info')

    def getAllDataFromReplicat(self, features):
        '''
        Return a dataframe with data of all dataframe
        :return:
        '''
        data = pd.DataFrame()
        try:
            for rep in self.replicat:
                tmp = rep.getDataByFeatures(features)
                data.join(data, tmp)
            return data
        except Exception as e:
            print(e)
            print('Error in getAllDataFromReplicat')


    def addPS(self, platesetup):
        '''
        Add the platesetup to the plate
        :param platesetup:
        :return:
        '''
        try :
            # TODO
            return 0
        except Exception as e:
            print(e)


    def getPS(self):
        '''
        Get the platesetup from the plate
        :return: plateSetup
        '''
        try:
            # TODO
            return 0
        except Exception as e:
            print(e)

    def getResult(self):
        '''

        :return:
        '''
        try:
            return 0
        # TODO
        except Exception as e:
            print(e)