import pandas as pd
import os


def path(csv_names, path_local):
    paths = []
    for name in csv_names:
        path = os.path.join(path_local, name)
        paths.append(path)
    return paths

def dataframe(paths):
    dfs = []
    for path in paths:
        df = pd.read_excel(path)
        dfs.append(df)
    return dfs

def datetime(dfs):
    datetimes = []
    for df in dfs:
        df.HHMM = df.HHMM / 100
        df['HHMM'] = df['HHMM'].replace(24.0, 0.0)
        df.head(100)
        df['Datum und Zeit'] = df["Datum"].astype(str) + ' ' + df.HHMM.astype(str)
        df['Datumszeit'] = pd.to_datetime(df['Datum und Zeit'], format='%Y-%m-%d %H.%M')
        datetime = df['Datumszeit']
        datetimes.append(datetime)
    return datetimes


class Data:

    def __init__(self, csvs, localpath):
        paths = path(csvs, localpath)
        self.dataframes = dataframe(paths)
        self.datetimes = datetime(self.dataframes)
