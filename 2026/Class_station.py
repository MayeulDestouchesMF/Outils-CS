import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def read_station_data(id_number):
    file_path = "/Users/sagarra/Downloads/Fichier_Meteo/station_2018.csv"
    df = pd.read_csv(file_path, parse_dates=[4])
    # Verification que l'id existe
    if id_number not in df["number_sta"].unique():
        print(f"La station demandée {id_number} n'existe pas.")
        print(f"Les possibilitées sont {df['number_sta'].unique()}")
        raise ValueError("Station {id_number} does not exist!")
    # Lecture et filtrage
    return df[df["number_sta"] == id_number]


def print_station_info(df: pd.DataFrame, id_number: int):
    print(f" Information pour la station {id_number}")
    print(f" Latitude de la station : {df['lat'].unique()}")
    print(f" Longitude de la station : {df['lon'].unique()}")
    print(f" Hauteur de la station : {df['height_sta'].unique()}")


def select_period(df, start_period, end_period, hour=None):
    # On reprend l'exemple de la slide précédente
    cdt = (df.date > start_period) * (df.date < end_period)
    # Mise a jour de la condition pour rajouter la selection de l'heure
    if hour is not None:  # Attention `if hour:` ne fonctionne pas avec 0.
        cdt = cdt * (df.date.dt.hour == hour)
    df_period = df[cdt]
    return df_period


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


def aggregation(df: pd.DataFrame, variable: str, methode: str = "mean"):
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


def visualize(x_value, y_value, axis_labels=["X", "Y"]):
    """Plot the y vs x values on a graph with the possibility of specified axis labels"""
    plt.plot(x_value, y_value)
    plt.xlabel(axis_labels[0])
    plt.ylabel(axis_labels[1])
    plt.show()


class StationMeteo:
    def __init__(self, id_number):
        self.id = id_number
        self.df = read_station_data(self.id)
        self.df_period = self.df

    def set_period(self, start, end):
        self.df_period = select_period(self.df, start, end)

    def info(self):
        print_station_info(self.df_period, self.id)

    def extrema(self, var: str):
        return extrema(self.df_period, var)

    def aggregate(self, var, methode):
        return aggregation(self.df_period, var, methode=methode)

    def export(self, period=False):
        if not period:
            self.df.to_csv(f"station_{self.id}.csv")
        else:
            self.df_period.to_csv(f"station_{self.id}.csv")


if 0:
    station_id = 28206001
    df_station_73010 = read_station_data(station_id)
    print_station_info(df_station_73010, station_id)
    df_station_73010_oct = select_period(df_station_73010, "2018-10-1", "2018-10-15")
    h_temp_max, h_temp_min = extrema(df_station_73010_oct, "t")
    mean_temp = aggregation(df_station_73010_oct, "t", methode="mean")
    visualize(
        range(len(mean_temp)),
        mean_temp,
        axis_labels=["Heure de la journée", "Temperature Moyenne"],
    )

Station_73 = StationMeteo(28206001)
Station_73.set_period("2018-2-1", "2018-2-5")
h_max, h_min = Station_73.extrema("t")
mean_T = Station_73.aggregate("t", methode="mean")
visualize(range(24), mean_T, axis_labels=["Heure", "Température moyenne"])
# Station_73.export(period=True)


#### RESEAU
class StationMeteoAb:
    def __init__(self, id_number, df):
        self.id = id_number
        self.df = df
        self.df_period = self.df

    def set_period(self, start, end):
        self.df_period = select_period(self.df, start, end)

    def info(self):
        print_station_info(self.df_period, self.id)

    def extrema(self, var: str):
        return extrema(self.df_period, var)

    def aggregate(self, var, methode):
        return aggregation(self.df_period, var, methode=methode)

    def export(self, period=False):
        if not period:
            self.df.to_csv(f"station_{self.id}.csv")
        else:
            self.df_period.to_csv(f"station_{self.id}.csv")


class Reseau:
    def __init__(self, file_path):
        self.file_path = file_path
        self.stations = {}
        self._load_stations()

    def _load_stations(self):
        df = pd.read_csv(self.file_path, parse_dates=[4])
        for id_number in df["number_sta"].unique():
            station_df = df[df["number_sta"] == id_number]
            self.stations[id_number] = StationMeteoAb(id_number, station_df)

    def get_station(self, id_number):
        return self.stations.get(id_number)

    def info(self):
        for id in self.stations:
            print(10 * "-")
            self.stations[id].info()

    def set_period(self, start, end):
        for station in self.stations.values():
            station.set_period(start, end)


Res = Reseau("/Users/sagarra/Downloads/Fichier_Meteo/station_2018.csv")
Res.info()
Res.set_period("2018-2-1", "2018-2-5")
mean_T_A = Res.get_station(28206001).aggregate("t", methode="mean")
mean_T_B = Res.get_station(85191003).aggregate("t", methode="mean")
visualize(
    range(24),
    abs(np.array(mean_T_A) - np.array(mean_T_B)),
    axis_labels=["Temperature Station A", "Température Station B"],
)
