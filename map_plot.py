import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import shapely.affinity as aff

from collect_roads import *


ref = pd.DataFrame(
    {'Reference': ['Southampton', 'Camberly'],
     'Latitude': [50.949497, 51.317762 ],
     'Longitude': [-1.371054, -0.759275]})
gref = gpd.GeoDataFrame(
    ref, geometry=gpd.points_from_xy(ref.Longitude, ref.Latitude))


world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
ax = world[world.name == 'United Kingdom'].plot(color='white', edgecolor='black')

# OS road data uses British National Grid coordinates https://britishnationalgrid.uk
road = read_road('../oproad_essh_gb/data/SU_RoadLink.shp', b_roads=False)


road['geometry'] = road['geometry'].apply(road_transform, args=(1.427e-5, 0.897e-5, -7.710944, 49.901267))

gref.plot(ax=ax, color='red')
road[road['class']=='Motorway'].plot(ax=ax, color='blue')
road[road['class']=='A Road'  ].plot(ax=ax, color='green')
#road[road['class']=='B Road'  ].plot(ax=ax, color='grey')
plt.show()