#TransCellAssay

This Python packages is for analysis of Transfected Cell Assay in High Throughput Screening environment.   
Data input is designed to be Single Cell data but 1data/well will work also.
This package has been designed with the aim to facilitate the development of data analysis pipeline, so programming skills are needed for the moment. 
This package was developped and tested on python 3.4. It can replace CellHTS2 or similar software

### What TCA do :

* Quality Control for control, data consistency across replicat (check if data are missing)
* Controls based and non-controls based normalization, logarithmic transformation
* Systematic Error Detection Test (edge effect or something else)
* Systematics error Correction with Bscore, BZscore, PMP, MEA, DiffusionModel and basic background Correction/Well Correction
* Scoring (SSMD, T-Statistics,...)
* Basic Go enrichment with list of gene

##Python Module Dependencies

* Python 3.4
* Pandas 
* Numpy 
* Scipy 
* Matplotlib, seaborn
* Scikit-learn 
* requests, beautifulsoup4 for REST part
* xlsxwriter

Python package in most recent version is a must

##CONTACT 
 
kopp@igbmc.fr  

##Contributions 
 
If you find it useful, fork the repository, improve it and request a pull.

##License

This work is for the moment on [CC BY-NC-ND 4.0 License](https://creativecommons.org/licenses/by-nc-nd/4.0/)  
© 2014-2015 KOPP Arnaud All Rights Reserved


##Principale Idea to implement

* Machine Learning like clustering or classification of hit
* Bayesian Inference (FDR...)
* PP-interaction
* -Omics data interaction like RNA-seq from multiple cell lines
* Dose Response Analysis
* Phenotypic Response
* KEGG, STRING, Panther, Biogrid, ... 
* A lot more graphics (Screen hit map, ...)
* Rejecting Plate by Z-score
* Make a docker image for easy sharing !!