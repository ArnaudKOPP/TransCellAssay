__author__ = 'Arnaud KOPP'

'''

'''
import TCA.PlateSetup

class Plate():
    def __init__(self,):
        '''
        Constructor
        :return: nothing
        '''
        self.replicat = dict()
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
        for keys, values in self.replicat.items():
            print(keys)

    def addreplicat(self, name, replicat):
        '''
        Add replicat to plate
        :param replicat: Give a replicat object
        :param name:  Give a name for added replicat object
        :return: nothing
        '''
        try:
            self.replicat[name] = replicat
        except Exception as e:
            print(e)


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

    def getreplicat(self):
        return 0

    def getinfo(self):
        return 0