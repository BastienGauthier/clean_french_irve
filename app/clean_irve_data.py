import pandas as pd
from utils import URL_STABLE_DATAGOUV, type_df_irve

df_irve = pd.read_csv(URL_STABLE_DATAGOUV)
df_irve = type_df_irve(df_irve)

# Clean power in W instead of kW (>2MW should not exist)
df_irve_clean = df_irve.copy()
df_irve_clean.puissance_nominale = df_irve.puissance_nominale.apply(
    lambda x: x if x < 2000 else x / 1000
)

# Remove doubles, depending on their last modifications
# rows are ordered by id_pdc_itinerance and last_modified in an increasing order
df_irve_clean = df_irve_clean.sort_values(["id_pdc_itinerance", "last_modified"])

# id_pdc_itinerance is supposed to be a unique ID
df_irve_clean = df_irve_clean.drop_duplicates("id_pdc_itinerance", keep="last")

# Write new file
df_irve_clean.to_parquet("data/df_irve_etalab_cleaned.parquet")

# Read data to detect if no regression occured
df_irve_clean_robust = pd.read_parquet(
    "data/df_irve_etalab_cleaned_robust.parquet"
)

n_pdc = df_irve_clean.shape[0]
n_pdc_robust = df_irve_clean_robust.shape[0]

if n_pdc >= n_pdc_robust:
    df_irve_clean.to_parquet("data/df_irve_etalab_cleaned_robust.parquet")
