from pathlib import Path
import pandas as pd

URL_STABLE_DATAGOUV = (
    "https://www.data.gouv.fr/fr/datasets/r/eb76d20a-8501-400e-b336-d85724de5435"
)

APP_FOLDER = str(Path(__file__).parent.parent)

def type_df_irve(df_irve : pd.DataFrame):
    df_irve.code_insee_commune = df_irve.code_insee_commune.astype(str)
    df_irve.tarification = df_irve.tarification.astype(str)
    df_irve.prise_type_ef= df_irve.prise_type_ef.astype(bool)
    df_irve.prise_type_2 = df_irve.prise_type_2.astype(bool) 
    df_irve.prise_type_combo_ccs = df_irve.prise_type_combo_ccs.astype(bool) 
    df_irve.prise_type_chademo = df_irve.prise_type_chademo.astype(bool)
    df_irve.prise_type_autre = df_irve.prise_type_autre.astype(bool)
    df_irve.gratuit = df_irve.gratuit.astype(bool)
    df_irve.paiement_acte = df_irve.paiement_acte.astype(bool)
    df_irve.paiement_cb = df_irve.paiement_cb.astype(bool) 
    df_irve.paiement_autre = df_irve.paiement_autre.astype(bool)
    df_irve.reservation = df_irve.reservation.astype(bool)
    df_irve.station_deux_roues = df_irve.station_deux_roues.astype(bool)
    df_irve.cable_t2_attache = df_irve.cable_t2_attache.astype(bool)
    return df_irve