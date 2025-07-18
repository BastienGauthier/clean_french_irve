# %%
# Importation
import pandas as pd
import numpy as np
import datetime as dt


# %%
# Combined function
def filter_wrong_id(df):
    """Seul les id_pdc_itinerance "Non concerné" sont filtrés"""
    mask = ~df.id_pdc_itinerance.isin(["Non concerné"])
    return df[mask]


def get_int(x):
    try:
        return int(x)
    except ValueError:
        return np.nan


def get_dict_corresp():
    corresp_file = "data/corresp_code_postal_insee.csv"
    df_corresp = pd.read_csv(corresp_file, encoding_errors="ignore", sep=";")
    dict_corresp = df_corresp.set_index("Code_postal")[
        ["#Code_commune_INSEE"]
    ].to_dict()["#Code_commune_INSEE"]
    return dict_corresp


def clean_code_insee(df_irve):
    dict_corresp = get_dict_corresp()

    code_postaux = (
        df_irve[df_irve.code_insee_commune.isna()]["adresse_station"]
        .str.extract(r".*(\d{5}).*")
        .squeeze()
        .values
    )
    code_postaux = [get_int(c) for c in code_postaux]
    code_insee = [dict_corresp.get(c, np.nan) for c in code_postaux]

    df_irve.loc[df_irve.code_insee_commune.isna(), "code_insee_commune"] = code_insee

    return df_irve


def add_daily_file_to_combined(df_combined, df_new):
    # Update existing values
    df_combined_updated = df_combined.copy()
    col_order = df_combined.columns

    mask_updated = df_new.id_pdc_itinerance.isin(df_combined.id_pdc_itinerance)
    df_update = df_new[mask_updated].set_index("id_pdc_itinerance")

    df_combined_updated = df_combined_updated.set_index("id_pdc_itinerance")

    df_combined_updated.loc[df_update.index, :] = df_update
    df_combined_updated = df_combined_updated.reset_index()
    df_combined_updated = df_combined_updated[col_order]  # restore initial order

    # add new values
    mask_new = ~df_new.id_pdc_itinerance.isin(df_combined.id_pdc_itinerance)
    df_combined_updated = pd.concat(
        [df_combined_updated, df_new[mask_new]], axis=0, ignore_index=True
    )

    return df_combined_updated


def update_date_origine(df_combined, df_new, df_origine):
    """
    Deux opération sont réalisées
    - date_origine -> Ajout pour ceux vu la première fois
    - date_derniere_vue, n_vues -> maj pour ceux présents
    """
    df_new_origin = df_origine.copy()

    # Ajout des id_pdc_iterance vu pour la première fois
    mask_first_time = ~df_new.id_pdc_itinerance.isin(df_combined.id_pdc_itinerance)

    new_origin = pd.DataFrame(index=df_new[mask_first_time].id_pdc_itinerance)
    new_origin["date_origine"] = dt.date.today()
    new_origin["date_derniere_vue"] = dt.date.today()
    new_origin["n_vues"] = 1

    df_new_origin = pd.concat([new_origin, df_new_origin], axis=0)

    # MAJ des id_pdc_itinerance revu
    index_updated = df_new[~mask_first_time].id_pdc_itinerance.values
    df_new_origin.loc[index_updated, "date_derniere_vue"] = dt.date.today()
    df_new_origin.loc[index_updated, "n_vues"] += 1

    return df_new_origin


# %%
# Main
if __name__ == "__main__":
    df_irve_clean = pd.read_parquet("data/df_irve_etalab_cleaned.parquet")

    df_irve_clean_combined = pd.read_parquet(
        "data/df_irve_etalab_cleaned_combined.parquet"
    )

    df_origine = pd.read_parquet("data/irve_combined_data_follow_up.parquet")

    df_combined = filter_wrong_id(
        df_irve_clean_combined
    )  # safety, should not be useful
    df_new = filter_wrong_id(df_irve_clean)
    df_new = clean_code_insee(df_new)

    df_combined_updated = add_daily_file_to_combined(df_combined, df_new)
    df_combined_updated.to_parquet("data/df_irve_etalab_cleaned_combined.parquet")

    df_new_origin = update_date_origine(df_combined, df_new, df_origine)
    df_new_origin.to_csv("data/irve_combined_data_follow_up.csv")
