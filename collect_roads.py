import pandas as pd
import geopandas as gpd
import shapely.affinity as aff
import os

def read_road(file, b_roads=True):
    cols_to_drop = ['fictitious', 'identifier', 'name1', 'name1_lang', 'name2', 'name2_lang', 'numberTOID', 'nameTOID', 'startNode', 'endNode', 'loop', 'structure', 'primary', 'trunkRoad']
    road = road = gpd.read_file(file).drop(cols_to_drop, axis=1)
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