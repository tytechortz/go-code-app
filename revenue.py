import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import os
import geopandas as gpd 
from sodapy import Socrata
import json
import numpy as np
from datetime import datetime


app = dash.Dash()
app.config['suppress_callback_exceptions']=True

server = app.server

today = datetime.today()
current_year = today.year


client = Socrata("data.colorado.gov", None)

pop_results = client.get("q5vp-adf3", limit=381504)
mj_results = client.get("j7a3-jgd3", limit=6000)
biz_results = client.get("sqs8-2un5", limit=200000)

df_pop = pd.DataFrame.from_records(pop_results)
df_pop['totalpopulation'] = df_pop['totalpopulation'].astype(int)
df_pop = df_pop.drop(['age', 'malepopulation', 'femalepopulation'], axis=1)
df_pop = df_pop.groupby(['year', 'county'], as_index=False)['totalpopulation'].sum()
df_pop['county'] = df_pop['county'].str.upper()
df_pop['year'] = df_pop['year'].astype(int)
df_pop_pc = df_pop[(df_pop['year'] >= 2014) & (df_pop['year'] < current_year)]
# print(df_pop_pc)

df_revenue = pd.DataFrame.from_records(mj_results)
df_revenue['county'] = df_revenue['county'].str.upper()

df_revenue.fillna(0, inplace=True)
# print(df_revenue)

df_revenue['med_sales'] = df_revenue['med_sales'].astype(int)
df_revenue['rec_sales'] = df_revenue['rec_sales'].astype(int)

df_revenue['tot_sales'] = df_revenue['med_sales'] + df_revenue['rec_sales']
df_revenue = df_revenue.groupby(['year', 'county']).agg({'tot_sales': 'sum'})
# print(df_revenue)
df_revenue = df_revenue.reset_index()

# df_revenue['month'] = df_revenue['month'].astype(int)
# df_revenue['year'] = df_revenue['year'].astype(int)
df_revenue.loc[df_revenue['tot_sales'] > 0, 'color'] = 'red'
df_revenue.loc[df_revenue['tot_sales'] == 0, 'color'] = 'blue'
df_revenue['year'] = df_revenue['year'].astype(int)
# df_revenue = df_revenue.drop(['med_blank_code','rec_blank_code'], 1)

df_rev_pc = df_revenue[(df_revenue['year'] >= 2014) & (df_revenue['year'] < current_year)]
# print(df_rev_pc)
df_pc = pd.merge(df_rev_pc, df_pop, how='left', left_on=['county', 'year'], right_on=['county', 'year'])

df_pc.loc[df_pc['tot_sales'] > 0, 'color'] = 'red'
df_pc.loc[df_pc['tot_sales'] == 0, 'color'] = 'blue'
# print(df_pc)

# df['rev_per_cap'] = np.where(df['tot_sales'] == 0, 0, df['tot_sales'] / df['totalpopulation'])

# df['med_rev_pc'] = np.where(df['med_sales'] == 0, 0, df['med_sales'] / df['totalpopulation'])

# df['rec_rev_pc'] = np.where(df['rec_sales'] == 0, 0, df['rec_sales'] / df['totalpopulation'])

# df['Date'] = pd.to_datetime(df[['year', 'month']].assign(Day=1))
# df = df.set_index('Date')
# print(df)
# df = df.sort_values(['county', 'year', 'month'])

# print(df)
# print(df_revenue)
# print(df_revenue.columns)

with open('./Colorado_County_Boundaries.json') as json_file:
    jdata = json_file.read()
    topoJSON = json.loads(jdata)

sources=[]
for feat in topoJSON['features']: 
        sources.append({"type": "FeatureCollection", 'features': [feat]})


pop_rev = gpd.read_file('./per_cap_joined.geojson')

rpd = pop_rev.set_index('COUNTY', drop=False)
# print(rpd)
# print(rpd.columns)
# print(rpd)
# print(df_revenue)
# counties = gpd.read_file('./Colorado_County_Boundaries.geojson')
# with open('./Colorado_County_Boundaries.json') as json_file:
# # with open(counties) as json_file:
#     jdata = json_file.read()
#     topoJSON = json.loads(jdata)
    
# sources=[]
# for feat in topoJSON['features']: 
#         sources.append({"type": "FeatureCollection", 'features': [feat]})

counties = gpd.read_file('./Colorado_County_Boundaries.geojson')
counties.sort_values(by=['US_FIPS'])
# print(counties)
# print(counties.columns)
df_lat_lon = counties[['COUNTY', 'CENT_LAT', 'CENT_LONG']]
# print(df_lat_lon)

# df = pd.merge(df, df_lat_lon, how='left', left_on=['county'], right_on=['COUNTY'])
df_revenue = pd.merge(df_revenue, df_lat_lon, how='left', left_on=['county'], right_on=['COUNTY'])
# df_revenue = pd.concat([df_revenue, df_lat_lon])
# 
# print(df_revenue)

df_pc = pd.merge(df_pc, df_lat_lon, how='left', left_on=['county'], right_on=['COUNTY'])
df_pc['pc_rev'] = df_pc['tot_sales'] / df_pc['totalpopulation']
# print(sources)
df_biz = pd.DataFrame.from_records(biz_results)

df_biz['address'] = df_biz['street_address'] + ', ' + df_biz['city'] + ', ' + df_biz['zip']

# print(df_biz.head(20))



df_biz['year'] = df_biz['year'].astype(int)
df_biz['licensee'] = df_biz['licensee'].str.replace(',', '')
df_biz['licensee'] = df_biz['licensee'].str.upper()

# df_biz = df_biz[(df_biz['year'] > 2012) & df_biz['year'] < 2014]
# df_biz = df_biz[df_biz['year'] == 2014]

df_biz = df_biz.drop(['certification', 'street_address', 'dba'], axis=1)

df_biz['city_st'] = df_biz['city'] + ', CO'
# df_biz = df_biz.drop_duplicates(subset=['licensee'])
df_biz['zip'] = df_biz['zip'].replace(np.nan, 0)
# df_biz.to_csv('export_biz.csv')
df_biz['zip'] = df_biz['zip'].astype(int)

df_zip = pd.read_csv('./CO_zips.csv')
df_zip['zip'] = df_zip['Zip']

df_zip['zip'] = df_zip['zip'].replace(np.nan, 0)
df_zip['zip'] = df_zip['zip'].astype(int)

df_biz = df_biz.merge(df_zip, on=['zip', 'zip'], how='left')
df_biz = df_biz.drop(['City', 'Zip'], axis=1)


# df_biz = df_biz.groupby(['County', 'year'])['licensee'].count().reset_index()
df_biz = df_biz.groupby(['County', 'year'])['licensee'].nunique().reset_index()
print(df_biz)

df_biz['County'] = df_biz['County'].str.upper()

# print(df_biz)



counties_list = []

for i in df_pop.county.unique():
     counties_list.append(i)

color_list = ['purple', 'darkblue', 'dodgerblue', 'darkgreen','black','lightgreen','yellow','orange', 'darkorange','red','darkred','violet']

def revenue_App():
     return html.Div([
               html.Div([
                    html.H4(
                         'COLORADO CANNABIS REVENUE',
                         className='twelve columns',
                         style={'text-align': 'center'}
                    )
               ],
                    className='row'
               ),
               html.Div([
                    html.H4(
                         'County Population and Projected Growth',
                         className='twelve columns',
                         style={'text-align': 'center'}
                    )
               ],
                    className='row'
               ),
               html.Div([
                    html.Div([
                         html.Div([
                              dcc.RadioItems(
                                   id='tot-per-select',
                                   options=[
                                        {'label':'Total Revenue',
                                        'value':'tot-rev'},
                                        {'label':'Per Capita Revenue',
                                        'value':'per-cap'},
                                        {'label':'Annual Rev Change',
                                        'value':'ann-rev-chng'},
                                   ],
                                   labelStyle={'display':'inline-block'},
                                   value='tot-rev'
                                   ),
                         ],
                              className='eight columns'
                         ),
                    ],
                         className='eight columns'
                    ),
               ],
                    className='row'
               ),
               html.Div([
                    html.Div([
                         html.Div([
                              dcc.Graph('revenue-map')
                         ],
                              className='twelve colums'
                         ),
                    ],
                         className='eight columns'
                    ),
               ],
                    className='row'
               ),
               
               html.Div([
                    html.Div([
                         dcc.Slider(
                                   id='year2',
                                   min=2014,
                                   max=2020,
                                   step=1,
                                   marks={x: '{}'.format(x) for x in range(2014, 2020)},
                                   value=2014
                              ),
                    ],
                         className='eight columns'
                    ),
               ],
                    className='row'
               ),
               html.Div([
                    html.Div([
                         html.Div([
                              dcc.RadioItems(
                                   id='graph-selector',
                                   options=[
                                        {'label':'Pop',
                                        'value':'pop'},
                                        {'label':'Bus',
                                        'value':'rev'},
                                   ],
                                   labelStyle={'display':'inline-block'},
                                   value='pop'
                                   ),
                         ],
                              className='eight columns'
                         ),
                    ],
                         className='eight columns'
                    ),

               ],
                    className='row'
               ),
               html.Div(id='pop-rev-controls'),
               html.Div([
                    html.Div([
                         html.Div([
                              dcc.Graph(
                                   id='county-pop-rev-graph'),
                         ],
                              className='seven columns'
                         ),
                              html.Div([
                                   html.Div([
                                        html.Div(id='pop-rev-stats') 
                                        ],
                                             className='round1'
                                        ), 
                              ],
                                   className='four columns'
                              ),
                         ],
                              className='twelve columns'
                         ),
               ],
                    className='row'
               ),
               html.Div(id='pop-rev-graph-selection', style={'display': 'none'}),
     ])

app.layout = revenue_App