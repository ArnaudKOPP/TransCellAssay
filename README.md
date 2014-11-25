#TransCellAssay

This Python packages is for analysis of Transfected Cell Assay in High Throughput Screening environment.   
Data input is designed to be Single Cell data but 1data/well will work also.


##HOW TO USE IT
It will certainly be like a toolbox for the moment, so programming skill is needed. This package work on python 3.4.

### What TCA do :
1. Controls based and non-controls based normalization, logarithmic transformation
2. Systematic Error Detection Test
3. Systematics error Correction with Bscore, BZscore, PMP, MEA, DiffusionModel and basic background Correction/Well Correction
4. Quality Control 
5. Scoring (SSMD, T-Statistics,...)
6. Go enrichment (still in development)

##Python Module Dependencies
1. Pandas > 0.14
2. Numpy > 1.9
3. Scipy > 0.12
4. Matplotlib > 1.3.1
5. Scikit-learn 
6. requests, beautifulsoup4, xlsxwriter

##CONTACT  
kopp@igbmc.fr  

##Contributions  
If you find it useful, fork the repository, improve it and request a pull.

##License
This work is for the moment on [CC BY-NC-ND 4.0 License](https://creativecommons.org/licenses/by-nc-nd/4.0/)  
© 2014 KOPP Arnaud All Rights Reserved


## Next
###Performance enhancement
1. Refactoring Plate Analysis (cell count, ...) to use more numpy ndarray
2. Using Cython for certain part of work ??

### BUG
1. SubPlate and SubReplicat are still very buggy
2. Better Import system ???

### Principale Idea
1. Machine Learning like clustering or classification of hit
2. Bayesian Inference (FDR...)
3. PP-interaction
4. -Omics data interaction like RNA-seq from multiple cell lines
5. Dose Response Analysis
6. Phenotypic Response
7. KEGG, STRING, Panther, Biogrid, ... 
8. A lot more graphics (Screen hit map, ...)
9. Rejecting Plate by Z-score
