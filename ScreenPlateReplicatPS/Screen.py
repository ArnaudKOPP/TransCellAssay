__author__ = 'Arnaud KOPP'
"""
Screen is designed for manipulating screen that contain multiple different plate
"""
import ScreenPlateReplicatPS.Plate


class Screen():
    '''
    Class that defined a screen, and contain several plate
    '''

    def __init__(self):
        '''
        Constructor
        :return:
        '''
        self.PlateList = {}
        self.Info = {}
        self.Threshold = None  # Threeshold for considering Cell as positive
        self.Neg = None
        self.Pos = None
        self.Tox = None

    def addPlate(self, plate):
        '''
        Add plate to the screen
        :param plate: input plate
        :return:
        '''
        try:
            assert isinstance(plate, ScreenPlateReplicatPS.Plate)
            self.PlateList[plate.Name] = plate
        except Exception as e:
            print(e)
            print('Can\'t insert this plate in screen instance' % plate)

    def getPlate(self, name):
        '''
        Return Plate specified by name
        :return: plate
        '''
        try:
            return self.PlateList[name]
        except Exception as e:
            print(e)
            print('Can\'t get this plate one %s' % name)

    def addInfo(self, key, value):
        '''
        Add Info
        :param key:
        :param value:
        :return: nothing
        '''
        try:
            self.Info.pop(key, value)
        except Exception as e:
            print(e)

    def getInfo(self):
        '''
        Get info
        :return: infor (dict)
        '''
        try:
            return self.Info
        except Exception as e:
            print(e)
            print('Error in getting info')


    def __add__(self, plate):
        '''
        Add plate to the screen
        :param plate: input plate
        :return:
        '''
        try:
            assert isinstance(plate, ScreenPlateReplicatPS.Plate)
            self.PlateList[plate.Name] = plate
        except Exception as e:
            print(e)
            print('Can\'t insert this plate in screen instance' % plate)


    def __getitem__(self, key):
        '''
        get plate object
        :param key:
        :return:
        '''
        try:
            return self.PlateList[key]
        except Exception as e:
            print(e)

    def __repr__(self):
        '''
        Definition for the representation
        :return:
        '''
        try:
            return ("\n SCREEN OBJECT :\n" + "\n Threshold : \n" + repr(
                self.Threshold) + "\n Neg Control \n" + repr(self.Neg) + "\n Pos Control \n" + repr(
                self.Pos) + "\n Tox Control \n" + repr(self.Tox))
        except Exception as e:
            print(e)

    def __str__(self):
        '''
        Definition for the print
        :return:
        '''
        try:
            return ("\n SCREEN OBJECT :\n" + "\n Threshold : \n" + repr(
                self.Threshold) + "\n Neg Control \n" + repr(self.Neg) + "\n Pos Control \n" + repr(
                self.Pos) + "\n Tox Control \n" + repr(self.Tox))
        except Exception as e:
            print(e)

