# BBS (Breeding Bird Survey) Mapping
Mapping breeding bird survey distance bands and species records (University of Ulster Remote Sensing and GIS module EGM722 assignment project)

## Background
Repeated, standardised surveys enable abundance and diversity of species present to be monitored over time. To carry out breeding bird surveys as part of a standardised monitoring programme for their nature reserves, Essex Wildlife Trust have adapted the [British Trust for Ornithology (BTO) breeding bird survey methodology](https://www.bto.org/our-science/projects/breeding-bird-survey/research-conservation/methodology-and-survey-design), to apply these standardised methods on a smaller scale for monitoring individual nature reserves (rather than the national scheme's 1km squares methods). Fixed transects are surveyed twice per season, transects are split into approximate 200m sections, and all birds encountered (by song, call or sight) are recorded within a distance of the transect. The distance bands are defined as follows in the survey methodology: 
- 0-25m
- 25-100m
- 100m+
- Birds flying over during the survey are also recorded separately. 

Whilst it is valuable to have breeding bird survey records mapped in order to visualise and analyse alongside other spatial data, these records may not be mapped during the survey itself for a variety of reasons (speed/concentration required during recording making GIS apps unsuitable options, lack of access to GIS licenses). 
Manually mapping these records afterwards would be extremely time consuming when a large number of sites have been surveyed multiple times, with multiple distance bands to take into account per transect section. 

## Purpose
This repository has been created to share a Python program enabling an automated workflow for mapping breeding bird survey (BBS) results. Using a shapefile representing each transect section surveyed, and a set of CSV files representing the results from each survey detailing the site name, transect section, "side" and distance band, points are plotted for each record on the correct side and distance from the original transect line. 

## How to install and use this code
### Installations required to get started

### Cloning this repository

### Create a conda environment for using this code

### Running and adapting this code

### Test data provided
Test data provided includes: 
- A shapefile representing a selection of breeding bird survey transects, with "RESERVE" (site) and "SECTION" (numbered section along each transect) attributes
- Three example results CSV files
These files are provided within "data_files/Test" of the main branch of the repository. 
