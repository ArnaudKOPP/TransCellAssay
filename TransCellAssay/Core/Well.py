"""
Class for representing siRNA or wathever that target a gene
"""

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Dev"


class Well(object):
    def __init__(self, name, position, refPlaque):
        try:
            self.Name = name
            self.Position = position
            self.RefPlaque = refPlaque
            self.Id = None
            self.IdType = None
            self.TargetSequence = None
        except Exception as e:
            print(e)

    def set_id(self, identifier, identifier_type):
        try:
            self.Id = identifier
            self.IdType = identifier_type
        except Exception as e:
            print(e)

    def set_target_sequence(self, tgt_seq):
        try:
            self.TargetSequence = tgt_seq
        except Exception as e:
            print(e)

    def __repr__(self):
        try:
            return 0
        except Exception as e:
            print(e)

    def __str__(self):
        try:
            return 0
        except Exception as e:
            print(e)