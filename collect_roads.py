import pandas as pd
import geopandas as gpd
import shapely.affinity as aff
import os

tile_transformations = {
    'SU' : (1.447080e-5, 0.887500e-5, -7.800128, 49.912384),
}

def download_roads():
    import requests
    url = "https://api.os.uk/downloads/v1/products/OpenRoads/downloads?area=GB&format=ESRI%C2%AE+Shapefile&redirect"
    r = requests.get(url, allow_redirects=True)
    open('OSopenRoads.zip', 'wb').write(r.content)
    import zipfile
    with zipfile.ZipFile('OSopenRoads.zip', 'r') as zip:
        zip.extractall('OSopenRoads')

def reference_points():
    # Use these to work out suitable tile transformations
    ref = pd.DataFrame(
    {'Reference': ['Southampton', 'Farnborough'],
     'Latitude': [50.949497, 51.317733 ],
     'Longitude': [-1.371054, -0.759332]})
    return gpd.GeoDataFrame(ref, geometry=gpd.points_from_xy(ref.Longitude, ref.Latitude))

def read_road(file, b_roads=True, small_roads=False):
    cols_to_drop = ['fictitious', 'identifier', 'name1', 'name1_lang', 'name2', 'name2_lang', 'numberTOID', 'nameTOID', 'startNode', 'endNode', 'loop', 'structure', 'primary', 'trunkRoad']
    road = road = gpd.read_file(file).drop(cols_to_drop, axis=1)
    if not small_roads:
        road = road[(road['class']!='Unclassified') & (road['class']!='Unknown') & (road['class']!='Classified Unnumbered') & (road['class']!='Not Classified')]
    if not b_roads:
        road = road[(road['class']!='B Road')]
    return road

def all_links(dir):
    roads = []
    for root, dirs, files in os.walk(dir):
        for file in files:     
            if file.endswith('RoadLink.shp'):
                roads.append(read_road(root+'/'+str(file)))
    return roads

def road_transform(road_segment, xscale, yscale, xoff, yoff):
    return aff.translate(aff.scale(road_segment, xfact=xscale, yfact=yscale, origin=(0,0,0)), xoff=xoff, yoff=yoff)

def get_roads(tile, folder, b_roads=True, small_roads=False):
    road = read_road(folder+tile+'_RoadLink.shp', b_roads=b_roads, small_roads=small_roads)
    road['geometry'] = road['geometry'].apply(road_transform, args=tile_transformations[tile])
    return road

def plot_roads(ax, road, b_roads=False, small_roads=False):
    road[road['class']=='Motorway'].plot(ax=ax, color='blue')
    road[road['class']=='A Road'  ].plot(ax=ax, color='green')
    if b_roads:
        road[road['class']=='B Road'  ].plot(ax=ax, color='dimgrey')
    if small_roads:
        road[(road['class']!='Motorway') & (road['class']!='A Road') & (road['class']!='B Road')].plot(ax=ax, color='darkgrey')

if __name__=="__main__":
    
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    uk = world[world.name == 'United Kingdom']
    ax = uk.plot(color='white', edgecolor='black')

    road = get_roads('SU', 'OSopenRoads/data/', b_roads=False)
    gref = reference_points()
    gref.plot(ax=ax, color='red')
    plot_roads(ax, road, b_roads=False, small_roads=False)
    # road[road['class']=='Motorway'].plot(ax=ax, color='blue')
    # road[road['class']=='A Road'  ].plot(ax=ax, color='green')
    # road[road['class']=='B Road'  ].plot(ax=ax, color='grey')