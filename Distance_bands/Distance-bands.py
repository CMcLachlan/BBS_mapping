import geopandas as gpd

test_transects = gpd.read_file('Test_data/test_transects.shp')

left_buffer025 = test_transects.buffer(25, single_sided=True)
LB025gdf = gpd.GeoDataFrame(gpd.GeoSeries(left_buffer025))
LB025gdf = LB025gdf.rename(columns={0:'geometry'}).set_geometry('geometry')
LB025join = LB025gdf.sjoin(test_transects, how="inner", predicate='touches')
LB025join['Side'] = 'L'
LB025join['Band'] = '0-25'

right_buffer025 = test_transects.buffer(-25, single_sided=True)
RB025gdf = gpd.GeoDataFrame(gpd.GeoSeries(right_buffer025))
RB025gdf = RB025gdf.rename(columns={0:'geometry'}).set_geometry('geometry')
RB025join = RB025gdf.sjoin(test_transects, how="inner", predicate='touches')
RB025join['Side'] = 'R'
RB025join['Band'] = '0-25'

band025 = gpd.pd.merge(LB025join, RB025join, how='outer')

band025.to_file('Test_results/band025_test.shp')

testbuffer25_100A = test_transects.buffer(100, single_sided=True)
testbuffer25_100temp = test_transects.buffer(25, single_sided=True)
testbuffer25_100Left = testbuffer25_100A.difference(testbuffer25_100temp)


gpd.GeoSeries(testbuffer25_100Left).to_file('Test_results/left_buffer25_100_test.shp')
