# TransCellAssay

This Python packages is for analysis of Transfected Cell Assay data in High Throughput Screening environment.   
Data input is designed to be Single Cell data (1data/Well work well too) in csv/txt file (with extend use of pandas dataframe).
This package has been designed with the aim to facilitate the development of data analysis pipeline, so programming skills are needed for the moment.
It was developed and tested on python 3.4 platform and aim to replace CellHTS2 or similar software for our analysis.
It work on 96, 384 and 1536(depend format) Well plate with acceptable performance.

## What TCA do :

* Quality Control for control, data consistency across replica (check if data are missing).
* Controls based and non-controls based normalization, logarithmic transformation, feature scaling.
* Systematic Error Detection Test (border effect on plate).
* Systematics error Correction with Bscore, BZscore, PMP, MEA, DiffusionModel, polynomial/lowess fitting.
* Scoring with SSMD, T-Statistics, T-Test, Rank product, single cell properties.

## Python Module Dependencies

* Python >= 3.4
* Pandas
* Numpy
* Scipy
* Matplotlib, seaborn
* Scikit-learn

Python package in most recent version is a must.

## License

This work is under [GPLv3](http://www.gnu.org/licenses/gpl-3.0.html) licence.
<kopp@igbmc.fr>


© 2014-2016 KOPP Arnaud All Rights Reserved
