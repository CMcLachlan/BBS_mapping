
# BBS MAPPING - PYTHON SCRIPT TO PLOT BBS RECORDS TO CORRECT SITE, TRANSECT SECTION AND RECORDING BAND

# ---------------------------------------------------------------------------------------------------------------------
# IMPORTS
# The following lines are required to import the modules used within the script
import pandas as pd
import geopandas as gpd
from shapely import offset_curve
import random
import os
from shapely import wkt

# ---------------------------------------------------------------------------------------------------------------------
# VARIABLES
# The lines below define variables used at several points within the script, which may be updated if required to apply
# the script to other directories or data in a different CRS.

# "BBS_records" is the folder containing the original unmapped records (should only contain the records CSV files)
BBS_records = "data_files/Test/Records"  # Assign directory to be iterated through to "BBS_records"
BBS_list = os.listdir(BBS_records)  # Using os.listdir, create a list of all of the files in "BBS_records"

Transects = gpd.read_file("data_files/Test/BBS_test_transects.shp")  # read shapefile and assign to "Transects"

# "Updated_BBS" is the folder where updated records should be saved (should be empty before first running script and
# intermediate files are overwritten before reaching the end result)
Updated_BBS = "data_files/Test/Updated_records"  # Assign directory to be iterated through to "Updated_BBS"
Updated_BBS_list = os.listdir(Updated_BBS)  # Using os.listdir, create a list of all of the files in "Updated_BBS"

MyCRS = 'epsg:27700'  # Define the CRS of the data to ensure geometry column can be read later in the script. For the
# distance bands to be correctly mapped, this must be a projected CRS.

# ---------------------------------------------------------------------------------------------------------------------
# FUNCTION DEFINITIONS
# read_dist function:
# Create a function which defines the distances between which each record should be offset from the walked transect
def read_dist(records):
    """
    Given a dataset including the fields "X0.25", "X25.100", "X100." and "flying", with the relevant distance for each
    row indicated by a survey count value in the appropriate column, add a column to define the distance band to be used
    for mapping each record.

    :param records: dataframe
        CSV file containing the columns "X0.25", "X25.100", "X100." and "flying", with the relevant
        distance for each row indicated by a survey count value in the appropriate column.
    :return withdist: The updated dataframe
        Returns a new dataframe containing columns "distfrom" and "distto" defining the distance band from the transect
        line which the record should be mapped into.
    """

    recordsa = records[(records['X0.25'] != 'NA')]  # slice dataframe and assign 0-25 value to appropriate rows
    recordsa['distfrom'] = '0'
    recordsa['distto'] = '25'
    recordsa['birdnumber'] = recordsa['X0.25']  # copy the survey count value into a new column
    recordsb = records[(records['X25.100'] != 'NA')]  # slice dataframe and assign 25-100 value to appropriate rows
    recordsb['distfrom'] = '25'
    recordsb['distto'] = '100'
    recordsb['birdnumber'] = recordsb['X25.100']  # copy the survey count value into a new column
    recordsc = records[(records['X100.'] != 'NA')]  # slice dataframe and assign 100-200 value to appropriate rows
    recordsc['distfrom'] = '100'
    recordsc['distto'] = '130'
    recordsc['birdnumber'] = recordsc['X100.']  # copy the survey count value into a new column
    recordsd = records[(records['flying'] != 'NA')]  # slice dataframe and assign 0-0 value to appropriate rows
    recordsd['distfrom'] = '0'
    recordsd['distto'] = '0'
    recordsd['birdnumber'] = recordsd['flying']  # copy the survey count value into a new column
    mergedA = pd.concat([recordsa, recordsb])  # merge slices back together to create dataset with distance and count
    mergedB = pd.concat([mergedA, recordsc])
    mergedC = pd.concat([mergedB, recordsd])
    withdist = mergedC[(mergedC['birdnumber'].notna())]
    return withdist  # return the new merged dataframe


# transect_geom function:
# Create a function to copy the relevant transect geometry into the unmapped records dataframe
def transect_geom(records, transects):
    """
    Given a dataset containing survey records including columns indicating site name and transect section, and a line
    shapefile also including the site name and transect section as attributes, look up the  site name and transect
    section in the transects shapefile to add the relevant geometry to the survey records.

    :param records: dataframe
        CSV file of survey records containing the columns "reserve" and "section".
    :param transects: shapefile
        Line layer containing the attributes "RESERVE" and "SECTION".
    :return withgeom: The updated geodataframe
        Returns a new geodataframe which includes geometry for each survey record, which matches the appropriate
        transect section on the appropriate reserve.
    """

    mergedrecords = pd.merge(records, transects,  how='left', left_on=['reserve','section'], right_on = ['RESERVE',
                                                                                                         'SECTION'])
    return mergedrecords  # merge transects and records by matching up reserve name and transect section


# read_offset function:
# Create a function which offsets the line geometry for each record to the correct side and distance
def read_offset(Records):
    """
    Given a dataframe containing survey records, distance and side each record should be offset from the original
    transect, and linestring geometry, offset each record by a distance as defined within the dataframe.

    :param Records: dataframe
        CSV file of survey records including the columns "distfrom" (float), "distto" (float), "geometry" (linestring
        WKT in projected CRS), "L.R" ('L'/'R' indicating side of transect).
    :return: offset_records
        Geodataframe with geometry column updated as offset by the appropriate distance on the appropriate side of the
        original transect line.
    """

    Records['geometry'] = Records['geometry'].apply(wkt.loads)
    Records = gpd.GeoDataFrame(Records, crs=MyCRS)
    for ind, row in Records.loc[(Records['L.R'] == 'L')].iterrows():
        fr = Records.loc[ind, 'distfrom']
        to = Records.loc[ind, 'distto']
        dist = random.uniform(to, fr)
        Records.loc[ind, 'geometry'] = row['geometry'].offset_curve(dist, quad_segs=16, join_style=1, mitre_limit=5.0)
    for ind, row in Records.loc[(Records['L.R'] == 'R')].iterrows():
        fr = Records.loc[ind, 'distfrom']
        to = Records.loc[ind, 'distto']
        dist = -abs(random.uniform(to, fr))
        Records.loc[ind, 'geometry'] = row['geometry'].offset_curve(dist, quad_segs=16, join_style=1, mitre_limit=5.0)
    return Records


# plot_points function:
# Create a function which converts the records geometry from linestring to points a random distance along each line
def plot_points(Records):
    """
    Given a dataframe containing survey records mapped to a line offset the appropriate side/distance from the original
    transect line, use each record's linestring geometry to plot a point a random distance along the for each record.
    :param Records: dataframe
        CSV file containing a "geometry" column (linestring WKT) and any other data for each record
    :return: Records points
        Geodataframe with geometry converted from linestring to a single point a random distance along the line, and
        unrequired columns removed.
    """

    Records['geometry'] = Records['geometry'].apply(wkt.loads)
    Records = gpd.GeoDataFrame(Records, crs=MyCRS)
    for ind, row in Records.iterrows():
        pointdist = random.uniform(0.3, 0.7)  # generate a random number to represent a point along the line
        Records.loc[ind, 'geometry'] = row['geometry'].interpolate(pointdist, normalized=True)
    Records.drop(columns=["Unnamed: 0.1", "Unnamed: 0.2", "Unnamed: 0", "Shape_Leng", "RESERVE", "SECTION"], inplace=True)
    return Records


# ---------------------------------------------------------------------------------------------------------------------
# APPLICATION OF FUNCTIONS TO RECORDS FILES
for f in BBS_list:  # Use the for loop to iterate through the list of files
    records = pd.read_csv(f"data_files/Test/Records/{f}")  # read each csv file in the folder specified above
    read_dist(records).to_csv(f"data_files/Test/Updated_records/{f}")  # apply read_dist to files then write to csv


for f in Updated_BBS_list:  # Use the for loop to iterate through the list of files
    Records = pd.read_csv(f"data_files/Test/Updated_records/{f}")  # read each csv file in the folder specified above
    transect_geom(Records, Transects).to_csv(f"data_files/Test/Updated_records/{f}")
    # merge transect geometry to records then write to csv


for f in Updated_BBS_list:  # Use the for loop to iterate through the list of files
    Records = pd.read_csv(f"data_files/Test/Updated_records/{f}")  # read each csv file in the folder specified above
    read_offset(Records).to_csv(f"data_files/Test/Updated_records/{f}")  # apply read_offset and write to csv


for f in Updated_BBS_list:  # Use the for loop to iterate through the list of files
    Records = pd.read_csv(f"data_files/Test/Updated_records/{f}")  # read each csv file in the folder specified above
    plot_points(Records).to_csv(f"data_files/Test/Updated_records/{f}")  # apply plot_points and write to csv
