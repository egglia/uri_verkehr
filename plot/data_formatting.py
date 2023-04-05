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
        df.HHMM = df.HHMM / 100
        df['HHMM'] = df['HHMM'].replace(24.0, 23.59)
        df.head(100)
        df['Datum und Zeit'] = df["Datum"].astype(str) + ' ' + df.HHMM.astype(str)
        df['Datumszeit'] = pd.to_datetime(df['Datum und Zeit'], format='%Y-%m-%d %H.%M')
        df['Datumszeit'].notna()
        dataframe = df[df['Querschnitt'].notna()]
        data_daily = dataframe.groupby(dataframe['Datumszeit'].dt.date)['Querschnitt'].sum()
        dataframe_daily = data_daily.to_frame(name='Querschnitt').reset_index()
        dfs.append(dataframe_daily)
    return dfs


class Data:

    def __init__(self, csvs, local_path):
        paths = path(csvs, local_path)
        self.dataframes = dataframe(paths)
