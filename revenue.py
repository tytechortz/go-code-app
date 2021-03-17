import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import os
from sodapy import Socrata

app = dash.Dash()
app.config['suppress_callback_exceptions']=True

server = app.server

client = Socrata("data.colorado.gov", None)

results = client.get("q5vp-adf3", limit=381504)

df_pop = pd.DataFrame.from_records(results)

df_pop['totalpopulation'] = df_pop['totalpopulation'].astype(int)

df_pop = df_pop.drop(['age', 'malepopulation', 'femalepopulation'], axis=1)
df_pop = df_pop.groupby(['year', 'county'], as_index=False)['totalpopulation'].sum()
print(df_pop.tail())

counties = []

for i in df_pop.county.unique():
     counties.append(i)

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
                         dcc.Dropdown(
                                   id='county',
                                   options=[{'label':i, 'value':i} for i in counties],
                                   value='Denver'
                              ),
                    ],
                         className='three columns'
                    ),
               ],
                    className='row'
               ),
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