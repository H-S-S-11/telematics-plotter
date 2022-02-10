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

def journey_title(journey, late_threshold=19, early_threshold=5):
    start = journey.head(1)
    end   = journey.tail(1)
    il, ih = start.index.values[0], end.index.values[0]
    ss, sc, st = str(start.loc[il, 'Street']), start.loc[il, 'City'], start.loc[il, 'Event Time Stamp']
    es, ec, et = str(end  .loc[ih, 'Street']), end  .loc[ih, 'City'], end  .loc[ih, 'Event Time Stamp']
    end_time = pd.to_datetime(et)
    duration = end_time - pd.to_datetime(st)
    if ss=='nan': ss=''
    else: ss=ss+', '
    if es=='nan': es=''
    else: es=es+', '
    s = f'{ss}{sc} at {st}'
    e = f'{es}{ec} at {et}'
    name =  f'Journey from {s}\nto {e}'
    if duration > pd.Timedelta('01:00:00'):
        name = name + '\n(over 1 hour!)'
    if (end_time.hour > late_threshold) or (end_time.hour < early_threshold):
        name = name + '\n(driving late?)'
    return name

def journey_line(journey):
    # Should change this so that journey isn't converted to GDF when read in
    # but instead changed straight to line here, to avoid deprecationWarning
    points = journey['geometry'].values 
    line = geometry.LineString(points)
    df = pd.DataFrame({'line' : [line]})
    return gpd.GeoDataFrame(df, geometry=df.line)

def speeding(journey, mode='average', tolerance=0):
    if mode=='average':
        journey['average_speed'] = journey['Delta Trip Distance']/journey['Time Elapsed']
        # The above is in (100 m/s), multiply by 360 to get kph
        return journey[journey['average_speed']*360 > (journey['Road Speed Limit'] + tolerance)]
    elif mode=='peak':
        return journey[journey['Delta Max Speed'] > (journey['Road Speed Limit'] + tolerance)]

def harsh_braking(journey, threshold=8):
    names = []
    for n in range(threshold, 11):
        names.append(f'Delta Decelerations {n}')
    journey['harsh braking'] = journey.loc[:, names].sum(axis=1)
    return journey[journey['harsh braking'] != 0]

# At some point make a prepare_telematics function to delete leading lines