import pandas as pd
from sodapy import Socrata
import numpy as np

client = Socrata("data.colorado.gov", None)

# https://data.colorado.gov/resource/j7a3-jgd3.csv
# https://data.colorado.gov/resource/j7a3-jgd3.json

results = client.get("j7a3-jgd3", limit=6000)


df_rev_cty = pd.DataFrame.from_records(results)
pop_results = client.get("q5vp-adf3", limit=381504)


df_rev_cty = df_rev_cty.drop(['id', 'med_blank_code', 'rec_blank_code'], 1)
# print(df_rev_cty)

df_rev_cty[['rec_sales', 'med_sales']] = df_rev_cty[['rec_sales', 'med_sales']].astype(float)
df_rev_cty = df_rev_cty.fillna(0)
# print(df_rev_cty)
df_rev_cty['total_sales'] = df_rev_cty['rec_sales'] + df_rev_cty['med_sales']
# print(df_rev_cty)
df_rev_cty['month'] = df_rev_cty['month'].astype(int)
df_rev_cty = df_rev_cty.sort_values(['county', 'year', 'month'], ascending=(True, True, True)).reset_index()



# df_rev_cty = df_rev_cty.groupby('year').reset_index
# df_rev_cty = df_rev_cty.set_index(['year', 'month'])
# df_rev_cty = df_rev_cty.groupby(['county', 'year', 'month']).total_sales.sum().sort_index(level=['county', 'year', 'month'])

# df_rev_cty = df_rev_cty.groupby('county')
# print(df_rev_cty.head(15))

df_pop = pd.DataFrame.from_records(pop_results)
df_pop['totalpopulation'] = df_pop['totalpopulation'].astype(int)
df_pop = df_pop.drop(['age', 'malepopulation', 'femalepopulation'], axis=1)
df_pop = df_pop.groupby(['year', 'county'], as_index=False)['totalpopulation'].sum()

# print(df_pop.tail(15))

new_df = pd.merge(df_rev_cty, df_pop, how='left', left_on=['county', 'year'], right_on=['county', 'year'])

new_df['rev_per_cap'] = np.where(new_df['total_sales'] == 0, 0, new_df['total_sales'] / new_df['totalpopulation'])

new_df['med_rev_pc'] = np.where(new_df['med_sales'] == 0, 0, new_df['med_sales'] / new_df['totalpopulation'])

new_df['rec_rev_pc'] = np.where(new_df['rec_sales'] == 0, 0, new_df['rec_sales'] / new_df['totalpopulation'])

print(new_df.columns)

cty_df = new_df[new_df['county'] == 'Adams']

print(cty_df)
