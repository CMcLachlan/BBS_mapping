import geopandas as gpd

test_transects = gpd.read_file('Test_data/test_transects.shp')

def distance_bands(transect, dist_from, dist_to, left=True, right=True):
    """
    Create a polygon buffer for a defined distance from a line.

    :param transect: shapefile
        The line dataset to be buffered to create the distance bands
    :param dist_from: int, float
        Distance in metres the polygon should begin from the transect line
    :param dist_to: int, float
        Distance in metres the polygon should reach from the transect line
    :param left: bool, optional
        Default = True - to create a polygon on the "left" side of the transect (positive buffer)
    :param right: bool, optional
        Default = True - to create a polygon on the "right" side of the transect (negative buffer)
    :return: dist_from-dist_to_buffer: a geodataframe containing defined distance polygons and attributes from original line
    """
    buffer = {}
    if left:
        lb = transect.buffer(dist_to, single_sided=True)  # create initial left buffer from 0 to dist_to
        lbgdf = gpd.GeoDataFrame(gpd.GeoSeries(lb))  # convert buffer to geodataframe to add attributes
        lbgdf = lbgdf.rename(columns={0: 'geometry'}).set_geometry('geometry')  # set geometry of geodataframe
        lbjoin = lbgdf.sjoin(transect, how="inner", predicate='touches')  # join attributes from transects to buffer
        lbjoin['Side'] = 'L' # add column to label these polygons as the "left" recording compartments
        lbjoin['Band'] = '{}-{}'.format(dist_from, dist_to)  # add column to label these polygons as "dist_from-dist_to" band
        templeft = transect.buffer(dist_from, single_sided=True)  # create temporary buffer to subtract from the first
        leftbuf = lb.difference(templeft)  # create required polygons by subtracting unrequired area
        leftgdf = gpd.GeoDataFrame(gpd.GeoSeries(leftbuf))  # convert new geoseries to geodataframe
        leftgdf = leftgdf.rename(columns={0: 'geometry'}).set_geometry('geometry')  # set geometry of new geodataframe
        leftbuffer = lbjoin.set_geometry(leftgdf['geometry'])  # copy geometry from subtracted buffer to geodataframe to be exported
    if right:
        rb = transect.buffer(-abs(dist_to), single_sided=True)  # create initial right buffer from 0 to dist_to
        rbgdf = gpd.GeoDataFrame(gpd.GeoSeries(rb))  # convert buffer to geodataframe to add attributes
        rbgdf = rbgdf.rename(columns={0: 'geometry'}).set_geometry('geometry')  # set geometry of geodataframe
        rbjoin = rbgdf.sjoin(transect, how="inner", predicate='touches')  # join attributes from transects to buffer
        rbjoin['Side'] = 'R'  # add column to label these polygons as the "right" recording compartments
        rbjoin['Band'] = '{}-{}'.format(dist_from, dist_to)  # add column to label these polygons as "dist_from-dist_to" band
        tempright = transect.buffer(-abs(dist_from), single_sided=True)  # create temporary buffer to subtract from the first
        rightbuf = rb.difference(tempright)  # create required polygons by subtracting unrequired area
        rightgdf = gpd.GeoDataFrame(gpd.GeoSeries(rightbuf))  # convert new geoseries to geodataframe
        rightgdf = rightgdf.rename(columns={0: 'geometry'}).set_geometry('geometry')  # set geometry of new geodataframe
        rightbuffer = rbjoin.set_geometry(rightgdf['geometry'])  # copy geometry from subtracted buffer to geodataframe to be exported
    if left and right:
        buffer = gpd.pd.merge(leftbuffer, rightbuffer, how='outer')
    elif not(left):
        buffer = rightbuffer
    else:
        buffer = leftbuffer
    return buffer

DB025 = distance_bands(test_transects, 0, 25)
DB25100 = distance_bands(test_transects, 25, 100)
DB100300 = distance_bands(test_transects, 100, 300)

DistanceBandsa = gpd.pd.merge(DB025, DB25100, how='outer')
DistanceBands = gpd.pd.merge(DistanceBandsa, DB100300, how='outer')
DistanceBands.to_file('Test_results/DistanceBands_test.shp')

