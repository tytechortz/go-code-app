import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import os

app = dash.Dash()
app.config['suppress_callback_exceptions']=True

server = app.server

df_pop = pd.read_csv('pop.csv')

counties = []

for i in df_pop.county.unique():
     counties.append(i)



# def revenue_App():
#      return html.Div([
#                html.Div([
#                     html.Div([
#                          html.H2(
#                               'COLORADO CANNABIS',
#                          )
#                     ],
#                          className='twelve colums'
#                     ),
#                ],
#                     className='row'
#                ),
#                html.Div([
#                     html.Div([
#                          html.Div([
#                               dcc.Graph(
#                                    id='county-pop-graph',
#                               ),
#                          ]),
#                          html.Div([
#                               dcc.Dropdown(
#                                    id='county',
#                                    options=[{'label':i, 'value':i} for i in counties],
#                               ),
#                          ])
#                     ],
#                          className='twelve columns'
#                     ),
#                ],
#                     className='row'
#                ),
#      ])

# app.layout = revenue_App