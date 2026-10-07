import datetime as dt

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

"""
Correction of TP 4 - First part
"""


def read_station_data(df: pd.DataFrame, id_number: int) -> pd.DataFrame:
    """
    Returns a filtered dataframe with data from the required station only.
    """
    # Check that the id does exist.
    if id_number not in df["number_sta"].unique():
        print(f"La station demandée {id_number} n'existe pas.")
        print(f"Les possibilitées sont {df['number_sta'].unique()}")
        raise ValueError(f"Station {id_number} does not exist!")
    # Filter rows based on station number
    return df[df["number_sta"] == id_number]


def print_station_info(df: pd.DataFrame, id_number: int) -> None:
    """
    Find and print information on the location of a given station.
    """
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
    """
    Returns a filtered dataframe with dates between `start_period` and `end_period`.
    If `hour` is provided, adds an additional filtering to return only data at
    this hour of the day.
    """
    condition = (df.date >= start_period) * (df.date <= end_period)
    # Update condition to add hour selection
    if hour is not None:  # Caution! `if hour:` would not work (when hour==0)
        condition = condition * (df.date.dt.hour == hour)
    df_period = df[condition]
    return df_period


# Read CSV file into a Pandas DataFrame.
file_path = "/home/newton/horsenm/destouchesm/COURS_CS/data/station_2018.csv"
df = pd.read_csv(file_path, parse_dates=[4])

# Print number of unique station identifiers.
n_stations = df["number_sta"].unique().size
print(f"There are data from {n_stations} stations in the file.")

# Filter by station
df_station = read_station_data(df, id_number=53116003)

# Filter by period
start_period = dt.datetime(2018, 10, 1)
end_period = dt.datetime(2018, 10, 15)
df_period = select_period(df_station, start_period, end_period)

# Find maximum temperature
max_temperature = df_period["t"].max()

# List of elements that have reached this maximum temperature.
elt = df_period[df_period["t"] == max_temperature]

print(f"La température maximale sur la période a été de {max_temperature}.")
print(
    "Elle a été atteinte pour les dates suivantes :",
    elt["date"].dt.strftime("%Y%m%d-%H").values,
)

# We now find the time of the maximum average temperature
hours = []
mean_temp = []
# Compute average for each hour
for hour in range(0, 24):
    df_period = select_period(df_station, start_period, end_period, hour=hour)
    hours.append(hour)
    mean_temp.append(df_period["t"].mean())

# Find the maximum of the average cycle
mean_max = np.max(mean_temp)
# Look up when this maximum has been reached
index_max = mean_temp.index(mean_max)
# Find associated hour
print(
    f"L'heure pour laquelle le maximum de température moyenne a été atteint est {hours[index_max]}H"
)


def extrema(df: pd.DataFrame, variable: str) -> tuple[str, str]:
    """
    For a given variable, return the first hour at which the maximum and minimum
    have been reached.
    """
    maxi = df[variable].max()
    mini = df[variable].min()
    # Filter to keep only elements where maximum has been reached.
    max_date = df[df[variable] == maxi]
    # Same for minimum.
    min_date = df[df[variable] == mini]
    max_hour = max_date["date"].dt.strftime("%H").values[0]
    min_hour = min_date["date"].dt.strftime("%H").values[0]
    return (max_hour, min_hour)


def aggregate(df: pd.DataFrame, variable: str, method: str) -> list[float]:
    """
    Return mean, min or max the required variable, depending on the chosen
    aggregation method.
    """
    result = []
    for hour in range(0, 24):
        condition = df.date.dt.hour == hour
        df_selected = df[condition]
        print("hour:", hour, "size:", df_selected.size, "head:", df_selected.head())
        if method == "mean":
            result.append(df_selected[variable].mean())
        elif method == "min":
            result.append(df_selected[variable].min())
        elif method == "max":
            result.append(df_selected[variable].max())
        else:
            raise ValueError("Aggregation method not known")
    return result


def aggregate_bis(df: pd.DataFrame, variable: str, method: str) -> list[float]:
    """
    Return mean, min or max the required variable, depending on the chosen
    aggregation method.
    """
    result = []
    for hour in range(0, 24):
        cdt = df.date.dt.hour == hour
        df_selected = df[cdt]
        if method in ["mean", "max", "min"]:
            # We use `getattr` to find the attribute corresponding to our method,
            # and we apply it.
            result.append(df_selected[variable].__getattr__(method)())
        else:
            raise ValueError("Aggregation method not known")
    return result


def visualize_hourly_means(
    df: pd.DataFrame, variable: str, labels: tuple[str, str]
) -> None:
    """
    Plot hourly mean of required variable
    """
    mean_data = aggregate(df, variable, "mean")
    print(mean_data)
    hours = np.arange(24)
    plt.plot(hours, mean_data)
    plt.xlabel(labels[0])
    plt.ylabel(labels[1])
    plt.show()


# Test the plotting tool
df_period = select_period(df_station, start_period, end_period)
visualize_hourly_means(df_period, "t", labels=("hour", "mean temperature in K"))
