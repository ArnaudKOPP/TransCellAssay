__author__ = 'Arnaud KOPP'
"""
Screen is designed for manipulating screen that contain multiple different plate
"""
import ScreenPlateReplicatPS.Plate


class Screen():
    """
    Class that defined a screen, and contain several plate
    """

    def __init__(self):
        """
        Constructor
        self.PlateList = {} # dict that contain all plate
        self.Info = {} # Dict that contain info
        self.Threshold = None  # Threeshold for considering Cell as positive
        self.Neg = None # Negative reference for the screen
        self.Pos = None # Positive reference for the screen
        self.Tox = None  # Toxicity reference for the screen
        """
        self.PlateList = {}
        self.Info = {}
        self.Threshold = None  # Threeshold for considering Cell as positive
        self.Neg = None
        self.Pos = None
        self.Tox = None

    def addPlate(self, plate):
        """
        Add plate to the screen
        :param plate: input plate
        """
        try:
            assert isinstance(plate, ScreenPlateReplicatPS.Plate)
            self.PlateList[plate.Name] = plate
        except Exception as e:
            print(e)
            print('\033[0;31m[ERROR]\033[0m  Can\'t insert this plate in screen instance' % plate)

    def getPlate(self, name):
        """
        Return Plate specified by name
        :return: plate
        """
        try:
            return self.PlateList[name]
        except Exception as e:
            print(e)
            print('\033[0;31m[ERROR]\033[0m  Can\'t get this plate one %s' % name)

    def addInfo(self, key, value):
        """
        Add Info
        :param key:
        :param value:
        """
        try:
            self.Info.pop(key, value)
        except Exception as e:
            print(e)

    def getInfo(self):
        """
        Get info with desired key
        :return: info (dict)
        """
        try:
            return self.Info
        except Exception as e:
            print(e)
            print('\033[0;31m[ERROR]\033[0m  Error in getting info')

    def __len__(self):
        """
        get number of plate
        :return: int
        """
        try:
            return len(self.PlateList)
        except Exception as e:
            print(e)

    def __add__(self, plate):
        """
        Add plate to the screen
        :param plate: input plate
        """
        try:
            assert isinstance(plate, ScreenPlateReplicatPS.Plate)
            self.PlateList[plate.Name] = plate
        except Exception as e:
            print(e)
            print('\033[0;31m[ERROR]\033[0m  Can\'t insert this plate in screen instance' % plate)

    def __getitem__(self, key):
        """
        get plate object
        :param key:
        :return: return plate
        """
        try:
            return self.PlateList[key]
        except Exception as e:
            print(e)

    def __repr__(self):
        """
        Definition for the representation
        """
        try:
            return ("\n SCREEN OBJECT :\n" +
                    "\n Threshold : \n" + repr(self.Threshold) +
                    "\n Neg Control \n" + repr(self.Neg) +
                    "\n Pos Control \n" + repr(self.Pos) +
                    "\n Tox Control \n" + repr(self.Tox))
        except Exception as e:
            print(e)

    def __str__(self):
        """
        Definition for the print
        """
        try:
            return ("\n SCREEN OBJECT :\n" +
                    "\n Threshold : \n" + repr(self.Threshold) +
                    "\n Neg Control \n" + repr(self.Neg) +
                    "\n Pos Control \n" + repr(self.Pos) +
                    "\n Tox Control \n" + repr(self.Tox))
        except Exception as e:
            print(e)