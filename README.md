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
6. Go enrichment (still in development)

##DEPENDENCIES
1. Python > 3.3
2. Pandas > 0.14
3. Numpy > 1.9
4. Scipy > 0.12
5. Matplotlib > 1.3.1
6. Scikit-learn 
7. requests, grequests (still buggy), beautifulsoup4

##CONTACT  
kopp@igbmc.fr  

##Contributions  
If you find it useful, fork the repository, improve it and request a pull.

##License
This work is for the moment on [CC BY-NC-ND 4.0 License](https://creativecommons.org/licenses/by-nc-nd/4.0/)  
© 2014 KOPP Arnaud All Rights Reserved


## TODO

### BUG
1. SubPlate and SubReplicat are still very buggy
2. Better Import system ???

### Principale Idea
1. Machine Learning :
    1. Classification ( C4.5, SVM, Neural Network, K neirest Neighbor, Random Forest ...)
    2. Clustering ( K-mean, EM, Hierarchical ... )
    3. Dimensionality reduction ( PCA, Gready Stepwise, Infogain, OneR, Greedy ... )
2. Bayesian Inference (FDR...)
3. GSEA (GO)
4. PP-interaction
5. -Omics data interaction like RNA-seq from multiple cell lines
6. Dose Response Analysis
7. Phenotypic Response
8. KEGG, STRING, Panther, Biogrid, ... 
9. A lot more graphics (Screen hit map, ...)
10. Rejecting Plate by Z-score

### Long long term
1. Web interface

### Need To be Refactoring
1. ResultArray.py
2. CellCount.py
3. PosCells.py
4. Analysis.py