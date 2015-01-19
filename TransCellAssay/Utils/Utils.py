# coding=utf-8
"""
Usefull function
"""

import sys
import time

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


def reporthook(count, block_size, total_size):
    """
    Reporthook for visualizing advance of download
    :param count:
    :param block_size:
    :param total_size:
    :return:
    """
    global start_time
    if count == 0:
        start_time = time.time()
        return
    duration = time.time() - start_time
    progress_size = int(count * block_size)
    speed = int(progress_size / (1024 * duration))
    percent = int(count * block_size * 100 / total_size)
    sys.stdout.write("\r...%d%%, %d MB, %d KB/s, %d seconds passed" %
                     (percent, progress_size / (1024 * 1024), speed, duration))
    sys.stdout.flush()


def get_opposite_well_format(to_change):
    """
    Change Well Format
    A1 to (0,0) or (1,3) to B4
    1536 format not yet supported
    :param to_change: tuple or str
    :return: opposite well format
    """
    lettereq = dict(A=0, B=1, C=2, D=3, E=4, F=5, G=6, H=7, I=8, J=9, K=10, L=11, M=12, N=13, O=14, P=15)
    numbeq = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L', 12: 'M',
              13: 'N', 14: 'O', 15: 'P'}
    try:
        if isinstance(to_change, tuple):
            new_form = "{0}{1}".format(str(numbeq[to_change[0]]), to_change[1] + 1)
            return new_form
        elif isinstance(to_change, str):
            new_form = lettereq[to_change[0]], int(to_change[1:]) - 1
            return new_form
        else:
            raise ValueError
    except Exception as e:
        print(e)