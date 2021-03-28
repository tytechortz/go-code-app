import dash
import pandas as pd
import numpy as np
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
from homepage import Homepage
from revenue import revenue_App, df_pop, rpd, counties, df_revenue, sources, df_pc
import os
from dotenv import load_dotenv


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
     ),


@app.callback(
     Output('county-pop-graph', 'figure'),
     [Input('revenue-map', 'clickData'),
     Input('year', 'value')])
def display_cnty_pop(clickData, selected_year):
     # print(clickData)
     county = clickData['points'][-1]['text']
     # print(county)
     df_county_pop = df_pop[df_pop['county'] == county]
     print(df_county_pop)
     print(selected_year)
     df_county_pop_range = df_county_pop[(df_county_pop['year'] >= selected_year[0]) & (df_county_pop['year'] <= selected_year[1])]
     print(df_county_pop_range)
     
     fig = px.bar(df_county_pop_range, x='year', y='totalpopulation')

     return fig

@app.callback(
     Output('pop-stats', 'children'),
     [Input('revenue-map', 'clickData'),
     Input('year', 'value')])
def county_pop_stats(clickData, selected_year):
     # print(selected_year)
     # print(df_pop)
     # print(selected_year[0])
     current_year = df_pop['year'] == selected_year[0]
     # print(current_year)
     projected_year = df_pop['year'] == selected_year[1]
     county = clickData['points'][-1]['text']
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
     Input('month', 'value'),
     Input('tot-per-select', 'value')])         
def update_rev_map(selected_year, selected_month, tot_per):
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
     # print(df_smr)

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

