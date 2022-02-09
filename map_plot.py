import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import shapely.affinity as aff

from collect_roads import *
from read_telematics import *

b_roads = True
telematics_file = 'example_telematics.csv'
# Roughly corresponds to minutes
min_journey = 5

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
uk = world[world.name == 'United Kingdom']

# OS road data uses British National Grid coordinates https://britishnationalgrid.uk
road = get_roads('SU', '../oproad_essh_gb/data/', b_roads=b_roads)

journeys = list_journeys('example_telematics.csv')

for journey in journeys:
    if len(journey.index) > min_journey:
        journey_name = journey_title(journey)
        ax = uk.plot(color='white', edgecolor='black')
        road[road['class']=='Motorway'].plot(ax=ax, color='blue')
        road[road['class']=='A Road'  ].plot(ax=ax, color='green')
        if b_roads:
            road[road['class']=='B Road'  ].plot(ax=ax, color='grey')
        journey_line(journey).plot(ax=ax, color='red')
        plt.title(journey_name)

plt.show()