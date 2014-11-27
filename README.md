#TransCellAssay

This Python packages is for analysis of Transfected Cell Assay in High Throughput Screening environment.   
Data input is designed to be Single Cell data but 1data/well will work also.


##HOW TO USE IT

This package has been designed with the aim to facilitate the development of data analysis pipeline, so programming skills are needed for the moment. 
This package was developped and tested on python 3.4.

### What TCA do :

* Controls based and non-controls based normalization, logarithmic transformation
* Systematic Error Detection Test
* Systematics error Correction with Bscore, BZscore, PMP, MEA, DiffusionModel and basic background Correction/Well Correction
* Quality Control 
* Scoring (SSMD, T-Statistics,...)
* Go enrichment (still in development)

##Python Module Dependencies

* Pandas > 0.14
* Numpy > 1.9
* Scipy > 0.12
* Matplotlib > 1.3.1
* Scikit-learn 
* requests, beautifulsoup4, xlsxwriter

##CONTACT 
 
kopp@igbmc.fr  

##Contributions 
 
If you find it useful, fork the repository, improve it and request a pull.

##License

This work is for the moment on [CC BY-NC-ND 4.0 License](https://creativecommons.org/licenses/by-nc-nd/4.0/)  
© 2014 KOPP Arnaud All Rights Reserved


## Next

###Performance enhancement

* Refactoring Plate Analysis (cell count, ...) to use more numpy ndarray
* Using Cython for certain part of work ??

### BUG

* SubPlate and SubReplicat are still very buggy
* Better Import system ???

### Principale Idea to implement

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