from distutils.core import setup
from Cython.Build import cythonize

setup(
    name='TransCellAssay',
    version='0.01',
    packages=['Core', 'Utils', 'Stat', 'IO', 'ML', 'Omics'],
    install_requires=['pandas', 'numpy', 'scipy', 'scikit-learn', 'matplotlib', 'xlsxwriter', 'beautifulsoup4',
                      'requests'],
    url='https://github.com/ArnaudKOPP/TransCellAssay',
    license='CC BY-NC-ND 4.0 License',
    author='Arnaud KOPP',
    author_email='kopp.arnaud@gmail.com',
    description='Package for analyze HTS data'
)

setup(
    ext_modules=cythonize("TransCellAssay/Stat/PlateAnalyzis.py"),
)

"""
python3 setup.py build_ext --inplace
"""