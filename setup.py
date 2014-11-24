from distutils.core import setup

setup(
    name='TransCellAssay',
    version='0.01',
    packages=['Core', 'Utils', 'Stat', 'IO', 'ML', 'Omics'],
    install_requires=['pandas', 'numpy', 'scipy', 'scikit-learn', 'matplotlib', 'xlsxwriter', 'beautifulsoup4',
                      'requests'],
    url='https://github.com/ArnaudKOPP/TransCellAssay',
    license='GPL V3',
    author='Arnaud KOPP',
    author_email='kopp.arnaud@gmail.com',
    description='Package for analyze HTS data'
)
