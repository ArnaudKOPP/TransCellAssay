#TransCellAssay

This Python packages is for analysis of Transfected Cell Assay data in High Throughput Screening environment.   
Data input is designed to be Single Cell data but 1data/well will work also in csv/txt file.
This package has been designed with the aim to facilitate the development of data analysis pipeline, so programming skills are needed for the moment. 
It was developed and tested on python 3.4 platform and will replace CellHTS2 or similar software for our analysis. It work 
on 96, 384 and 1536(depend format) Well plate with acceptable performance.

### What TCA do :

* Quality Control for control, data consistency across replica (check if data are missing)
* Controls based and non-controls based normalization, logarithmic transformation, feature scaling
* Systematic Error Detection Test
* Systematics error Correction with Bscore, BZscore, PMP, MEA, DiffusionModel and basic background Correction/Well Correction
* Scoring (SSMD, T-Statistics, T-Test, Rank product, single cell properties)

##Python Module Dependencies

* Python 3.4
* Pandas 
* Numpy 
* Scipy 
* Matplotlib, seaborn
* Scikit-learn

Python package in most recent version is a must

##CONTACT 
 
kopp@igbmc.fr

##License

This work is under [GPLv3](http://www.gnu.org/licenses/gpl-3.0.html) licence.
© 2014-2015 KOPP Arnaud All Rights Reserved


##Further developpment

* Machine Learning like clustering or classification of hit
* Bayesian Inference 
* Dose Response Analysis
* Phenotypic Response
* hdf5 support