import pandas as pd
import os

localpath = 'C://Users//taseehol//PycharmProjects//uri_verkehr//data//DatenSisag//Verkehrsdaten//Rohdaten Auswertungfiles xls//2022'
csvs = ['6004_2022.xlsx', '6009_2022.xlsx']

def path(csvs, localpath):
    paths = []
    for csv in csvs:
        path = os.path.join(localpath, csv)
        paths.append(path)
    return paths


def get_csv(paths):
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

paths = path(csvs, localpath)
dfs = get_csv(paths)
datetime_dfs = datetime(dfs)

print(datetime_dfs[0])
