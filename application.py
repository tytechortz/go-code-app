import dash
import pandas as pd
import numpy as np
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
from homepage import Homepage
from revenue import revenue_App, df_pop, rpd, counties, df_revenue, sources 
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

# @app.callback(
#     Output('year-selector', 'children'),
#     [Input('year', 'value')])
# def display_month_selector(year):
     
#      return html.P('Select Year', style={'text-align': 'center'}), html.Div([
#           dcc.RangeSliderr(id='year'),
#      ],
#           className='pretty_container'
#      ),

# @app.callback(
#     Output('year-selector2', 'children'),
#     [Input('year2', 'value')])
# def display_month_selector(year):
     
#      return html.P('Select Year', style={'text-align': 'center'}), html.Div([
#           dcc.Sliderr(id='year2'),
#      ],
#           className='pretty_container'
#      ),

# @app.callback(
#     Output('month-selector', 'children'),
#     [Input('y', 'value')])
# def display_month_selector(year):
     
#      return html.P('Select Year', style={'text-align': 'center'}), html.Div([
#           dcc.Sliderr(id='year2'),
#      ],
#           className='pretty_container'
#      ),


@app.callback(
     Output('county-pop-graph', 'figure'),
     [Input('revenue-map', 'clickData'),
     Input('year', 'value')])
def display_cnty_pop(clickData, selected_year):
     # print(clickData)
     county = clickData['points'][-1]['text']
     # print(county)
     df_county_pop = df_pop[df_pop['county'] == county]
     # print(df_county_pop)
     
     fig = px.bar(df_county_pop, x='year', y='totalpopulation')

     return fig

@app.callback(
     Output('pop-stats', 'children'),
     [Input('revenue-map', 'clickData'),
     Input('year', 'value')])
def county_pop_stats(clickData, selected_year):
     print(selected_year)
     print(df_pop)
     print(selected_year[0])
     current_year = df_pop['year'] == selected_year[0]
     # print(current_year)
     projected_year = df_pop['year'] == selected_year[1]
     county = clickData['points'][-1]['text']
     print(county)
     selected_county = df_pop['county'] == county
     print(selected_county)
     current_pop = df_pop[current_year & selected_county]
     selected_year_pop = df_pop[projected_year & selected_county]
     print(selected_year_pop)
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
     Input('month', 'value')])         
def update_rev_map(selected_year, selected_month):
     # print(selected_year)
#     year='2018'
     # print(selected_month)
     year1 = selected_year
     # print(year1)
     # year2 = year1[-2:]
     # print(year2)
     rpd_s = rpd.sort_values(by=['RId2'])
     # print(rpd_s)
     rpd_s = rpd_s.apply(pd.to_numeric, errors='ignore')
     rpd_s = rpd_s.fillna(0)
     # print(rpd_s.columns)

     counties_s = counties.sort_values(by=['US_FIPS'])
     #     print(counties_s.columns)
     # print(df_revenue.head())
     # print(df)
     # selected_med_rev = rpd_s.loc[ : ,'Rper_cap_med_'+year2+'']
     # selected_rec_rev = rpd_s.loc[ : ,'Rper_cap_rec_'+year2+'']
     # print(selected_med_rev)
     # df1 = df
     # df1['Date'] = pd.to_datetime(df[['year', 'month']].assign(Day=1))
     # df1.set_index('Date', inplace=True)

     # at = df1.groupby('county')['tot_sales'].resample('Y').sum()
     
     # df1 = df1.agg({'tot_sales': 'sum'})
     # df1 = df.DataFrame
     # print(at)
     # print(df1.columns)
     # print(type(df1.loc['Date']))
     df_year = df_revenue.loc[df_revenue['year'] == str(selected_year)] 
     # df.sort_values('id', inplace=True)
     # print(selected_rev)
     # selected_rec_rev = rpd_s.loc[ : ,'Rper_cap_rec_'+year2+'']
     # print(df_year)
     # print(df_year)

     df_smr = pd.DataFrame({'county': df_year['county'], 'year': df_year.year, 'total': df_year.tot_sales,'CENT_LAT':df_year.CENT_LAT,
                    'CENT_LON':df_year.CENT_LONG, 'marker_size':(df_year.tot_sales)*(.2**9.5)})
     
     # df_smr = pd.DataFrame({'name': selected_rev.index, 'med_rev': selected_med_rev.values, 'rec_rev': 
     #           selected_rec_rev.values, 'tot_rev': selected_med_rev.values + selected_rec_rev.values,'CENT_LAT':counties_s['CENT_LAT'],
     #                'CENT_LON':counties_s['CENT_LONG'], 'marker_size':(selected_med_rev.values + selected_rec_rev.values)*(.3**3)})
     #     print(df_smr.columns)
     # df_year = df.loc[df['year'] == int(year1)]
     # print(df_year)
     # df_smr = df_smr.loc(df_smr['year'] == selected_year)
     # print(df_smr)
 
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

          

if __name__ == '__main__':
    app.run_server(port=8080, debug=True)

