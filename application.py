import dash
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('pop.csv')

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

counties = []

for i in df.county.unique():
  counties.append(i)

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
     dcc.Graph(
          id='county-pop-graph',
     ),
     dcc.Dropdown(
          id='county',
          options=[{'label':i, 'value':i} for i in counties],
     ),
])

@app.callback(
     Output('county-pop-graph', 'figure'),
     Input('county', 'value'))
def display_cnty_pop(selected_county):
     df_county_pop = df[df['county'] == selected_county]

     fig = px.bar(df_county_pop, x='year', y='totalPopulation')

     return fig

if __name__ == '__main__':
    app.run_server(port=8080, debug=True)

