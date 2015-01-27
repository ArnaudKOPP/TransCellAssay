# coding=utf-8
"""
In this correction method, the background signal corresponding to each well is calculated by averaging the activities
withing each well across all plate of screen.
Then, a kriging interpolation can be made but not sur for the moment.
We substract then the calculated background to value from plate or replicat.
"""

import numpy as np
import TransCellAssay as TCA


__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


class BackgroundCorrection():
    """

    :param args:
    :raise NotImplementedError:
    """

    def __init__(self, *args):
        self.BackgroundModel = None
        self.BackgroundModelMean = None
        try:
            self.screen = []
            for arg in args:
                if isinstance(arg, TCA.Plate):
                    self.screen.append(arg)
                elif isinstance(arg, list):
                    for elem in arg:
                        if isinstance(elem, TCA.Plate):
                            self.screen.append(elem)
                        else:
                            raise TypeError('Accept only list of Plate element')
                else:
                    raise TypeError('Accept only plate or list of plate')
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def background_correction(self, apply="Plate", verbose=False):
        """

        :param apply:
        :param verbose:
        """
        try:
            self.__background_evaluation(apply_on=apply, verbose=verbose)
            self.__background_surface_analysis()
            self.__apply_background_elimination()
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def __background_evaluation(self, apply_on='Plate', verbose=False, control_well=None):
        """

        :param apply_on:
        :param verbose:
        :param control_well:
        :raise AttributeError:
        """
        try:
            if apply_on == "Plate":
                # iterate on all plate
                for plate in self.screen:
                    # check if plate object
                    if not isinstance(plate, TCA.Plate):
                        raise TypeError("Must provided good object")
                    else:
                        if self.BackgroundModel is None:
                            self.BackgroundModel = np.zeros(plate.array.shape)
                        self.BackgroundModel += plate.array
                self.BackgroundModel *= 1 / len(self.screen)
            elif apply_on == "Replicat":
                object_cnt = 0
                # iterate on all plate
                for plate in self.screen:
                    # check if plate object
                    if not isinstance(plate, TCA.Plate):
                        raise TypeError("Must provided good object")
                    else:
                        # iterate on all replicat in the plate
                        for repName, repValue in plate.replica.items():
                            if not isinstance(repValue, TCA.Replica):
                                raise TypeError
                            else:
                                if self.BackgroundModelMean is None:
                                    self.BackgroundModelMean = np.zeros(repValue.array.shape)
                                self.BackgroundModel += repValue.array
                                object_cnt += 1
                self.BackgroundModel *= 1 / object_cnt
            else:
                raise AttributeError("Apply strategy only on plate or replicat")
            if verbose:
                np.set_printoptions(suppress=True)
                print("Background Evaluation table (Median) :")
                print("Apply strategy was : ", apply_on)
                print(self.BackgroundModel)
                print("")
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def __background_surface_analysis(self, plot=False):
        """

        :param plot:
        :return:
        """
        try:
            return 0
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def __apply_background_elimination(self, apply_on, control_well=None):
        """

        :param apply_on:
        :param control_well:
        :raise AttributeError:
        """
        try:
            if apply_on == "Plate":
                # iterate on all plate
                for plate in self.screen:
                    # check if plate object
                    if not isinstance(plate, TCA.Plate):
                        raise TypeError("Must provided good object")
                    else:
                        plate.sec_array -= self.BackgroundModel
                        plate.isSpatialNormalized = True
            elif apply_on == "Replicat":
                # iterate on all plate
                for plate in self.screen:
                    # check if plate object
                    if not isinstance(plate, TCA.Plate):
                        raise TypeError("Must provided good object")
                    else:
                        # iterate on all replicat in the plate
                        for repName, repValue in plate.replica.items():
                            if not isinstance(repValue, TCA.Replica):
                                raise TypeError
                            else:
                                repValue.sec_array -= self.BackgroundModel
                                repValue.isSpatialNormalized = True
            else:
                raise AttributeError("Apply strategy only on plate or replicat")
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)