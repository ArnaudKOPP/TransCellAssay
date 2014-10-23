__author__ = 'Arnaud KOPP'
"""
In this correction method, the background signal corresponding to each well is calculated by averaging the activities
withing each well across all plate of screen.
Then, a kriging interpolation can be made but not sur for the moment.
We substract then the calculated background to value from plate or replicat.
"""

import ScreenPlateReplicatPS
import numpy as np


class BackgroundCorrection():
    def __init__(self, Screen):
        if isinstance(Screen, ScreenPlateReplicatPS.Screen):
            self.screen = Screen
            self.BackgroundModelMean = None
            self.BackgroundModelMedian = None
        else:
            raise TypeError

    def BackgroundCorrection(self, apply="Plate", verbose=False):
        try:
            self.BackgroundEvaluation(apply_on=apply, verbose=verbose)
            self.BackgroundSurfaceAnalysis()
            self.ApplyBackgroundElimination()
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def BackgroundEvaluation(self, apply_on, verbose, control_Well=None):
        try:
            if apply_on == "Plate":
                # iterate on all plate
                for key, value in self.screen.PlateList.items():
                    # check if plate object
                    if not isinstance(value, ScreenPlateReplicatPS.Plate):
                        raise TypeError
                    else:
                        if self.BackgroundModelMean is None:
                            self.BackgroundModelMean = np.zeros(value.DataMean.shape)
                        if self.BackgroundModelMedian is None:
                            self.BackgroundModelMedian = np.zeros(value.DataMedian.shape)
                        self.BackgroundModelMean += value.DataMean
                        self.BackgroundModelMedian += value.DataMedian
                self.BackgroundModelMedian *= 1 / len(self.screen)
                self.BackgroundModelMean *= 1 / len(self.screen)
            elif apply_on == "Replicat":
                objectCnt = 0
                # iterate on all plate
                for key, value in self.screen.PlateList.items():
                    # check if plate object
                    if not isinstance(value, ScreenPlateReplicatPS.Plate):
                        raise TypeError
                    else:
                        # iterate on all replicat in the plate
                        for repName, repValue in value.replicat.items():
                            if not isinstance(repValue, ScreenPlateReplicatPS.Replicat):
                                raise TypeError
                            else:
                                if self.BackgroundModelMean is None:
                                    self.BackgroundModelMean = np.zeros(repValue.DataMean.shape)
                                if self.BackgroundModelMedian is None:
                                    self.BackgroundModelMedian = np.zeros(repValue.DataMedian.shape)
                                self.BackgroundModelMean += repValue.DataMean
                                self.BackgroundModelMedian += repValue.DataMedian
                                objectCnt += 1
                self.BackgroundModelMedian *= 1 / objectCnt
                self.BackgroundModelMean *= 1 / objectCnt
                if verbose:
                    np.set_printoptions(suppress=True)
                    print("Background Evaluation table (Median) :")
                    print("Apply strategy was : ", apply_on)
                    print(self.BackgroundModelMedian)
                    print("")
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def BackgroundSurfaceAnalysis(self, plot=False):
        try:
            return 0
        except Exception as e:
            print(e)

    def ApplyBackgroundElimination(self, apply_on, control_Well=None):
        try:
            if apply_on == "Plate":
                # iterate on all plate
                for key, value in self.screen.PlateList.items():
                    # check if plate object
                    if not isinstance(value, ScreenPlateReplicatPS.Plate):
                        raise TypeError
                    else:
                        value.DataMean -= self.BackgroundModelMean
                        value.DataMedian -= self.BackgroundModelMedian
            elif apply_on == "Replicat":
                # iterate on all plate
                for key, value in self.screen.PlateList.items():
                    # check if plate object
                    if not isinstance(value, ScreenPlateReplicatPS.Plate):
                        raise TypeError
                    else:
                        # iterate on all replicat in the plate
                        for repName, repValue in value.replicat.items():
                            if not isinstance(repValue, ScreenPlateReplicatPS.Replicat):
                                raise TypeError
                            else:
                                value.DataMean -= self.BackgroundModelMean
                                value.DataMedian -= self.BackgroundModelMedian
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)