# coding=utf-8
"""
Substract a determined background of the screen/plate/replicat
Analogous to BackgroundCorrection but here it's a determined background that we provided
"""

import TransCellAssay as TCA

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


class BackgroundSubstraction():
    """

    :param background:
    """

    def __init__(self, background=None):
        try:
            self.background = background
            self.plate_lst = []
        except Exception as e:
            print(e)

    def background_substraction(self, *args):
        """

        :param args:
        """
        try:
            for arg in args:
                if isinstance(arg, TCA.Plate):
                    self.plate_lst.append(arg)
                elif isinstance(arg, list):
                    for elem in arg:
                        if isinstance(elem, TCA.Plate):
                            self.plate_lst.append(elem)
                        else:
                            raise TypeError('Accept only list of Plate element')
                else:
                    raise TypeError('Accept only plate or list of plate')
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)

    def __process(self):
        """

        """
        try:
            # iterate on all plate
            for plate in self.plate_lst:
                # iterate on all replicat in the plate
                for repName, repValue in plate.replicat.items():
                    repValue.sec_array = repValue.array - self.background
                    repValue.isSpatialNormalized = True
        except Exception as e:
            print(e)