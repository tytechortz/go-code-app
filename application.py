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
          dcc.Dropdown(
               id='county',
               options=[{'label':i, 'value':i} for i in counties], 
               value='Denver' 
          ),
     ],
          className='pretty_container'
     ),

@app.callback(
     Output('county-pop-graph', 'figure'),
     Input('county', 'value'))
def display_cnty_pop(selected_county):
     df_county_pop = df_pop[df_pop['county'] == selected_county]
     # print(df_county_pop)
     fig = px.bar(df_county_pop, x='year', y='totalpopulation')

     return fig

@app.callback(
     Output('pop-stats', 'children'),
     Input('county', 'value'))
def county_pop_stats(county):
     current_year = df_pop['year'] == '2021'
     projected_year = df_pop['year'] == '2050'
     selected_county = df_pop['county'] == county
     current_pop = df_pop[current_year & selected_county]
     pop_2050 = df_pop[projected_year & selected_county]
     print(pop_2050)
     if pop_2050.iloc[-1][-1] > current_pop.iloc[-1][-1]:
          pop_change = (pop_2050.iloc[-1][-1] - current_pop.iloc[-1][-1]) / current_pop.iloc[-1][-1]
     else:
          pop_change = -((current_pop.iloc[-1][-1] - pop_2050.iloc[-1][-1]) / current_pop.iloc[-1][-1])
     # print(pop_2050)
     return html.Div([
               html.Div('{} County Pop. Stats'.format(county), style={'text-align':'center'}),
               html.Div([
                    html.Div('Current Population', style={'text-align':'center'}),
                    html.Div('{:,.0f}'.format(current_pop.iloc[-1][-1]), style={'text-align':'center'}),
                    html.Div('2050 Projected Pop', style={'text-align':'center'}),
                    html.Div('{:,.0f}'.format(pop_2050.iloc[-1][-1]), style={'text-align':'center'}),
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

