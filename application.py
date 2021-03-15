import dash
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html


new_df = pd.read_csv('pop.csv')
print(new_df.tail())

