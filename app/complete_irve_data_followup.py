# %%
# Importation
import pandas as pd
import datetime as dt

# %%
# Reading data
df_irve_clean = pd.read_csv("data/df_irve_etalab_cleaned.csv", index_col=0)

df_irve_clean_robust = pd.read_csv(
    "data/df_irve_etalab_cleaned_robust.csv", index_col=0
)

df_irve_clean_combined = pd.read_csv(
    "data/df_irve_etalab_cleaned_combined.csv", index_col=0
)

# %%
# Filling data
n_pdc = df_irve_clean.shape[0]
n_pdc_robust = df_irve_clean_robust.shape[0]
n_pdc_combined = df_irve_clean_combined.shape[0]
today_date = str(dt.date.today())
with open("data/irve_data_follow_up.csv", "a") as f:
    f.write(f"{today_date},{n_pdc},{n_pdc_robust},{n_pdc_combined}\n")
