import dash
import pandas as pd
import numpy as np
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
from homepage import Homepage
from revenue import revenue_App, df_pop


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
    Output('year-selector', 'children'),
    [Input('year', 'value')])
def display_month_selector(year):
     
     return html.P('Select Year', style={'text-align': 'center'}), html.Div([
          dcc.RangeSliderr(id='year'),
     ],
          className='pretty_container'
     ),


@app.callback(
     Output('county-pop-graph', 'figure'),
     [Input('county', 'value'),
     Input('year', 'value')])
def display_cnty_pop(selected_county, selected_year):
     df_county_pop = df_pop[df_pop['county'] == selected_county]
     
     fig = px.bar(df_county_pop, x='year', y='totalpopulation')

     return fig

@app.callback(
     Output('pop-stats', 'children'),
     [Input('county', 'value'),
     Input('year', 'value')])
def county_pop_stats(county, selected_year):
     print(selected_year[0])
     current_year = df_pop['year'] == str(selected_year[0])
     print(current_year)
     projected_year = df_pop['year'] == str(selected_year[1])
     selected_county = df_pop['county'] == county
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
          

if __name__ == '__main__':
    app.run_server(port=8080, debug=True)

