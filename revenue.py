import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import os
import geopandas as gpd 
from sodapy import Socrata
import json
import numpy as np

app = dash.Dash()
app.config['suppress_callback_exceptions']=True

server = app.server

client = Socrata("data.colorado.gov", None)

pop_results = client.get("q5vp-adf3", limit=381504)
mj_results = client.get("j7a3-jgd3", limit=6000)

df_pop = pd.DataFrame.from_records(pop_results)
df_pop['totalpopulation'] = df_pop['totalpopulation'].astype(int)
df_pop = df_pop.drop(['age', 'malepopulation', 'femalepopulation'], axis=1)
df_pop = df_pop.groupby(['year', 'county'], as_index=False)['totalpopulation'].sum()
df_pop['county'] = df_pop['county'].str.upper()

df_revenue = pd.DataFrame.from_records(mj_results)
df_revenue['county'] = df_revenue['county'].str.upper()

df_revenue.fillna(0, inplace=True)

df_revenue['med_sales'] = df_revenue['med_sales'].astype(int)
df_revenue['rec_sales'] = df_revenue['rec_sales'].astype(int)
df_revenue['tot_sales'] = df_revenue['med_sales'] + df_revenue['rec_sales']
df_revenue.loc[df_revenue['tot_sales'] > 0, 'color'] = 'red'
df_revenue.loc[df_revenue['tot_sales'] == 0, 'color'] = 'blue'
df_revenue = df_revenue.drop(['med_blank_code','rec_blank_code'], 1)

df = pd.merge(df_revenue, df_pop, how='left', left_on=['county', 'year'], right_on=['county', 'year'])

df['rev_per_cap'] = np.where(df['tot_sales'] == 0, 0, df['tot_sales'] / df['totalpopulation'])

df['med_rev_pc'] = np.where(df['med_sales'] == 0, 0, df['med_sales'] / df['totalpopulation'])

df['rec_rev_pc'] = np.where(df['rec_sales'] == 0, 0, df['rec_sales'] / df['totalpopulation'])

df['Date'] = pd.to_datetime(df[['year', 'month']].assign(Day=1))

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

# print(sources)
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
                         dcc.RangeSlider(
                                   id='year',
                                   min=1990,
                                   max=2050,
                                   step=1,
                                   # options=[{'label':x, 'value':x} for x in range(2022, 2050)],
                                   value=[2021,2050]
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
                                   min=1990,
                                   max=2050,
                                   step=1,
                                   # options=[{'label':x, 'value':x} for x in range(2022, 2050)],
                                   value=2021
                              ),
                    ],
                         className='eight columns'
                    ),
               ],
                    className='row'
               ),
               # html.Div([
               #      html.Div([
               #           dcc.Dropdown(
               #                     id='county',
               #                     options=[{'label':i, 'value':i} for i in counties_list],
               #                     value='Denver'
               #                ),
               #      ],
               #           className='three columns'
               #      ),
               # ],
               #      className='row'
               # ),
               html.Div([
                    html.Div([
                         html.Div([
                              dcc.Graph(
                                   id='county-pop-graph'),
                         ],
                              className='eight columns'
                         ),
                              html.Div([
                                   html.Div([
                                        html.Div(id='pop-stats') 
                                        ],
                                             className='round1'
                                        ), 
                              ],
                                   className='three columns'
                              ),
                         ],
                              className='twelve columns'
                         ),
               ],
                    className='row'
               ),
     ])

app.layout = revenue_App