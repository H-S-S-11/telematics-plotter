import numpy as np
import pandas as pd
import geopandas as gpd
from shapely import geometry

def list_journeys(file):
    tel = pd.read_csv(file)
    journeys = []
    cols_to_drop = ['Journey ID']
    for id in tel['Journey ID'].unique():
        journey = tel[tel['Journey ID']==id].drop(cols_to_drop, axis=1)
        journeys.append(gpd.GeoDataFrame(journey, geometry=gpd.points_from_xy(journey.Longitude, journey.Latitude)))
    return journeys

def journey_title(journey):
    start = journey.head(1)
    end   = journey.tail(1)
    il, ih = start.index.values[0], end.index.values[0]
    ss, sc, st = str(start.loc[il, 'Street']), start.loc[il, 'City'], start.loc[il, 'GPS Date Time']
    es, ec, et = str(end  .loc[ih, 'Street']), end  .loc[ih, 'City'], end  .loc[ih, 'GPS Date Time']
    if ss=='nan': ss=''
    else: ss=ss+', '
    if es=='nan': es=''
    else: es=es+', '
    s = f'{ss}{sc} at {st}'
    e = f'{es}{ec} at {et}'
    return f'Journey from {s}\nto {e}'

def journey_line(journey):
    # Should change this so that journey isn't converted to GDF when read in
    # but instead changed straight to line here, to avoid deprecationWarning
    points = journey['geometry'].values 
    line = geometry.LineString(points)
    df = pd.DataFrame({'line' : [line]})
    return gpd.GeoDataFrame(df, geometry=df.line)

# At some point make a prepare_telematics function to delete leading lines