# coding=utf-8
from distutils.core import setup

setup(
    name='TransCellAssay',
    version='1.0',
    packages=['Core', 'Utils', 'Stat', 'IO'],
    install_requires=['pandas', 'numpy', 'scipy', 'scikit-learn', 'matplotlib', 'seaborn', 'xlsxwriter'],
    url='https://github.com/ArnaudKOPP/TransCellAssay',
    license='GPLv3',
    author='Arnaud KOPP',
    author_email='kopp.arnaud@gmail.com',
    description='Package for analyze High Throughput Screening data'
)
