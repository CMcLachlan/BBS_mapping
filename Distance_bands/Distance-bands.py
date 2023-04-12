import geopandas as gpd
import matplotlib.pyplot as plt

test_transects = gpd.read_file('Distance_bands/Test_data/Test_transects.shp')

left_buffer025 = test_transects.buffer(25, single_sided=True)
right_buffer025 = test_transects.buffer(-25, single_sided=True)


gpd.GeoSeries(right_buffer025).plot()
plt.show()

gpd.GeoSeries(right_buffer025).to_file('Distance_bands/Test_results/Right_buffer025_test.shp')
gpd.GeoSeries(left_buffer025).to_file('Distance_bands/Test_results/Left_buffer025_test.shp')