import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import shapely.affinity as aff

from collect_roads import *
from read_telematics import *

roads = False
b_roads = True
small_roads = True
telematics_file = 'example_telematics.csv'
# Roughly corresponds to minutes
min_journey = 5

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
uk = world[world.name == 'United Kingdom']

if roads:
    # OS road data uses British National Grid coordinates https://britishnationalgrid.uk
    road = get_roads('SU', '../oproad_essh_gb/data/', b_roads=b_roads, small_roads=small_roads)

journeys = list_journeys('example_telematics.csv')

for journey in journeys:
    if len(journey.index) > min_journey:
        # Journey flagged as possibly late if it ends after late_threshold or before early_threshold
        # Times are hours in 24hr clock
        journey_name = journey_title(journey, late_threshold=19, early_threshold=6)

        ax = uk.plot(color='white', edgecolor='black')
        if roads:
            plot_roads(ax, road, b_roads=b_roads, small_roads=small_roads)
        journey_line(journey).plot(ax=ax, color='purple')
        speeding(journey, mode='peak',    tolerance=0).plot(ax=ax, color='yellow')
        speeding(journey, mode='average', tolerance=0).plot(ax=ax, color='orange')
        harsh_braking(journey, threshold=8).plot(ax=ax, color='red')
        plt.title(journey_name)

plt.show()

# Maybe try grouping journeys by day?