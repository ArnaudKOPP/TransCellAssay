"""
Screen is designed for manipulating screen that contain multiple different plate
"""

import SOM.Plate

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


class Screen():
    """
    Class that defined a screen, and contain several plate
    """

    def __init__(self):
        """
        Constructor
        self.PlateList = {} # dict that contain all plate
        self.Info = {} # Dict that contain info
        self.type = None # type of screen : siRNA or compounds
        self.Threshold = None  # Threeshold for considering Cell as positive
        self.Neg = None # Negative reference for the screen
        self.Pos = None # Positive reference for the screen
        self.Tox = None  # Toxicity reference for the screen
        self.shape = (8, 12) # Default shape of plate
        """
        self.PlateList = {}
        self.Info = {}
        self.type = None
        self.Threshold = None
        self.Neg = None
        self.Pos = None
        self.Tox = None
        self.shape = (8, 12)

    def addPlate(self, plate):
        """
        Add plate to the screen
        :param plate: input plate
        """
        try:
            assert isinstance(plate, SOM.Plate)
            self.PlateList[plate.Name] = plate
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def getPlate(self, name):
        """
        Return Plate specified by name
        :return: plate
        """
        try:
            return self.PlateList[name]
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

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
            print("\033[0;31m[ERROR]\033[0m", e)

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
            assert isinstance(plate, SOM.Plate)
            self.PlateList[plate.Name] = plate
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

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
                    "\n Tox Control \n" + repr(self.Tox) + "\n")
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
                    "\n Tox Control \n" + repr(self.Tox) + "\n")
        except Exception as e:
            print(e)