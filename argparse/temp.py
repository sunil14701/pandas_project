import pandas as pd

datset1 = "ecommerce2010"
datset2 = "ecommerce2011"

df_2010 = pd.read_csv(f"../datasets/{datset1}.csv")
df_2011 = pd.read_csv(f"../datasets/{datset2}.csv")


county_2010 = df_2010.groupby("Country")["Country"].unique().head()
county_2010.sort_values()
print(county_2010)