import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString
import random
import os

transects = gpd.read_file("data_files/Test/BBS_test_transects.shp")  # read shapefile and assign to "transects"

def read_dist(records):
    """
    Given a dataset including the fields "X0.25", "X25.100", "X100." and "flying", with the relevant distance for each
    row indicated by a survey count value in the appropriate column, add a column to define the distance band to be used
    for mapping each record.

    :param records: dataframe
        CSV file containing the columns "X0.25", "X25.100", "X100." and "flying", with the relevant
        distance for each row indicated by a survey count value in the appropriate column.
    :return dist: The updated dataframe
        Returns a new dataframe containing a column defining the distance band from the transect line which the record
        should be mapped into.
    """

    recordsa = records[(records['X0.25'] != 'NA')]  # slice dataframe and assign 0-25 value to appropriate rows
    recordsa['dist'] = '0-25'
    recordsa['birdnumber'] = recordsa['X0.25']  # copy the survey count value into a new column
    recordsb = records[(records['X25.100'] != 'NA')]  # slice dataframe and assign 25-100 value to appropriate rows
    recordsb['dist'] = '25-100'
    recordsb['birdnumber'] = recordsb['X25.100']  # copy the survey count value into a new column
    recordsc = records[(records['X100.'] != 'NA')]  # slice dataframe and assign 100-200 value to appropriate rows
    recordsc['dist'] = '100-200'
    recordsc['birdnumber'] = recordsc['X100.']  # copy the survey count value into a new column
    recordsd = records[(records['flying'] != 'NA')]  # slice dataframe and assign 0-0 value to appropriate rows
    recordsd['dist'] = '0-0'
    recordsd['birdnumber'] = recordsd['flying']  # copy the survey count value into a new column
    mergedA = pd.concat([recordsa, recordsb])  # merge slices back together to create dataset with distance and count
    mergedB = pd.concat([mergedA, recordsc])
    mergedC = pd.concat([mergedB, recordsd])
    withdist = mergedC[(mergedC['birdnumber'].notna())]
    return withdist  # return the new merged dataframe


my_dir = "data_files/Test/Records"  # Assign directory to be iterated through to "my_dir"

dir_list = os.listdir(my_dir) # Using os.listdir, create a list of all of the files in "my_dir"

for f in dir_list:  # Use the for loop to iterate through the list of files
    records = pd.read_csv(f"data_files/Test/Records/{f}")  # read each csv file in the folder specified above
    read_dist(records).to_csv(f"data_files/Test/Updated_records/{f}.csv")  # apply read_dist to files then write to csv


