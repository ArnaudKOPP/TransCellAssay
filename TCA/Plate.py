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
        self.plate = TCA.PlateSetup()


    def printmetainfo(self):
        '''
        Print MetaInfo for Plate object
        :return: print some output
        '''
        for keys, values in self.MetaInfo.items():
            print(keys, values)

    def printreplicat(self):
        '''
        Print replicat list
        :return: print replicat list
        '''
        for item in self.replicat:
            item.printinfo()

    def addreplicat(self, replicat):
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

    def getNBreplicat(self):
        '''
        return number of replicat
        :return: int
        '''
        try:
            return len(self.replicat)
        except Exception as e:
            print(e)
            print('Error in getting number of replicat')

    def addinfo(self, key, value):
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


    def getinfo(self):
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
        try :
            for rep in self.replicat:
                tmp  = rep.getDataByFeatures(features)
                data.join(data, tmp)
            return data
        except Exception as e:
            print(e)
            print('Error in getAllDataFromReplicat')