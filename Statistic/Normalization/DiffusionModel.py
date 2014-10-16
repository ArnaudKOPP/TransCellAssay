__author__ = 'Arnaud KOPP'

import numpy as np
import sys


def diffusionModel(Array, max_iterations=100, verbose=False):
    '''
    Performed the DiffusionModel Process
    :param Array: numpy array represente matrix to normalize
    :param max_iterations: max iterations in process
    :param verbose: print result
    :return: result array
    '''
    EdgeEffect = DiffusionModel(Array.copy())
    EdgeEffect.DiffusionModel(max_iterations=max_iterations)
    BestIteration = EdgeEffect.FindIterationsForBestMatch(Array.copy())
    ShiftMult = EdgeEffect.FindBestShiftMultCoeff(Array.copy(), BestIteration)
    CorrectedTable = None
    # Correct the plate
    if not BestIteration == 0:
        CorrectedTable = EdgeEffect.CorrectThePlate(Array.copy(), BestIteration, ShiftMult[0], ShiftMult[1])

    if verbose:
        np.set_printoptions(suppress=True)
        print("DiffusionModel methods for removing systematics error")
        print("Diffusion Iteration :", BestIteration)
        print("Diffusion Shift :", ShiftMult[0])
        print("Diffusion multiplicative coeff: ", ShiftMult[1])
        print("-----Normalized Table-------")
        print(CorrectedTable)
        print("-----Original Table-------")
        print(Array)
        print("")

    return CorrectedTable


class DiffusionModel():
    '''
    Class that represent the Diffusion Model
    '''
    def __init__(self, array):
        self.Array = array
        self.CoeffDiff = 0.125
        self.Mask = np.zeros
        self.DiffusionMaps = list()  # list of numpy array
        self.DiffusionMapsMeans = list()  # list of numpy array
        self.DiffusionMapsStdev = list()  # list of numpy array

    def DiffusionModel(self, max_iterations=50):
        try:
            self.GenerateMask()
            self.ComputeDiffusionMaps(max_iterations=max_iterations)
        except Exception as e:
            print("DiffusionModel Method")
            print(e)

    def GetDiffusion(self, iteration):
        try:
            return self.DiffusionMaps[iteration]
        except Exception as e:
            print("GetDiffusion Method")
            print(e)

    def GenerateMask(self):
        try:
            self.Mask = np.zeros((self.Array.shape[0] + 2, self.Array.shape[1] + 2))
            for i in range(self.Array.shape[0] + 2):
                self.Mask[i][0] = 1
                self.Mask[i][self.Array.shape[1] + 1] = 1
            for j in range(self.Array.shape[1] + 2):
                self.Mask[0][j] = 1
                self.Mask[self.Array.shape[0] + 1][j] = 1
        except Exception as e:
            print("GenerateMask Method")
            print(e)

    def DiffusionLaplacianFunction(self, input, output, Width, Height):
        try:
            for i in range(Height):
                for j in range(Width):
                    if self.Mask[i][j] == 0:
                        output[i][j] = input[i][j] + (input[i + 1][j] + input[i - 1][j] + input[i][j + 1] + input[i][
                            j - 1] - 1 * input[i][j]) * self.CoeffDiff
                    else:
                        output[i][j] = self.Mask[i][j]
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

            return output
        except Exception as e:
            print("DiffusionLaplacianFunction Method")
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
                    TmpPlate[X][Y] = (Plate[X][Y] - Average) / Stdev

            for iter in range(len(self.DiffusionMaps)):
                CurrentDist = 0
                for X in range(self.Array.shape[0]):
                    for Y in range(self.Array.shape[1]):
                        CurrentDist = np.sqrt((self.DiffusionMaps[iter][X][Y] - TmpPlate[X][Y]) * (
                            self.DiffusionMaps[iter][X][Y] - TmpPlate[X][Y]))
                if CurrentDist < Dist:
                    BestIter = iter
                    Dist = CurrentDist
            return BestIter
        except Exception as e:
            print("FindIterationsForBestMatch Methods")
            print(e)

    def FindBestShiftMultCoeff(self, inputPlate, IdxDiff):
        try:
            TmpPlate = np.zeros(self.Array.shape)
            ShiftMult = [0] * 2
            MaxDist = sys.float_info.max
            CurrentDist = 0

            MinMultValue = 0  # -2147483648 < X < 466537709
            MaxMultValue = 1000  # -2147483648 < X < 466537709
            DeltaMultValue = 10  # -2147483648 < X < 466537709

            MinShiftValue = 0  # -2147483648 < X < 466537709
            MaxShiftValue = 1000  # -2147483648 < X < 466537709
            DeltaShiftValue = 10  # -2147483648 < X < 466537709

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
            print("FindBestShiftMultCoeff Method")
            print(e)

    def CorrectThePlate(self, inputPlate, IdxDiff, Shift, MultCoeff):
        try:
            CorrectedPlate = np.zeros(self.Array.shape)
            print("Hello")
            for X in range(self.Array.shape[0]):
                for Y in range(self.Array.shape[1]):
                    CorrectedPlate[X][Y] = inputPlate[X][Y] / (self.DiffusionMaps[IdxDiff][X][Y] * MultCoeff + Shift)
            return CorrectedPlate
        except Exception as e:
            print("CorrectThePlate Method")
            print(e)

    def ComputeDiffusionMaps(self, max_iterations=100):
        try:
            CurrentMap = np.zeros((self.Array.shape[0] + 2, self.Array.shape[1] + 2))
            Nextmap = np.zeros((self.Array.shape[0] + 2, self.Array.shape[1] + 2))
            CurrentMapWithoutBorders0 = np.zeros(self.Array.shape)

            CurrentMap = self.Mask.copy()

            for X in range(self.Array.shape[0]):
                for Y in range(self.Array.shape[1]):
                    CurrentMapWithoutBorders0[X][Y] = CurrentMap[X + 1][Y + 1]

            self.DiffusionMaps.append(CurrentMapWithoutBorders0)

            ValueList = list()

            for i in range(max_iterations):
                Nextmap = self.DiffusionLaplacianFunction(CurrentMap, Nextmap, self.Array.shape[1] + 2,
                                                          self.Array.shape[0] + 2)
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
            print("ComputeDiffusionMaps Method")
            print(e)