"""
In this correction method, the background signal corresponding to each well is calculated by averaging the activities
withing each well across all plate of screen.
Then, a kriging interpolation can be made but not sur for the moment.
We substract then the calculated background to value from plate or replicat.
"""

import numpy as np

from TransCellAssay import Core


__author__ = "Arnaud KOPP"
__copyright__ = "© 2014 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


class BackgroundCorrection():
    def __init__(self, Screen):
        if isinstance(Screen, Core.Screen):
            self.screen = Screen
            self.BackgroundModel = None
            self.BackgroundModelMean = None
        else:
            raise TypeError("\033[0;31m[ERROR]\033[0m Provided Screen Object Object")

    def background_correction(self, apply="Plate", verbose=False):
        try:
            self.background_evaluation(apply_on=apply, verbose=verbose)
            self.background_surface_analysis()
            self.apply_background_elimination()
        except Exception as e:
            print(e)

    def background_evaluation(self, apply_on, verbose, control_well=None):
        try:
            if apply_on == "Plate":
                # iterate on all plate
                for key, value in self.screen.allPlate.items():
                    # check if plate object
                    if not isinstance(value, Core.Plate):
                        raise TypeError("\033[0;31m[ERROR]\033[0m Must provided good object")
                    else:
                        if self.BackgroundModel is None:
                            self.BackgroundModel = np.zeros(value.Data.shape)
                        self.BackgroundModel += value.Data
                self.BackgroundModel *= 1 / len(self.screen)
            elif apply_on == "Replicat":
                object_cnt = 0
                # iterate on all plate
                for key, value in self.screen.allPlate.items():
                    # check if plate object
                    if not isinstance(value, Core.Plate):
                        raise TypeError("\033[0;31m[ERROR]\033[0m Must provided good object")
                    else:
                        # iterate on all replicat in the plate
                        for repName, repValue in value.replicat.items():
                            if not isinstance(repValue, Core.Replicat):
                                raise TypeError
                            else:
                                if self.BackgroundModelMean is None:
                                    self.BackgroundModelMean = np.zeros(repValue.Data.shape)
                                self.BackgroundModel += repValue.Data
                                object_cnt += 1
                self.BackgroundModel *= 1 / object_cnt
            else:
                raise AttributeError("\033[0;31m[ERROR]\033[0m Apply strategy only on plate or replicat")
            if verbose:
                np.set_printoptions(suppress=True)
                print("Background Evaluation table (Median) :")
                print("Apply strategy was : ", apply_on)
                print(self.BackgroundModel)
                print("")
        except Exception as e:
            print(e)

    def background_surface_analysis(self, plot=False):
        try:
            return 0
        except Exception as e:
            print(e)

    def apply_background_elimination(self, apply_on, control_well=None):
        try:
            if apply_on == "Plate":
                # iterate on all plate
                for key, value in self.screen.allPlate.items():
                    # check if plate object
                    if not isinstance(value, Core.Plate):
                        raise TypeError("\033[0;31m[ERROR]\033[0m Must provided good object")
                    else:
                        value.SECData -= self.BackgroundModel
                        value.isSpatialNormalized = True
            elif apply_on == "Replicat":
                # iterate on all plate
                for key, value in self.screen.allPlate.items():
                    # check if plate object
                    if not isinstance(value, Core.Plate):
                        raise TypeError("\033[0;31m[ERROR]\033[0m Must provided good object")
                    else:
                        # iterate on all replicat in the plate
                        for repName, repValue in value.replicat.items():
                            if not isinstance(repValue, Core.Replicat):
                                raise TypeError
                            else:
                                value.SECData -= self.BackgroundModel
                                value.isSpatialNormalized = True
            else:
                raise AttributeError("\033[0;31m[ERROR]\033[0m Apply strategy only on plate or replicat")
        except Exception as e:
            print(e)