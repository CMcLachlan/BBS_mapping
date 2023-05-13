# BBS (Breeding Bird Survey) Mapping
Mapping breeding bird survey distance bands and species records (University of Ulster Remote Sensing and GIS module EGM722 assignment project)

## Background
Repeated, standardised ecological surveys enable abundance and diversity of species present to be monitored over time. To carry out breeding bird surveys as part of a standardised monitoring programme for their nature reserves, Essex Wildlife Trust have adapted the [British Trust for Ornithology (BTO) breeding bird survey methodology](https://www.bto.org/our-science/projects/breeding-bird-survey/research-conservation/methodology-and-survey-design), to apply these standardised methods on a smaller scale for monitoring individual nature reserves (rather than the national scheme's 1km squares methods). Fixed transects are surveyed twice per season, transects are split into approximate 200m sections, and all birds encountered (by song, call or sight) are recorded within a distance of the transect. The distance bands are defined as follows in the survey methodology: 
- 0-25m
- 25-100m
- 100m+
- Birds flying over during the survey are also recorded separately. 

Whilst it is valuable to have breeding bird survey records mapped, to visualise and integrate with other spatial data, manually mapping these records for a large number of transects would be extremely time consuming. 

## Purpose of the "BBS_mapping" code
This Python program is intended to enable an automated workflow for efficiently mapping breeding bird survey (BBS) results within the appropriate area, given survey data detailing the site, transect section, recording distance and side of transect the record was made on, and a shapefile containing lines representing each transect section on each reserve surveyed. 

## How to install and use this code
### Installations required to get started
Prior to installing and running this program, the user must have set up a GitHub account and installed Git and Conda on their machine. If this has not been completed, use the links below to complete these steps:
-	Set up GitHub account to enable use of the repository: https://github.com/ 
-	Git setup: https://git-scm.com/downloads 
-	Conda setup: https://docs.anaconda.com/free/anaconda/install/ 
-	(Optional) Github desktop: https://desktop.github.com/

### Fork and clone this repository
Find and fork the repository: 
-	Follow the link above (https://github.com/CMcLachlan/BBS_mapping) and ensure you are signed in to your GitHub account.
-	Press the “Fork” button which should be visible at the top right of the page.
-	Options for creating the fork will then be displayed. There is another branch within the BBS_mapping repository currently under development for mapping polygons representing the BBS recording distance bands, however this is not required for using the script described here, which is in the main branch. To only include the main branch in the forked repository, ensure “Copy the main branch only” is ticked. If you would like to include all branches in the repository, ensure “Copy the main branch only” is unticked. 
-	Then, click “create fork”. 
-	Once the fork has been created, you should be automatically directed to your newly forked version of the repository. 
-	Make a note of the URL, which should be similar to: “https://github.com/<your_username>/BBS_mapping”, where <your_username> represents the username of your GitHub account. 
Clone the repository so it can be worked with locally. Instructions below cover how to do this using a command prompt, however Github desktop may alternatively be used if preferred: 
-	Open Command Prompt on your computer
-	Type cd followed by the location you want the repository’s files to be stored. 
For example: 

`cd C:\Users\charl\project`
(If desired, you can navigate to the location from file explorer, right-click on the address bar and press “copy address as text”, then paste this into the command prompt, to ensure the location is copied correctly)
-	Press enter, then type or paste the following command to clone the repository to your chosen location (replace “your_username” with your GitHub user name):

`git clone https://github.com/your_username/egm722.git`
- Press enter. A message should be displayed to indicate that the repository is being cloned and when this has completed. 

### Create a conda environment for using this code
Set up a conda environment to install the required packages. Instructions below cover how to do this using Anaconda Command Prompt, however Anaconda Navigator or other preferred environment management method may alternatively be used if preferred. 
-	Open Anaconda Prompt on your computer
-	Type cd and type the directory you have cloned the repository to (and press enter to run the command), e.g.: 

`cd c:\Users\charl\project\BBS_mapping`
-	Then, use the following command to create the environment using the environment.yml file within the repository: 

`conda env create -f environment.yml`
-	After pressing enter, leave the command to run and after some time, a message should appear to confirm that this has completed, as well as how to activate/deactivate the environment. 

### Running and adapting this code
Run the script from within the BBS_mapping environment using your integrated development environment (IDE) of choice (instructions below for setting up PyCharm Community Edition): 
-	If PyCharm is not already installed, visit https://www.jetbrains.com/pycharm/download/, download the appropriate Community version for the computer you are using, and follow the installation instructions. 
-	With PyCharm installed, open Pycharm and select “create a new project”. 
-	For “Location”, save the project in the same location as the cloned BBS_mapping repository 
-	To set up a python interpreter, use the conda environment which was created in a previous step. 
-	First select “Previously configured interpreter”
-	Then press “Add interpreter” 
-	Select “Conda environment” 
-	As prompted, provide the path to the conda executable and python interpreter which is part of the previously configured BBS_mapping environment. 
-	Conda executable location may vary but should be found in the C:\Users\charl\anaconda3\condabin\conda.bat (or a similar location relative to where Anaconda is installed such as ~\Anaconda3\bin\conda)
-	Python interpreter precise location may vary, but should be found relative to Anaconda in e.g. ~/Anaconda3/envs/BBS_mapping/bin/python.exe or similar depending on operating system. 
-	Press “OK”, then “Create”, then “Create from existing sources” 
-	Double-click “BBS_mapping.py” which should now be available in the side window of the project, and press “run” or shift+F10 to run the script.  

### Dependencies
The script’s main dependencies, detailed in the table below, are listed in the environment.yml file of the repository for convenient installation of the required packages, excluding ‘os’ and ‘random’, which are standard modules in Python and do not require separate installation. 
| Dependency | Purpose |
| ---------- | ------- |
| geopandas | Reading and writing files | 
| pandas | Reading and writing files, merging dataframes, returning co-ordinates from a given distance along each record line |
| shapely | Offsetting transect lines | 
| os | Listing all files in directory to be processed | 
| random | Generating random numbers between 0 and 1 for plotting points at varying distance along transect section lines, generating random numbers between recording distance band values |

### Test data provided
Test data provided includes: 
- A shapefile representing a selection of breeding bird survey transects, with "RESERVE" (site) and "SECTION" (numbered section along each transect) attributes, in "data_files/Test" of the main branch of the repository
- Three example survey results CSV files, in "data_files/Test/Records" of the main branch of the repository

These test data files may be used automatically if running the script from within the BBS_mapping environment, as the paths to these files within the repository are included within the script. 
For further details about adapting this code and/or applying to other datasets, please refer to the "How-to Guide" within this repository. 
