# coding=utf-8
"""
Class for representing a well
"""

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Dev"


class Well(object):
    """
    Class to be a representation of a Well with importante data for RNAi screens
    """

    def __init__(self, name, position, ref_plate):
        try:
            self.name = name
            self.position = position
            self.ref_plate = ref_plate
            self.id = None
            self.id_type = None
            self.target_sequence = None
        except Exception as e:
            print(e)

    def set_id(self, identifier, identifier_type):
        """

        :param identifier:
        :param identifier_type:
        """
        try:
            self.id = identifier
            self.id_type = identifier_type
        except Exception as e:
            print(e)

    def set_target_sequence(self, tgt_seq):
        """

        :param tgt_seq:
        """
        try:
            self.target_sequence = tgt_seq
        except Exception as e:
            print(e)

    def __repr__(self):
        try:
            return 0
        except Exception as e:
            print(e)

    def __str__(self):
        try:
            return self.__repr__()
        except Exception as e:
            print(e)
