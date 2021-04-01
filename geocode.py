from sodapy import Socrata
import json
import pandas as pd
# from pygeocoder import Geocoder
import geopandas as gpd
from shapely.geometry import Point
from geopandas.tools import geocode
from geopy.geocoders import Nominatim
import geocoder
import requests
import numpy as np

client = Socrata("data.colorado.gov", None)


results = client.get("sqs8-2un5", limit=200000)

# Geocoder.geocode("4207 N Washington Ave, Douglas, AZ 85607").valid_address
# fp = results

data = pd.DataFrame.from_records(results)

data['address'] = data['street_address'] + ', ' + data['city'] + ', ' + data['zip']

# print(data['year'])

data['year'] = data['year'].astype(int)
print(data.columns)
data = data[(data['year'] > 2013) & data['year'] < 2016]
# df = data[data['year'] == 2015]

df = data.drop(['certification', 'license_no', 'street_address', 'dba'], axis=1)

df['city_st'] = df['city'] + ', CO'

df = df.drop_duplicates(subset=['licensee'])
print(df.head())
print(df.shape)

# df['county'] = geocoder.google(df['city_st'])

print(df.head())

# df.to_csv('export_csv.csv', header=True)
df_zip = pd.read_csv('./CO_zips.csv')
df_zip['zip'] = df_zip['Zip']
print(df_zip)
df_zip['zip'] = df_zip['zip'].replace(np.nan, 0)
df['zip'] = df['zip'].replace(np.nan, 0)
# print(df_zip[df_zip['zip'].isnull()])
df_zip['zip'] = df_zip['zip'].astype(int)
df['zip'] = df['zip'].astype(int)

df = df.merge(df_zip, on=['zip', 'zip'], how='left')
df = df.drop(['City', 'Zip'], axis=1)
print(df)
df = df.groupby(['County', 'year'])['licensee'].count().reset_index()
print(df)

# df_sunrise = df[df['licensee'] == 'SUNRISE SOLUTIONS, LLC']
# print(df_sunrise)
# # data = data[:10]
# # print(df)
# df_count = df.groupby('category').nunique()
# print(df_count)
# location = [x for x in df['address'].unique().tolist() 
#             if type(x) == str]
# latitude = []
# longitude =  []
# for i in range(0, len(location)):
#      try:
#         address = location[i] 
#         geolocator = Nominatim(user_agent="go_code_app")
#         loc = geolocator.geocode(address)
#         latitude.append(loc.latitude)
#         longitude.append(loc.longitude)
#      #    print('The geographical coordinate of location are {}, {}.'.format(loc.latitude, loc.longitude))
#      except:
#         # in the case the geolocator does not work, then add nan element to list
#         # to keep the right size
#         latitude.append(np.nan)
#         longitude.append(np.nan)

# df_ = pd.DataFrame({'address':location, 'loc_lat': latitude, 'loc_lon':longitude})

# new_df = df.merge(df_, on='address', how='left')
# print(new_df)


# geolocator = Nominatim(user_agent="go_code_app")
# geolocator = Nominatim(user_agent='go_code_app')
# ladd1 = data
# location = geolocator.geocode(ladd1)
# df['gcode'] = data.address.apply(geolocator.geocode)

# print(location.latitude)
# print(data.head(2))