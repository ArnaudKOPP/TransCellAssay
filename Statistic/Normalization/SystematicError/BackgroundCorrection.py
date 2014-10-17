__author__ = 'Arnaud KOPP'
"""
In this correction method, the background signal corresponding to each well is calculated by averaging the activities
withing each well across all plate of screen. Then, a kriging interpolation is made.
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
            print(e)

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
                            self.BackgroundModelMean = np.zeros(value.DataMatrixMean.shape)
                        if self.BackgroundModelMedian is None:
                            self.BackgroundModelMedian = np.zeros(value.DataMatrixMedian.shape)
                        self.BackgroundModelMean += value.DataMatrixMean
                        self.BackgroundModelMedian += value.DataMatrixMedian
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
                                    self.BackgroundModelMean = np.zeros(repValue.DataMatrixMean.shape)
                                if self.BackgroundModelMedian is None:
                                    self.BackgroundModelMedian = np.zeros(repValue.DataMatrixMedian.shape)
                                self.BackgroundModelMean += repValue.DataMatrixMean
                                self.BackgroundModelMedian += repValue.DataMatrixMedian
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
            print(e)

    def BackgroundSurfaceAnalysis(self, plot=False):
        try:
            return 0
        except Exception as e:
            print(e)

    def ApplyBackgroundElimination(self):
        try:
            return 0
        except Exception as e:
            print(e)