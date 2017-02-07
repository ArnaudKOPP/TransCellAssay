# TransCellAssay

This Python packages is designed to analysis data from High Content Screening assay.   
Data input are designed to be Single Cell data (1data/Well work well too) in csv/txt file.<br>
This package has been designed with the aim to facilitate the development of data analysis pipeline, so programming skills are needed to make you own analysis pipeline.<br>
It was developed and tested on python 3.4 platform and aim to replace CellHTS2 or similar software for our analysis.<br>
It work on 96, 384 and 1536 (depend format) well plate with acceptable performance.

## What TCA do :

* Quality Control for control, data consistency across replica (check if data are missing).
* Controls based and non-controls based normalization, logarithmic transformation, feature scaling.
* Systematic Error Detection Test (border effect on plate).
* Systematics error Correction with Bscore, BZscore, PMP, MEA, DiffusionModel, polynomial/lowess fitting.
* Scoring with SSMD, T-Statistics, T-Test, Rank product, single cell properties.
* Plotting features
* Easy use of Scikit-Learn machine learning package

## Python Module Dependencies

See requirements.txt file, packages in most recent version is a must.

## License

This work is under [GPLv3](http://www.gnu.org/licenses/gpl-3.0.html) licence.
<kopp@igbmc.fr>


© 2014-2017 KOPP Arnaud All Rights Reserved
