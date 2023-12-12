#%%
# Importation
import matplotlib.pyplot as plt
import pandas as pd

#%%
# Reading data
df_irve_follow_up = pd.read_csv(
    'data/irve_data_follow_up.csv', 
    parse_dates=[0]
    )

#%% 
# Creating graph
plt.figure(figsize=(10,7))
plt.scatter(
    df_irve_follow_up.date.values,
    df_irve_follow_up.n_pdc.values,
    label = '#PdC du fichier du jour'
    )
plt.scatter(
    df_irve_follow_up.date.values,
    df_irve_follow_up.n_pdc_robust.values,
    label = '#PdC du fichier robuste',
    marker='P'
    )
plt.scatter(
    df_irve_follow_up.date.values,
    df_irve_follow_up.n_pdc_combined.values,
    label = '#PdC du fichier combiné',
    marker='s'
    )
plt.legend()
plt.grid(True)
plt.title(
    "Evolution du nombre de points de connection dans le fichier consolidé d'Etalab"
    )
plt.xlabel('Date')
plt.ylabel('Nombre de points de connection unique')
plt.tight_layout()

plt.savefig('img/irve_data_follow_up.png')

# %%
