import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString
import random
import os

# create a function which defines the distances between which each record should be offset from the walked transect
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
    recordsc['distto'] = '200'
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


my_dir = "data_files/Test/Records"  # Assign directory to be iterated through to "my_dir"

dir_list = os.listdir(my_dir)  # Using os.listdir, create a list of all of the files in "my_dir"

for f in dir_list:  # Use the for loop to iterate through the list of files
    records = pd.read_csv(f"data_files/Test/Records/{f}")  # read each csv file in the folder specified above
    read_dist(records).to_csv(f"data_files/Test/Updated_records/withdist_{f}")  # apply read_dist to files then write to csv

# create a function to copy the relevant transect geometry into the unmapped records dataframe
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


Transects = gpd.read_file("data_files/Test/BBS_test_transects.shp")  # read shapefile and assign to "transects"

my_dir2 = "data_files/Test/Updated_records"  # Assign directory to be iterated through to "my_dir2"

dir_list2 = os.listdir(my_dir2)  # Using os.listdir, create a list of all of the files in "my_dir2"

for f in dir_list2:  # Use the for loop to iterate through the list of files
    Records = pd.read_csv(f"data_files/Test/Updated_records/{f}")  # read each csv file in the folder specified above
    transect_geom(Records, Transects).to_csv(f"data_files/Test/Updated_records/withgeom_{f}")
    # merge transect geometry to records then write to csv

