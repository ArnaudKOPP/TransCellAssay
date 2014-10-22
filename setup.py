from distutils.core import setup

setup(
    name='TransCellAssay',
    version='0.01',
    packages=['ScreenPateReplicatPS', 'Utils', 'Statistic', 'IO'],
    install_requires=['pandas', 'numpy', 'scipy', 'matplotlib'],
    url='https://github.com/ArnaudKOPP/TransCellAssay',
    license='GPL V2',
    author='Arnaud KOPP',
    author_email='kopp.arnaud@gmail.com',
    description='Package for analyze HTS data'
)
