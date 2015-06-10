# coding=utf-8
"""
The majority of of the spatial effect are caused by uneven temperature gradients across assay plates due to inefficient
incubation conditions. To predict the amount of evaporation in each well in a time and space dependent manner, and its
effect on the resulting data set, a diffusion-state model was developed. This method can ve generated based on the data
from single control col in stead of sample wells. The edge effect correction is then applied to each plate in the
screening run based on the generated model.
"""

import numpy as np
import sys
import logging
log = logging.getLogger(__name__)

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "GPLv3"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"


def diffusion_model(array, max_iterations=100, verbose=False):
    """
    Performed the DiffusionModel Process
    :param array: numpy array represente matrix to normalize
    :param max_iterations: max iterations in process
    :param verbose: print result
    :return: result array
    """

    edge_effect = DiffusionModel(array.copy())
    edge_effect.diffusion_model(max_iterations=max_iterations)
    best_iteration = edge_effect.find_iterations_for_best_match(array.copy())
    shift_mult = edge_effect.find_best_shift_mult_coeff(array.copy(), best_iteration)

    if not best_iteration == 0:
        corrected_table = edge_effect.correct_the_plate(array.copy(), best_iteration, shift_mult[0], shift_mult[1])
    else:
        corrected_table = array.copy()

    if verbose:
        print("DiffusionModel methods for removing systematics error")
        print("Diffusion Iteration :", best_iteration)
        print("Diffusion Shift :", shift_mult[0])
        print("Diffusion multiplicative coeff: ", shift_mult[1])
        print("-----Normalized Table-------")
        print(corrected_table)
        print("-----Original Table-------")
        print(array)
        print("")

    return corrected_table


class DiffusionModel(object):
    """
    Class that represent the Diffusion Model

    self.Array = array
    self.CoeffDiff = 0.125
    self.Mask = np.zeros
    self.DiffusionMaps = list()  # list of numpy array
    self.DiffusionMapsMeans = list()  # list of numpy array
    self.DiffusionMapsStdev = list()  # list of numpy array
    """

    def __init__(self, array):
        self.Array = array
        self.CoeffDiff = 0.125
        self.Mask = np.zeros
        self.DiffusionMaps = list()
        self.DiffusionMapsMeans = list()
        self.DiffusionMapsStdev = list()

    def diffusion_model(self, max_iterations=50):
        """

        :param max_iterations:
        :return:
        """
        try:
            self.generate_mask()
            self.compute_diffusion_maps(max_iterations=max_iterations)
        except Exception as e:
            print(e)

    def get_diffusion(self, iteration):
        """

        :param iteration:
        :return:
        """
        try:
            return self.DiffusionMaps[iteration]
        except Exception as e:
            print(e)

    def generate_mask(self):
        """

        :return:
        """
        try:
            self.Mask = np.zeros((self.Array.shape[0] + 2, self.Array.shape[1] + 2))
            for i in range(self.Array.shape[0] + 2):
                self.Mask[i][0] = 1
                self.Mask[i][self.Array.shape[1] + 1] = 1
            for j in range(self.Array.shape[1] + 2):
                self.Mask[0][j] = 1
                self.Mask[self.Array.shape[0] + 1][j] = 1
        except Exception as e:
            print(e)

    def diffusion_laplacian_function(self, input_arr, output, width, height):
        """

        :param input_arr:
        :param output:
        :param width:
        :param height:
        :return:
        """
        try:
            for i in range(height):
                for j in range(width):
                    if self.Mask[i][j] == 0:
                        output[i][j] = input_arr[i][j] + (input_arr[i + 1][j] + input_arr[i - 1][j] +
                                                          input_arr[i][j + 1] + input_arr[i][
                            j - 1] - 1 * input_arr[i][j]) * self.CoeffDiff
                    else:
                        output[i][j] = self.Mask[i][j]
            # Normalize the plate
            lext_plate = list()

            # compute average
            for X in range(self.Array.shape[0]):
                for Y in range(self.Array.shape[1]):
                    lext_plate.append(output[X + 1][Y + 1])

            average = np.nanmean(lext_plate)
            stdev = np.nanstd(lext_plate)

            for X in range(self.Array.shape[0]):
                for Y in range(self.Array.shape[1]):
                    output[X + 1][Y + 1] = (output[X + 1][Y + 1] - average) / stdev

            return output
        except Exception as e:
            print(e)

    def find_iterations_for_best_match(self, plate):
        """

        :param plate:
        :return:
        """
        try:
            bestiter = -1
            dist = sys.float_info.max
            lextplate = list()
            tmpplate = np.zeros(self.Array.shape)

            # compute average
            for X in range(self.Array.shape[0]):
                for Y in range(self.Array.shape[1]):
                    lextplate.append(plate[X][Y])

            average = np.nanmean(lextplate)
            stdev = np.nanstd(lextplate)

            for X in range(self.Array.shape[0]):
                for Y in range(self.Array.shape[1]):
                    tmpplate[X][Y] = (plate[X][Y] - average) / stdev

            for iteration in range(len(self.DiffusionMaps)):
                currentdist = 0
                for X in range(self.Array.shape[0]):
                    for Y in range(self.Array.shape[1]):
                        currentdist = np.sqrt((self.DiffusionMaps[iteration][X][Y] - tmpplate[X][Y]) * (
                            self.DiffusionMaps[iteration][X][Y] - tmpplate[X][Y]))
                if currentdist < dist:
                    bestiter = iteration
                    dist = currentdist
            return bestiter
        except Exception as e:
            print(e)

    def find_best_shift_mult_coeff(self, input_plate, idxdiff):
        """

        :param input_plate:
        :param idxdiff:
        :return:
        """
        try:
            tmpplate = np.zeros(self.Array.shape)
            shiftmult = [0] * 2
            maxdist = sys.float_info.max
            currentdist = 0

            minmultvalue = 0  # -2147483648 < X < 466537709
            maxmultvalue = 1000  # -2147483648 < X < 466537709
            deltamultvalue = 10  # -2147483648 < X < 466537709

            minshiftvalue = 0  # -2147483648 < X < 466537709
            maxshiftvalue = 1000  # -2147483648 < X < 466537709
            deltashiftvalue = 10  # -2147483648 < X < 466537709

            for DiffusionInitTemp in range(minmultvalue, maxmultvalue, deltamultvalue):
                for PlateInitTemp in range(minshiftvalue, maxshiftvalue, deltashiftvalue):
                    currentdist = 0
                    for X in range(self.Array.shape[0]):
                        for Y in range(self.Array.shape[1]):
                            tmpplate[X][Y] = self.DiffusionMaps[idxdiff][X][Y] * DiffusionInitTemp + PlateInitTemp
                            currentdist += np.sqrt(
                                (tmpplate[X][Y] - input_plate[X][Y]) * (tmpplate[X][Y] - input_plate[X][Y]))
                    if currentdist < maxdist:
                        maxdist = currentdist
                        shiftmult[0] = PlateInitTemp
                        shiftmult[1] = DiffusionInitTemp

            return shiftmult
        except Exception as e:
            print(e)

    def correct_the_plate(self, input_plate, idxdiff, shift, multcoeff):
        """

        :param input_plate:
        :param idxdiff:
        :param shift:
        :param multcoeff:
        :return:
        """
        try:
            corrected_plate = np.zeros(self.Array.shape)
            for X in range(self.Array.shape[0]):
                for Y in range(self.Array.shape[1]):
                    corrected_plate[X][Y] = input_plate[X][Y] / (self.DiffusionMaps[idxdiff][X][Y] * multcoeff + shift)
            return corrected_plate
        except Exception as e:
            print(e)

    def compute_diffusion_maps(self, max_iterations=100):
        """

        :param max_iterations:
        :return:
        """
        try:
            currentmap = np.zeros((self.Array.shape[0] + 2, self.Array.shape[1] + 2))
            nextmap = np.zeros((self.Array.shape[0] + 2, self.Array.shape[1] + 2))
            currentmapwithoutborders0 = np.zeros(self.Array.shape)

            currentmap = self.Mask.copy()

            for X in range(self.Array.shape[0]):
                for Y in range(self.Array.shape[1]):
                    currentmapwithoutborders0[X][Y] = currentmap[X + 1][Y + 1]

            self.DiffusionMaps.append(currentmapwithoutborders0)

            valuelist = list()

            for i in range(max_iterations):
                nextmap = self.diffusion_laplacian_function(currentmap, nextmap, self.Array.shape[1] + 2,
                                                            self.Array.shape[0] + 2)
                valuelist.clear()

                currentmapwithoutborders = np.zeros(self.Array.shape)

                for X in range(self.Array.shape[0]):
                    for Y in range(self.Array.shape[1]):
                        currentmapwithoutborders[X][Y] = nextmap[X + 1][Y + 1]
                        valuelist.append(currentmapwithoutborders[X][Y])

                self.DiffusionMaps.append(currentmapwithoutborders)
                self.DiffusionMapsMeans.append(np.nanmean(valuelist))
                self.DiffusionMapsStdev.append(np.nanmean(valuelist))
                currentmap = nextmap.copy()
        except Exception as e:
            print(e)