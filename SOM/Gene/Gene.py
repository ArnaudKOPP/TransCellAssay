"""
Class for representing siRNA or wathever that target a gene
"""

import SOM

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Dev"


class Gene():
    def __init__(self, name):
        try:
            self.Name = name
            self.Id = None
            self.Position = None
            self.RefPlaque = None
            self.TargetSequence = None
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