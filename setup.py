# coding=utf-8
from distutils.core import setup

setup(
    name='TransCellAssay',
    version='0.01',
    packages=['Core', 'Utils', 'Stat', 'IO'],
    install_requires=['pandas', 'numpy', 'scipy', 'scikit-learn', 'matplotlib', 'seaborn', 'xlsxwriter',
                      'beautifulsoup4', 'requests'],  # if WSDL add -> 'suds-jurko'
    url='https://github.com/ArnaudKOPP/TransCellAssay',
    license='CC BY-NC-ND 4.0 License',
    author='Arnaud KOPP',
    author_email='kopp.arnaud@gmail.com',
    description='Package for analyze High Throughput Screening data'
)