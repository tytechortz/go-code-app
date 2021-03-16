import dash
import pandas as pd
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
               value="Denver"  
          ),
     ],
          className='pretty_container'
     ),

@app.callback(
     Output('county-pop-graph', 'figure'),
     Input('county', 'value'))
def display_cnty_pop(selected_county):
     df_county_pop = df_pop[df_pop['county'] == selected_county]
     print(df_county_pop)
     fig = px.bar(df_county_pop, x='year', y='totalPopulation')

     return fig

if __name__ == '__main__':
    app.run_server(port=8080, debug=True)

