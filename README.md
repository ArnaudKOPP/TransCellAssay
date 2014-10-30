#TransCellAssay

This Python packages is for analysis of Transfected Cell Assay in High Throughput Screening environment.   
Data input is designed to be Single Cell data but 1data/well will work also.


##HOW TO USE IT
It will certainly be like a toolbox for the moment, so programming skill is needed.

### What TCA do :
1. Controls based and non-controls based normalization, logarithmic transformation
2. Systematic Error Detection Test
3. Systematics error Correction with Bscore, BZscore, PMP, MEA, DiffusionModel and basic background Correction/Well Correction
4. Quality Control 
5. Scoring (SSMD, T-Statistics,...)

### TODO
1. Machine Learning ( classification, clustering, Dimensionality Reduction, ...)
2. Bayesian Inference (FDR...)
3. GSEA, PP-interaction, -Omics data interaction
4. Web interface

##DEPENDENCIES
1. Python > 3.3
2. Pandas > 0.14
3. Numpy > 1.8
4. Scipy > 0.12
5. Matplotlib > 1.3.1
6. Scikit-learn 

##CONTACT  
kopp@igbmc.fr  

##Contributions  
If you find it useful, fork the repository, improve it and request a pull.

##License
This work is for the moment on [CC BY-NC-ND 4.0 License](https://creativecommons.org/licenses/by-nc-nd/4.0/)  
© 2014 KOPP Arnaud All Rights Reserved