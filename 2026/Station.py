import numpy as np
import datetime as dt
import pandas as pd


"""
Code complet des TP station meteo ( base pour l'OOP)
"""


def read_station_data(id_number):
    file_path = "./Station_fake.csv"
    df = pd.read_csv(file_path, parse_dates=[4])
    # Verification que l'id existe
    if id_number not in df["number_sta"].unique():
        print(f"La station demandée {id_number} n'existe pas.")
        print(f"Les possibilitées sont {df["number_sta"].unique()}")
        raise ValueError("Station {id_number} does not exist!")
    # Lecture et filtrage
    return df[df["number_sta"] == id_number]


def print_station_info(df: pd.DataFrame, id_number: int):
    data = read_station_data(df, id_number)
    print(f" Information pour la station {id_number}")
    print(f" Latitude de la station : {data["lat"].unique()}")
    print(f" Longitude de la station : {data["lon"].unique()}")
    print(f" Hauteur de la station : {data["height_sta"].unique()}")


def select_period(df, start_period, end_period, hour=None):

    # On reprend l'exemple de la slide précédente
    cdt = (df.date > start_period) * (df.date < end_period)
    # Mise a jour de la condition pour rajouter la selection de l'heure
    if hour is not None:  # Attention `if hour:` ne fonctionne pas avec 0.
        cdt = cdt * (df.date.dt.hour == hour)
    df_period = df[cdt]

    return df_period


df_station = read_station_data(id_number=73010)
start_period = dt.datetime(2025, 10, 20)
end_period = dt.datetime(2025, 10, 22)
df_period = select_period(df_station, start_period, end_period)
max_temperature = df_period["t"].max()

# Liste des elements ayant atteint cette température maximum.
elt = df_period[df_period["t"] == max_temperature]

print(f"La température maximale sur la période a été de {max_temperature}.")
print(
    f"Elle a été atteinte pour les dates suivantes : {elt["date"].dt.strftime("%Y%m%d-%H").values}"
)
# On va maintenant trouver la moyenne horaire maximale
# Dictionnaire qui va contenir le maximum pour chaque heure
mean_hour = {"hour": [], "value": []}
# On calcul la moyenne pour chaque heure
for i in range(0, 2):
    df_period = select_period(df_station, start_period, end_period, hour=None)
    print(len(df_period))
    mean_hour["hour"].append(i)
    mean_hour["value"].append(df_period["t"].mean())
# On recherche le maximum
mean_max = np.max(mean_hour["value"])
# On regarde quand ce maximum a été atteint
index_max = mean_hour["value"].index(mean_max)
# On regarde ensuite l'heure de ce maximum
print(
    f"L'heure pour laquelle ce maximum a été atteint est {mean_hour['hour'][index_max]} H"
)


def extrema(df: pd.DataFrame, variable: str):
    """
    Regarde pour une variable donnée la première heure pour
    laquelle le maximum/minimum a été atteint.
    """
    maxi = df[variable].max()
    mini = df[variable].min()
    # Filtre pour ne garder que les elements correspondants au maximum
    max_date = df[df[variable] == maxi]
    # au minimum
    min_date = df[df[variable] == mini]
    heure_max = max_date["date"].dt.strftime("%H").values[0]
    heure_min = min_date["date"].dt.strftime("%H").values[0]
    return (heure_max, heure_min)


def aggregation(df: pd.DataFrame, variable: str, methode: str):
    # Création d'une liste pour mettre la donnée aggrégée
    result = []
    for hour in range(0, 24):
        cdt = df.date.dt.hour == hour
        df_selected = df[cdt]
        if methode == "mean":
            result.append(df_selected[variable].mean())
        elif methode == "min":
            result.append(df_selected[variable].min())
        elif methode == "max":
            result.append(df_selected[variable].max())
        else:
            raise ValueError("Aggregation method not known")
    return result


def aggregated_bis(df, variable, methode):
    result = []
    for hour in range(0, 24):
        cdt = df.date.dt.hour == hour
        df_selected = df[cdt]
        if methode in ["mean", "max", "min"]:
            # On utilise getattr afin de requeter l'attribut correspondant à notre
            # méthode et on l'applique
            result.append(df_selected[variable].__getattr__(methode)())
        else:
            raise ValueError("Aggregation method not known")


# Soit on creer un objet station qui lit le fichier, soit on a un object station 'abstrait' qui
# faire l object station complet d'abord puis montrer REseaumeteo voir de l'heritage ?
class Station:
    def __init__(self, num_station):
        self.number = num_station


class ReseauMeteo:
    def __init__(self, file_path):
        self.file_path = file_path
        self.stations = dict()


reseau = ReseauMeteo()
reseau.charger_donnees("stations_meteo.csv")
reseau.afficher_resume()

# Exemple d'analyse
for num, sta in reseau.stations.items():
    print(f"Température moyenne à la station {num}: {sta.temperature_moyenne():.1f}°C")
