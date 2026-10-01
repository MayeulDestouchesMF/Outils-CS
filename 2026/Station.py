import datetime as dt

import numpy as np
import pandas as pd

"""
Code complet des TP station météo ( base pour l'OOP)
"""


def read_station_data(id_number: int) -> pd.DataFrame:
    file_path = "./Station_fake.csv"
    df = pd.read_csv(file_path, parse_dates=[4])
    # Check that the id does exist.
    if id_number not in df["number_sta"].unique():
        print(f"La station demandée {id_number} n'existe pas.")
        print(f"Les possibilitées sont {df['number_sta'].unique()}")
        raise ValueError(f"Station {id_number} does not exist!")
    # Reading and filtering
    return df[df["number_sta"] == id_number]


def print_station_info(df: pd.DataFrame, id_number: int) -> None:
    data = read_station_data(df, id_number)
    print(f" Information pour la station {id_number}")
    print(f" Latitude de la station : {data['lat'].unique()}")
    print(f" Longitude de la station : {data['lon'].unique()}")
    print(f" Hauteur de la station : {data['height_sta'].unique()}")


def select_period(
    df: pd.DataFrame,
    start_period: dt.datetime,
    end_period: dt.datetime,
    hour: int | None = None,
) -> pd.DataFrame:
    cdt = (df.date > start_period) * (df.date < end_period)
    # Update condition to add hour selection
    if hour is not None:  # Caution! `if hour:` would not work (when hour==0)
        cdt = cdt * (df.date.dt.hour == hour)
    df_period = df[cdt]

    return df_period


df_station = read_station_data(id_number=73010)
start_period = dt.datetime(2025, 10, 20)
end_period = dt.datetime(2025, 10, 22)
df_period = select_period(df_station, start_period, end_period)
max_temperature = df_period["t"].max()

# List of elements that have reached this maximum temperature.
elt = df_period[df_period["t"] == max_temperature]

print(f"La température maximale sur la période a été de {max_temperature}.")
print(
    f"Elle a été atteinte pour les dates suivantes : {elt['date'].dt.strftime('%Y%m%d-%H').values}"
)
# We now find the time of the maximum average temperature
# Dictionary to contain average for each hour
mean_hour: dict[str, list[float]] = {"hour": [], "value": []}
# Compute average for each hour
for i in range(0, 2):
    df_period = select_period(df_station, start_period, end_period, hour=None)
    print(len(df_period))
    mean_hour["hour"].append(i)
    mean_hour["value"].append(df_period["t"].mean())
# Find the maximum of the average cycle
mean_max = np.max(mean_hour["value"])
# Look up when this maximum has been reached
index_max = mean_hour["value"].index(mean_max)
# Find associated hour
print(
    f"L'heure pour laquelle ce maximum a été atteint est {mean_hour['hour'][index_max]} H"
)


def extrema(df: pd.DataFrame, variable: str):
    """
    For a given variable, returns the first hour at which the maximum and minimum
    have been reached.
    """
    maxi = df[variable].max()
    mini = df[variable].min()
    # Filtre pour ne garder que les elements correspondants au maximum
    max_date = df[df[variable] == maxi]
    # au minimum
    min_date = df[df[variable] == mini]
    max_hour = max_date["date"].dt.strftime("%H").values[0]
    min_hour = min_date["date"].dt.strftime("%H").values[0]
    print(type(max_hour))
    return (max_hour, min_hour)


def aggregation(df: pd.DataFrame, variable: str, method: str):
    result = []
    for hour in range(0, 24):
        cdt = df.date.dt.hour == hour
        df_selected = df[cdt]
        if method == "mean":
            result.append(df_selected[variable].mean())
        elif method == "min":
            result.append(df_selected[variable].min())
        elif method == "max":
            result.append(df_selected[variable].max())
        else:
            raise ValueError("Aggregation method not known")
    print(type(result))
    return result


def aggregated_bis(df: pd.DataFrame, variable: str, method: str):
    result = []
    for hour in range(0, 24):
        cdt = df.date.dt.hour == hour
        df_selected = df[cdt]
        if method in ["mean", "max", "min"]:
            # On utilise getattr afin de requeter l'attribut correspondant à notre
            # méthode et on l'applique
            result.append(df_selected[variable].__getattr__(method)())
        else:
            raise ValueError("Aggregation method not known")
    return result


# Soit on creer un objet station qui lit le fichier, soit on a un object station 'abstrait' qui
# faire l object station complet d'abord puis montrer REseaumeteo voir de l'heritage ?
class Station:
    def __init__(self, num_station):
        self.number = num_station


class ObservationNetwork:
    def __init__(self, file_path: str):
        self.file_path: str = file_path
        self.stations: Dict = dict()


network = ObservationNetwork()
network.load_data("stations_meteo.csv")
network.print_summary()

# Exemple d'analyse
for num, sta in network.stations.items():
    print(f"Température moyenne à la station {num}: {sta.temperature_moyenne():.1f}°C")
