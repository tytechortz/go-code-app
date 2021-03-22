import pandas as pd
from sodapy import Socrata

client = Socrata("data.colorado.gov", None)

# https://data.colorado.gov/resource/j7a3-jgd3.csv
# https://data.colorado.gov/resource/j7a3-jgd3.json

results = client.get("j7a3-jgd3", limit=2000)


df_rev_cty = pd.DataFrame.from_records(results)


df_rev_cty = df_rev_cty.drop(['id', 'med_blank_code', 'rec_blank_code'], 1)
print(df_rev_cty)

df_rev_cty[['rec_sales', 'med_sales']] = df_rev_cty[['rec_sales', 'med_sales']].astype(float)
print(df_rev_cty)
df_rev_cty['total_sales'] = df_rev_cty['rec_sales'] + df_rev_cty['med_sales']
print(df_rev_cty)