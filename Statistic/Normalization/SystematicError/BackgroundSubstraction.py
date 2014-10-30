"""
Substract a determined background of the screen/plate/replicat
Analogous to BackgroundCorrection but here it's a determined background that we provided
"""

import SOM

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


class BackgroundSubstraction():
    def __init__(self, background):
        try:
            self.background = background
        except Exception as e:
            print(e)

    def BackgroundSubstraction(self, Screen):
        try:
            if isinstance(Screen, SOM.Screen):
                self._process(Screen)
            else:
                raise AttributeError("\033[0;31m[ERROR]\033[0m  Must provied Screen Object")
        except Exception as e:
            print(e)

    def _process(self, Screen):
        try:
            # iterate on all plate
            for key, value in Screen.PlateList.items():
                # iterate on all replicat in the plate
                for repName, repValue in value.replicat.items():
                    repValue.SECDataMean = repValue.DataMean - self.background
                    repValue.SECDataMedian = repValue.DataMedian - self.background
                    repValue.isSpatialNormalized = True
        except Exception as e:
            print(e)