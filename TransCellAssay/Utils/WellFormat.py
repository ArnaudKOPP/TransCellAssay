"""
Utilities method for switching well format:
A1 to (0, 0) or (2, 2) to C3
"""

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


def get_opposite_well_format(input):
    """
    Change Well Format
    A1 to (0,0) or (1,3) to B4
    1536 format not yet supported
    :param input: tuple or str
    :return: opposite well format
    """
    lettereq = dict(A=0, B=1, C=2, D=3, E=4, F=5, G=6, H=7, I=8, J=9, K=10, L=11, M=12, N=13, O=14, P=15)
    numbeq = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L', 12: 'M',
              13: 'N', 14: 'O', 15: 'P'}
    try:
        if isinstance(input, tuple):
            new_form = "{0}{1}".format(str(numbeq[input[0]]), input[1] + 1)
            return new_form
        elif isinstance(input, str):
            new_form = lettereq[input[0]], int(input[1:]) - 1
            return new_form
        else:
            raise ValueError
    except Exception as e:
        print(e)
