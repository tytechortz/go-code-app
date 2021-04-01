import dash
import pandas as pd
import numpy as np
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
from homepage import Homepage
from revenue import revenue_App, df_pop, rpd, counties, df_revenue, sources, df_pc, df_biz
import os
from dotenv import load_dotenv
import plotly.graph_objects as go
from plotly.subplots import make_subplots


load_dotenv()

# require('dotenv').config()

app = dash.Dash()
application = app.server
app.config.suppress_callback_exceptions = True


# df = pd.read_csv('pop.csv')

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div([
    dcc.Location(id = 'url', refresh = False),
    html.Div(id = 'page-content')
])

# @app.callback(
#      Output('county-pop-graph', 'figure'),
#      [Input('revenue-map', 'clickData'),
#      Input('year', 'value')])
# def display_cnty_pop(clickData, selected_year):
     # county = clickData['points'][-1]['text']
     # df_rev = df_revenue[df_revenue['county'] == county]
     # df_rev = df_rev[df_rev['year'] < 2021]
#      # print(df_rev)
#      # print(clickData)
     
#      # print(county)
#      df_county_pop = df_pop[df_pop['county'] == county]
#      # print(df_county_pop)
#      # print(selected_year)

#      df_county_pop_range = df_county_pop[(df_county_pop['year'] >= 2014) & (df_county_pop['year'] <= selected_year[1])]

#      fig = make_subplots(specs=[[{"secondary_y":True}]])

     # fig.add_trace(
     #      go.Scatter(x=[1, 2, 3], y=[40, 50, 60], name="yaxis data"),
     #      secondary_y=False,
     # )

     # years = [2014, 2015, 2016, 2017, 2018, 2019, 2020]

     

     # fig.add_trace(
     #      go.Scatter(x=df_county_pop_range['year'], y=df_county_pop_range['totalpopulation'], name="yaxis2 data"),
     #      secondary_y=True,
     # )

     # fig.add_trace(
     #      go.Scatter(x=df_county_pop_range['year'], y=df_rev['tot_sales'], name="yaxis data"),
     #      secondary_y=False,
     # )


     
     # # trace1 = go.Bar(x=df_rev['tot_sales'],
     # #                 y=df_rev['year'])

     

     # # df_county_pop_range = df_county_pop[(df_county_pop['year'] >= selected_year[0]) & (df_county_pop['year'] <= selected_year[1])]
     # # print(df_county_pop_range)
     
     # # fig = px.bar(df_county_pop_range, x='year', y='totalpopulation')

     # return fig

@app.callback(Output('pop-rev-controls', 'children'),
            [Input('graph-selector', 'value')])
def display_pop_rev(pop_rev_choice):
     if  pop_rev_choice == 'pop' or 'rev':
          return html.Div([
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
               html.Div([
                    html.Div([
                         dcc.RangeSlider(
                                   id='year',
                                   min=1990,
                                   max=2050,
                                   step=1,
                                   # options=[{'label':x, 'value':x} for x in range(2022, 2050)],
                                   value=[2014,2020]
                              ),
                    ],
                         className='eight columns'
                    ),
               ],
                    className='row'
               ),
          ]),
     elif pop_rev_choice == 'rev':
          return html.H1('Else')

@app.callback(Output('page-content', 'children'),
            [Input('url', 'pathname')])
def display_page(pathname):
     if pathname == '/revenue':
          return revenue_App()
     else:
          return Homepage()   
          

@app.callback(
    Output('county-selector', 'children'),
    [Input('counties', 'value')])
def display_month_selector(county):
     
     return html.P('Select County', style={'text-align': 'center'}), html.Div([
          dcc.Dropdown(id='county'),
     ],
          className='pretty_container'
     )

@app.callback(
    Output('pop-rev-graph-selection', 'children'),
    [Input('graph-selector', 'value')])
def display_pop_rev_graph(pop_rev):
     if pop_rev == 'pop':
          return 'pop'
     else:
          return 'rev'
     # return html.P('Select County', style={'text-align': 'center'}), html.Div([
     #      dcc.Dropdown(id='county'),
     # ],
     #      className='pretty_container'
     # ),


# @app.callback(
#      Output('county-pop-rev-graph', 'figure'),
#      [Input('revenue-map', 'clickData'),
#      Input('year', 'value'),
#      Input('pop-rev-graph-selection', 'children')])
# def display_cnty_pop(clickData, selected_year, pop_rev):
#      print(pop_rev)
#      if pop_rev == 'pop':
#           if clickData is None:
#                county = 'DENVER'
#           else:
#                county = clickData['points'][-1]['text']
#           # print(county)
#           df_county_pop = df_pop[df_pop['county'] == county]
#           # print(df_county_pop)
#           # print(selected_year)
#           df_county_pop_range = df_county_pop[(df_county_pop['year'] >= selected_year[0]) & (df_county_pop['year'] <= selected_year[1])]
#           # print(df_county_pop_range)
          
#           fig = px.bar(df_county_pop_range, x='year', y='totalpopulation')

#           return fig
#      else:
#           if clickData is None:
#                county = 'DENVER'
#           else:
#                county = clickData['points'][-1]['text']
#           df_rev = df_revenue[df_revenue['county'] == county]
#           df_rev = df_rev[df_rev['year'] < 2021]

#           fig = px.bar(df_rev, x='year', y='tot_sales')

#           return fig

@app.callback(
     Output('county-pop-rev-graph', 'figure'),
     [Input('revenue-map', 'clickData'),
     Input('year', 'value'),
     Input('pop-rev-graph-selection', 'children')])
def display_cnty_pop(clickData, selected_year, pop_rev):
     county = clickData['points'][-1]['text']
     df_rev = df_revenue[df_revenue['county'] == county]
     df_rev = df_rev[df_rev['year'] < 2021]
     print(df_rev)
     # print(clickData)
     # print(county)
     df_county_pop = df_pop[df_pop['county'] == county]
     df_county_pop = df_county_pop[(df_county_pop['year'] >= selected_year[0]) & (df_county_pop['year'] <= selected_year[1])]

     print(df_biz)
     print(type(df_biz))

     # df_biz_count = df_biz.get_group('Adams')
     df_biz_count = df_biz[df_biz['County'] == county]
     # df_biz_count = df_biz['year'] <= 2021
     print(df_biz_count)
     # print(selected_year)

     fig = go.Figure(
          data=[
               go.Bar(
                    name='Annual Revenue',
                    x=df_rev['year'],
                    y=df_rev['tot_sales'],
                    yaxis='y',
                    offsetgroup=1
               ),
               # go.Bar(
               #      name='Population',
               #      x=df_county_pop['year'],
               #      y=df_county_pop['totalpopulation'],
               #      yaxis='y2',
               #      offsetgroup=2
               # ),
               go.Bar(
                    name='Business Count',
                    x=df_biz_count['year'],
                    y=df_biz_count['licensee'],
                    yaxis='y2',
                    offsetgroup=2
               ),
          ],
          layout={
               'yaxis': {'title': 'Population'},
               'yaxis2': {'title': 'Revenue', 'overlaying': 'y', 'side': 'right'}
          }
     )
     # fig = make_subplots(specs=[[{"secondary_y":True}]])


     # fig.add_trace(go.Bar(x=years,
     #            y=[219, 146, 112, 127, 124, 180, 236, 207, 236, 263,
     #               350, 430, 474, 526, 488, 537, 500, 439],
     #            name='Rest of world',
     #            marker_color='rgb(55, 83, 109)'
     #            ))
     # fig.add_trace(go.Bar(x=years,
     #            y=[16, 13, 10, 11, 28, 37, 43, 55, 56, 88, 105, 156, 270,
     #               299, 340, 403, 549, 499],
     #            name='China',
     #            marker_color='rgb(26, 118, 255)'
     #            ))

     # fig.add_trace(go.Bar(
     #      x=df_rev['year'],
     #      y=df_rev['tot_sales'],
     #      name="Annual Revenue",
     # ))

     # fig.add_trace(go.Bar(
     #      x=df_county_pop['year'],
     #      y=df_county_pop['totalpopulation'],
     #      name='Population',
     # ))


     
     fig.update_layout(barmode='group')
     # fig.show()


     # trace1 = go.Bar(x=df_rev['tot_sales'],
     #                 y=df_rev['year'])



     # df_county_pop_range = df_county_pop[(df_county_pop['year'] >= selected_year[0]) & (df_county_pop['year'] <= selected_year[1])]
     # print(df_county_pop_range)

     # fig = px.bar(df_county_pop_range, x='year', y='totalpopulation')

     return fig
     







     if pop_rev == 'pop':
          if clickData is None:
               county = 'DENVER'
          else:
               county = clickData['points'][-1]['text']
          # print(county)
          df_county_pop = df_pop[df_pop['county'] == county]
          # print(df_county_pop)
          # print(selected_year)
          df_county_pop_range = df_county_pop[(df_county_pop['year'] >= selected_year[0]) & (df_county_pop['year'] <= selected_year[1])]
          # print(df_county_pop_range)
          
          fig = px.bar(df_county_pop_range, x='year', y='totalpopulation')

          return fig
     else:
          if clickData is None:
               county = 'DENVER'
          else:
               county = clickData['points'][-1]['text']
          df_rev = df_revenue[df_revenue['county'] == county]
          df_rev = df_rev[df_rev['year'] < 2021]

          fig = px.bar(df_rev, x='year', y='tot_sales')

          return fig


@app.callback(
     Output('pop-stats', 'children'),
     [Input('revenue-map', 'clickData'),
     Input('year', 'value')])
def county_pop_stats(clickData, selected_year):
     if clickData is None:
          county = 'DENVER'
     else:
          county = clickData['points'][-1]['text']
     # print(selected_year)
     # print(df_pop)
     # print(selected_year[0])
     current_year = df_pop['year'] == selected_year[0]
     # print(current_year)
     projected_year = df_pop['year'] == selected_year[1]
     
     # print(county)
     selected_county = df_pop['county'] == county
     # print(selected_county)
     current_pop = df_pop[current_year & selected_county]
     selected_year_pop = df_pop[projected_year & selected_county]
     # print(selected_year_pop)
     if selected_year_pop.iloc[-1][-1] > current_pop.iloc[-1][-1]:
          pop_change = (selected_year_pop.iloc[-1][-1] - current_pop.iloc[-1][-1]) / current_pop.iloc[-1][-1]
     else:
          pop_change = -((current_pop.iloc[-1][-1] - selected_year_pop.iloc[-1][-1]) / current_pop.iloc[-1][-1])
     # print(pop_2050)
     return html.Div([
               html.Div('{} County Pop. Stats'.format(county), style={'text-align':'center'}),
               html.Div([
                    html.Div('{} Population'.format(selected_year[0]), style={'text-align':'center'}),
                    html.Div('{:,.0f}'.format(current_pop.iloc[-1][-1]), style={'text-align':'center'}),
                    html.Div('{} Population'.format(selected_year[1]), style={'text-align':'center'}),
                    html.Div('{:,.0f}'.format(selected_year_pop.iloc[-1][-1]), style={'text-align':'center'}),
                    html.Div('Projected Change', style={'text-align':'center'}),
                    html.Div('{0:.0%}'.format(pop_change), style={'text-align':'center'}),
               ],
                    className='round1'
               ),
          ],
               className='round1'
          ),

@app.callback(
     Output('revenue-map', 'figure'),
     [Input('year2', 'value'),
     # Input('month', 'value'),
     Input('tot-per-select', 'value')])         
def update_rev_map(selected_year,tot_per):
     # print(tot_per)
     # print(selected_year)
#     year='2018'
     # print(selected_month)
     year1 = selected_year
     # print(year1)
   
     # print(df_pc.columns)

     if tot_per == 'tot-rev':
          df_year = df_revenue.loc[df_revenue['year'] == selected_year]
          df_smr = pd.DataFrame({'county': df_year['county'], 'year': df_year.year, 'total revenue': df_year.tot_sales,'CENT_LAT':df_year.CENT_LAT,
                         'CENT_LON':df_year.CENT_LONG, 'marker_size':(df_year.tot_sales)*(.35**14)})

          df_smr_filtered = df_smr.loc[df_year['color'] == 'red']
     elif tot_per == 'per-cap':
          df_year = df_pc.loc[df_pc['year'] == selected_year]
          df_smr = pd.DataFrame({'county': df_year['county'], 'year': df_year.year, 'revenue per cap.': df_year.pc_rev,'CENT_LAT':df_year.CENT_LAT,
                         'CENT_LON':df_year.CENT_LONG, 'marker_size':(df_year.pc_rev)*(.5**4)})

          df_smr_filtered = df_smr.loc[df_year['color'] == 'red']

     elif tot_per == 'ann-rev-chng':
          df_year = df_revenue.loc[df_revenue['year'] == selected_year]
          # print(df_revenue)

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

          

if __name__ == '__main__':
    app.run_server(port=8080, debug=True)

