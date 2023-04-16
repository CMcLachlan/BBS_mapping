import geopandas as gpd

test_transects = gpd.read_file('Test_data/test_transects.shp')

left_buffer25 = test_transects.buffer(25, single_sided=True)  # create initial 25m left buffer
LB025gdf = gpd.GeoDataFrame(gpd.GeoSeries(left_buffer25))  # convert buffer to geodataframe to add attributes
LB025gdf = LB025gdf.rename(columns={0:'geometry'}).set_geometry('geometry')  # set geometry of geodataframe
LB025join = LB025gdf.sjoin(test_transects, how="inner", predicate='touches')  # join attributes from transects to buffer
LB025join['Side'] = 'L'  # add column to label these polygons as the "left" recording compartments
LB025join['Band'] = '0-25'  # add column to label these polygons as the "0-25m" distance band

temp_left0 = test_transects.buffer(0, single_sided=True)  # create temporary buffer to subtract from the first
left_buffer025 = left_buffer25.difference(temp_left0)  # create required polygons by subtracting unrequired area
leftGDF = gpd.GeoDataFrame(gpd.GeoSeries(left_buffer025))  # convert new geoseries to geodataframe
leftGDF = leftGDF.rename(columns={0:'geometry'}).set_geometry('geometry')  # set geometry of new geodataframe
LB025 = LB025join.set_geometry(leftGDF['geometry']) # copy geometry from subtracted buffer to geodataframe to be exported


right_buffer025 = test_transects.buffer(-25, single_sided=True)
RB025gdf = gpd.GeoDataFrame(gpd.GeoSeries(right_buffer025))
RB025gdf = RB025gdf.rename(columns={0:'geometry'}).set_geometry('geometry')
RB025join = RB025gdf.sjoin(test_transects, how="inner", predicate='touches')
RB025join['Side'] = 'R'
RB025join['Band'] = '0-25'

band025 = gpd.pd.merge(LB025join, RB025join, how='outer')

band025.to_file('Test_results/band025_test.shp')

left_buffer25100 = test_transects.buffer(100, single_sided=True)  # create initial 100m left buffer
LB025100gdf = gpd.GeoDataFrame(gpd.GeoSeries(left_buffer25100))  # convert buffer to geodataframe to add attributes
LB025100gdf = LB025100gdf.rename(columns={0:'geometry'}).set_geometry('geometry')  # set geometry of geodataframe
LB025100join = LB025100gdf.sjoin(test_transects, how="inner", predicate='touches')  # join attributes from transects to buffer
LB025100join['Side'] = 'L'  # add column to label these polygons as the "left" recording compartments
LB025100join['Band'] = '25-100'  # add column to label these polygons as the "25-100m" distance band

temp_left25 = test_transects.buffer(25, single_sided=True)  # create temporary buffer to subtract from the first
left_buffer25100 = left_buffer25100.difference(temp_left25)  # create required polygons by subtracting unrequired area
left25GDF = gpd.GeoDataFrame(gpd.GeoSeries(left_buffer25100))  # convert new geoseries to geodataframe
left25GDF = left25GDF.rename(columns={0:'geometry'}).set_geometry('geometry')  # set geometry of new geodataframe
LB25100 = LB025100join.set_geometry(left25GDF['geometry']) # copy geometry from subtracted buffer to geodataframe to be exported

LB25100.to_file('Test_results/left_buffer25_100_test.shp')
