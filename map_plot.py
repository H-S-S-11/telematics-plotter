import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import shapely.affinity as aff

from collect_roads import *
from read_telematics import *

roads = False
b_roads = True
small_roads = False
telematics_file = 'example_telematics.csv'
mode = 'average_speed'
# Roughly corresponds to minutes
min_journey = 5

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
uk = world[world.name == 'United Kingdom']

road = None
if roads:
    # OS road data uses British National Grid coordinates https://britishnationalgrid.uk
    road = get_roads('SU', 'OSopenRoads/data/', b_roads=b_roads, small_roads=small_roads)

journeys = list_journeys('example_telematics.csv')

# 3D plot with average speed? (Linestring Z)
for journey in journeys:
    if len(journey.index) > min_journey:
        # Journey flagged as possibly late if it ends after late_threshold or before early_threshold
        # Times are hours in 24hr clock
        journey_name = journey_title(journey, late_threshold=19, early_threshold=6)

        plot_journey(journey, mode=mode, uk=uk, road=road,
            roads=roads, b_roads=b_roads, small_roads=small_roads)
        plt.title(journey_name)

plt.show()

# Maybe try grouping journeys by day?