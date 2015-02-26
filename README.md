#TransCellAssay

This Python packages is for analysis of Transfected Cell Assay in High Throughput Screening environment.   
Data input is designed to be Single Cell data but 1data/well will work also.
This package has been designed with the aim to facilitate the development of data analysis pipeline, so programming skills are needed for the moment. 
It was developped and tested on python 3.4 platform and will replace CellHTS2 or similar software for our analysis. It work 
on 96 and 384 Well plate with acceptable performance (1536 on plate for further dev).

### What TCA do :

* Quality Control for control, data consistency across replicat (check if data are missing)
* Controls based and non-controls based normalization, logarithmic transformation, feature scaling
* Systematic Error Detection Test
* Systematics error Correction with Bscore, BZscore, PMP, MEA, DiffusionModel and basic background Correction/Well Correction
* Scoring (SSMD, T-Statistics, Rank product, single cell properties)

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

##Contributions 
 
If you find it useful, fork the repository, improve it and request a pull.

##License

This work is for the moment on [CC BY-NC-ND 4.0 License](https://creativecommons.org/licenses/by-nc-nd/4.0/)  
© 2014-2015 KOPP Arnaud All Rights Reserved


##Further developpment

* Machine Learning like clustering or classification of hit
* Bayesian Inference (FDR...)
* Dose Response Analysis
* Phenotypic Response
* 1536 Well Plate (big depend on format writing in export of data)