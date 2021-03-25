import plotly.express as px
import pandas as pd
from revenue import counties 






fig = px.choropleth(df, geojson=counties)
