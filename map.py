import plotly.express as px
import pandas as pd
from sodapy import Socrata
import dash
import geopandas as gpd 
import json
from urllib.request import urlopen
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import os


app = dash.Dash(__name__)

app.config['suppress_callback_exceptions']=True

server = app.server

client = Socrata("data.colorado.gov", None)
pop_results = client.get("q5vp-adf3", limit=381504)
mj_results = client.get("j7a3-jgd3", limit=6000)

with open('./Colorado_County_Boundaries.json') as json_file:
    jdata = json_file.read()
    topoJSON = json.loads(jdata)

sources=[]
for feat in topoJSON['features']: 
        sources.append({"type": "FeatureCollection", 'features': [feat]})

pop_rev = gpd.read_file('./per_cap_joined.geojson')

rpd = pop_rev.set_index('COUNTY', drop=False)

counties = gpd.read_file('./Colorado_County_Boundaries.geojson')
# print(counties)

# counties_s = counties.sort_values(by=['US_FIPS'])

df_pop = pd.DataFrame.from_records(pop_results)
df_pop['totalpopulation'] = df_pop['totalpopulation'].astype(int)
df_pop = df_pop.drop(['age', 'malepopulation', 'femalepopulation'], axis=1)
df_pop = df_pop.groupby(['year', 'county'], as_index=False)['totalpopulation'].sum()
df_pop['county'] = df_pop['county'].str.upper()
df_pop['year'] = df_pop['year'].astype(int)
print(df_pop)

df_revenue = pd.DataFrame.from_records(mj_results)
df_revenue['county'] = df_revenue['county'].str.upper()

df_revenue.fillna(0, inplace=True)
# print(df_revenue)

df_revenue['med_sales'] = df_revenue['med_sales'].astype(int)
df_revenue['rec_sales'] = df_revenue['rec_sales'].astype(int)

df_revenue['tot_sales'] = df_revenue['med_sales'] + df_revenue['rec_sales']
df_revenue = df_revenue.groupby(['year', 'county']).agg({'tot_sales': 'sum'})

df_revenue = df_revenue.reset_index()
# print(df_revenue)
# df_revenue['month'] = df_revenue['month'].astype(int)
# df_revenue['year'] = df_revenue['year'].astype(int)
df_revenue.loc[df_revenue['tot_sales'] > 0, 'color'] = 'red'
df_revenue.loc[df_revenue['tot_sales'] == 0, 'color'] = 'blue'

counties = gpd.read_file('./Colorado_County_Boundaries.geojson')
counties.sort_values(by=['US_FIPS'])
# print(counties)
# print(counties.columns)
df_lat_lon = counties[['COUNTY', 'CENT_LAT', 'CENT_LONG']]
# print(df_lat_lon)

# df = pd.merge(df, df_lat_lon, how='left', left_on=['county'], right_on=['COUNTY'])
df_revenue = pd.merge(df_revenue, df_lat_lon, how='left', left_on=['county'], right_on=['COUNTY'])


def get_layout():
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
                         dcc.Slider(
                                   id='month',
                                   min=1,
                                   max=12,
                                   step=1,
                                   # options=[{'label':x, 'value':x} for x in range(2022, 2050)],
                                   value=1
                              ),
                    ],
                         className='eight columns'
                    ),
               ],
                    className='row'
               ),
               
     ])

@app.callback(
     Output('revenue-map', 'figure'),
     [Input('year2', 'value'),
     Input('month', 'value')])         
def update_rev_map(selected_year, selected_month):
    
     year1 = selected_year
   
     rpd_s = rpd.sort_values(by=['RId2'])
     # print(rpd_s)
     rpd_s = rpd_s.apply(pd.to_numeric, errors='ignore')
     rpd_s = rpd_s.fillna(0)

     counties_s = counties.sort_values(by=['US_FIPS'])
     # print(df_revenue)
    
     df_year = df_revenue.loc[df_revenue['year'] == str(selected_year)] 
     # print(df_year)

     df_smr = pd.DataFrame({'county': df_year['county'], 'year': df_year.year, 'total': df_year.tot_sales,'CENT_LAT':df_year.CENT_LAT,
                    'CENT_LON':df_year.CENT_LONG, 'marker_size':(df_year.tot_sales)*(.2**9.5)})
     
     df_smr_filtered = df_smr.loc[df_year['color'] == 'red']

     color_counties = df_smr_filtered['county'].unique().tolist()
     
     def fill_color():
          for k in range(len(sources)):
               if sources[k]['features'][0]['properties']['COUNTY'] in color_counties:
                    sources[k]['features'][0]['properties']['COLOR'] = 'lightgreen'
               else: sources[k]['features'][0]['properties']['COLOR'] = 'white'                 
     fill_color()

    
     layers=[dict(sourcetype = 'json',
          source =sources[k],
          below="water", 
          type = 'fill',
          color = sources[k]['features'][0]['properties']['COLOR'],
          opacity = 0.5
          ) for k in range(len(sources))]
     data = [dict(
          lat = df_smr['CENT_LAT'],
          lon = df_smr['CENT_LON'],
          text = df_smr['county'],
          hoverinfo = 'text',
          type = 'scattermapbox',
          #    customdata = df['uid'],
          marker = dict(size=df_smr['marker_size'],color='forestgreen',opacity=.5),
          )]
     layout = dict(
               mapbox = dict(
                    accesstoken = os.environ.get("mapbox_token"),
                    center = dict(lat=39.05, lon=-105.5),
                    zoom = 5.85,
                    style = 'light',
                    layers = layers
               ),
               hovermode = 'closest',
               height = 450,
               margin = dict(r=0, l=0, t=0, b=0)
               )
     fig = dict(data=data, layout=layout)
     return fig

app.layout = get_layout

if __name__ == '__main__':
    app.run_server(port=8080, debug=True)