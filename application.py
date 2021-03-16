import dash
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
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

print(counties)
selected_cnty = 'Denver'


print(df.tail())
df = df[df['county']==selected_cnty]

fig = px.bar(df, x='year', y='totalPopulation')





app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
  dcc.Graph(
    id='pop-graph',
    figure=fig
  ),
  dcc.Dropdown(
    id='county',
    options=[{'label':i, 'value':i} for i in counties],
  ),
])

if __name__ == '__main__':
    app.run_server(port=8080, debug=True)

