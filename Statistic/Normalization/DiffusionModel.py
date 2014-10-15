__author__ = 'Arnaud KOPP'

import numpy as np
import sys


class DiffusionModel():
    def __init__(self, array):
        self.Array = array
        self.CoeffDiff = 0.125
        self.Mask = np.zeros
        self.DiffusionMaps = list()  # list of numpy array
        self.DiffusionMapsMeans = list()  # list of numpy array
        self.DiffusionMapsStdev = list()  # list of numpy array

    def DiffusionModel(self, save=False, verbose=True, max_iterations=50):
        try:
            self.GenerateMask()
            self.ComputeDiffusionMaps(max_iterations=max_iterations)
        except Exception as e:
            print(e)

    def GetDiffusion(self, iteration):
        try:
            return self.DiffusionMaps[iteration]
        except Exception as e:
            print(e)

    def GenerateMask(self):
        try:
            self.Mask = np.zeros((self.Array.shape[0] + 2, self.Array.shape[1] + 2))
            for i in range(self.Array.shape[0] + 2):
                self.Mask[i][0] = 1
                self.Mask[i][self.Array.shape[0] + 1] = 1
            for i in range(self.Array.shape[1] + 2):
                self.Mask[0][i] = 1
                self.Mask[self.Array.shape[1] + 1][i] = 1
        except Exception as e:
            print(e)

    def DiffusionLaplacianFunction(self, input, output, Width, Height):
        try:
            for i in range(Height):
                for j in range(Width):
                    if self.Mask[i][j] == 0:
                        output[i][j] = input[i][j] + (input[i + 1][j] + input[i - 1][j] + input[i][j + 1] + input[i][
                            j - 1] - 1 * input[i][j]) * self.CoeffDiff
                    else:
                        output[i][j] = self.Mask[i]

            # Normalize the plate
            LextPlate = list()

            # compute average
            for X in range(self.Array.shape[0]):
                for Y in range(self.Array.shape[1]):
                    LextPlate.append(output[X + 1][Y + 1])

            Average = np.mean(LextPlate)
            Stdev = np.std(LextPlate)

            for X in range(self.Array.shape[0]):
                for Y in range(self.Array.shape[1]):
                    output[X + 1][Y + 1] = (output[X + 1][Y + 1] - Average) / Stdev
        except Exception as e:
            print(e)

    def FindIterationsForBestMatch(self, Plate):
        try:
            BestIter = -1
            Dist = sys.float_info.max
            LextPlate = list()
            TmpPlate = np.zeros(self.Array.shape)

            # compute average
            for X in range(self.Array.shape[0]):
                for Y in range(self.Array.shape[1]):
                    LextPlate.append(Plate[X][Y])

            Average = np.mean(LextPlate)
            Stdev = np.std(LextPlate)

            for X in range(self.Array.shape[0]):
                for Y in range(self.Array.shape[1]):
                    Plate[X][Y] = (Plate[X][Y] - Average) / Stdev

            for iter in range(len(self.DiffusionMaps)):
                CurrentDist = 0
                for X in range(self.Array.shape[0]):
                    for Y in range(self.Array.shape[1]):
                        CurrentDist += np.sqrt((self.DiffusionMaps[iter][X][Y] - TmpPlate[X][Y]) * (
                            self.DiffusionMaps[iter][X][Y] - TmpPlate[X][Y]))
                if CurrentDist < Dist:
                    BestIter = iter
                    Dist = CurrentDist

            return BestIter
        except Exception as e:
            print(e)

    def FindBestShiftMultCoeff(self, inputPlate, IdxDiff):
        try:
            TmpPlate = np.zeros(self.Array.shape)
            ShiftMult = [0] * 2
            MaxDist = sys.float_info.max
            CurrentDist = 0

            MinMultValue = 0
            MaxMultValue = 10
            DeltaMultValue = 1

            MinShiftValue = 0
            MaxShiftValue = 10
            DeltaShiftValue = 1

            for DiffusionInitTemp in range(MinMultValue, MaxMultValue, DeltaMultValue):
                for PlateInitTemp in range(MinShiftValue, MaxShiftValue, DeltaShiftValue):
                    CurrentDist = 0
                    for X in range(self.Array.shape[0]):
                        for Y in range(self.Array.shape[1]):
                            TmpPlate[X][Y] = self.DiffusionMaps[IdxDiff][X][Y] * DiffusionInitTemp + PlateInitTemp
                            CurrentDist += np.sqrt(
                                (TmpPlate[X][Y] - inputPlate[X][Y]) * (TmpPlate[X][Y] - inputPlate[X][Y]))
                    if CurrentDist < MaxDist:
                        MaxDist = CurrentDist
                        ShiftMult[0] = PlateInitTemp
                        ShiftMult[1] = DiffusionInitTemp

            return ShiftMult
        except Exception as e:
            print(e)

    def CorrectThePlate(self, inputPlate, IdxDiff, Shift, MultCoeff):
        try:
            CorrectedPlate = np.zeros(self.Array.shape)

            for X in range(self.Array.shape[0]):
                for Y in range(self.Array.shape[1]):
                    CorrectedPlate[X][Y] = inputPlate[X][Y] / (self.DiffusionMaps[IdxDiff][X][Y] * MultCoeff + Shift)

            return CorrectedPlate
        except Exception as e:
            print(e)

    def ComputeDiffusionMaps(self, max_iterations=50):
        try:
            CurrentMap = np.zeros(self.Array.shape)
            Nextmap = np.zeros(self.Array.shape)
            CurrentMap = self.Mask.copy()
            CurrentMapWithoutBorders0 = np.zeros(self.Array.shape)

            for X in range(self.Array.shape[0]):
                for Y in range(self.Array.shape[1]):
                    CurrentMapWithoutBorders0[X][Y] = CurrentMap[X + 1][Y + 1]

            self.DiffusionMaps.append(CurrentMapWithoutBorders0)

            ValueList = list()

            for i in range(max_iterations):
                self.DiffusionLaplacianFunction(CurrentMap, Nextmap, self.Array.shape[1], self.Array.shape[0])
                ValueList.clear()

                CurrentMapWithoutBorders = np.zeros(self.Array.shape)

                for X in range(self.Array.shape[0]):
                    for Y in range(self.Array.shape[1]):
                        CurrentMapWithoutBorders[X][Y] = Nextmap[X + 1][Y + 1]
                        ValueList.append(CurrentMapWithoutBorders[X][Y])

                self.DiffusionMaps.append(CurrentMapWithoutBorders)
                self.DiffusionMapsMeans.append(np.mean(ValueList))
                self.DiffusionMapsStdev.append(np.mean(ValueList))
                CurrentMap = Nextmap.copy()
        except Exception as e:
            print(e)