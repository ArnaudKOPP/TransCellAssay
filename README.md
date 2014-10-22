#TransCellAssay PROJECT

This Python packages is for analyzis of Transfected Cell Assay in Higth Throughput Screening environment.  
He use different technique for removing systematic error like edge effect on plate.  
Data input is designed to be Single Cell data but 1data/well will work also.


##HOW TO USE IT
It will certainly be like a toolbox for the moment, so programming skill is needed.

### What TCA do :
1. Controls based and non-controls based normalization,  logarithmic transformation
2. Systematic Error Detection Test
3. Systematics error Correction with Bscore, BZscore, PMP, MEA, DiffusionModel and basic background Correction/Well Correction
4. Quality Control (need to be implemented)
5. Scoring (SSMD, TTest,...)

### TODO
1. Machine Learning ( classification, clustering, Dimensionality Reduction, ...)
2. Bayesian Inference
3. ???

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
