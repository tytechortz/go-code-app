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

pop_results = client.get("q5vp-adf3", limit=381504)
mj_results = client.get("j7a3-jgd3", limit=6000)
df_pop = pd.DataFrame.from_records(pop_results)
df_pop['totalpopulation'] = df_pop['totalpopulation'].astype(int)
df_pop = df_pop.drop(['age', 'malepopulation', 'femalepopulation'], axis=1)
df_pop = df_pop.groupby(['year', 'county'], as_index=False)['totalpopulation'].sum()

df_revenue = pd.DataFrame.from_records(mj_results)

print(df_revenue)


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
          
     ])

app.layout = revenue_App