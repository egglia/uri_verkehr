import math
import time
import numpy as np
import json
import glob
import warnings
import requests

import matplotlib.pyplot as plt
import seaborn as sns

import pandas as pd
import geopandas as gpd
pd.set_option('display.max_columns', None)


import datetime

df = pd.read_pickle('C://Users//enriq//Desktop//uri_verkehr//plot//dfipynb.pickle')
dftmp=df

def anpassung_zeit(df):
    df = df[df['Querschnitt'].notna()]
    df = df[df['Datum'].notna()]
    df.HHMM = df.HHMM / 100
    df['HHMM']=df['HHMM'].replace(24.0,23.59)
    df.head(100)
    df['Datum und Zeit'] = df["Datum"].astype(str).str[:10]+ ' ' +df.HHMM.astype(str)
    df['Datumszeit'] = pd.to_datetime(df['Datum und Zeit'], format='%Y-%m-%d %H.%M', errors= "coerce")
    return df
df=anpassung_zeit(df)

tmp = df
index = pd.DatetimeIndex(tmp['Datumszeit'])
tmp = tmp.iloc[index.indexer_between_time('06:30', '22:30')]
tmp = tmp[tmp['Datumszeit'].dt.year == 2022]
# group by measurepoint and date, then apply aggregations
result = tmp.groupby(['Zst', 'Datumszeit']).agg({'Querschnitt': ['sum']}).reset_index()
result["Datum"] =  result["Datumszeit"].dt.date
result.columns = [''.join(col).strip() for col in result.columns.values]
result = result.groupby(['Zst', 'Datum']).agg({'Querschnittsum': ['sum','min','max']}).reset_index()
result.columns = ['_'.join(col).strip() for col in result.columns.values]
result['diff'] = result['Querschnittsum_max']-result['Querschnittsum_min']
result['avg/h'] = result['Querschnittsum_sum']/17

result["Zst_"]=result["Zst_"].replace([5401, 6011, 6202, 6015, 6003, 6009, 6025, 6002, 6016, 6004, 6010, 6023, 6021, 6020, 6024,
6018, 6022, 6013, 6014, 6017, 6026, 6303, 6019, 6707, 6706, 6704, 6705, 6708, 6701, 6703, 7208, 7202, 7201, 7408, 7501, 7403, 8405,
8404, 8402, 8401, 8703, 8702, 9004, 9006, 9005, 9301, 9101, 7701, 6501],
['Bahnhof_Flüelen','Allmendstrasse', 'Hess', 'Ara Altdorf', 'JB Bau', 'Spital', 'EWA Altdorf', 'Schlosserei Trögli', 'Bifang',
 'Schulhaus Hagen', 'Staatsarchiv', 'Staatsarchiv2', 'Dätwyler', 'Gisler Druck', 'St. Karl',
 'Amavita Apotheke', 'Bahnhof Altdorf Bauernhof', 'Steinmatt Merck', 'Ehem. Kebab Hüsli', 'Kant. Verwaltung', 'Kollegium',
  'Strassenverkehrsamt', 'Ruberst', 'Grund Dorfstrasse', 'Grund Gotthardstrasse', 'Gandrütti', 'Adlergarten', 'Sisag',
   'Elektro Nauer', 'Jumbo', 'Breiteli', 'Birtschen', 'Erstfeld-Silenen', 'Silenen-Amsteg', 'Galleri Breitlaui',
   'Amsteg', 'Husen', 'Werkhalle Wassen', 'Nördlich einfahrt A2 Wassen Periodisch', 'Bahnhof Wassen', 'Teufelsstein Periodisch',
   'Südlich Keisel Göschenen', 'Andermatt Dorf', 'Nätschen', "Tristelboden", 'Feldbäckerei VBS', 'Tiefenbach', "Seelisberg",'Urnerboden'])

import plotly.express as px
fig = px.histogram(result, x='Zst_', y='avg/h', height=750)

fig.update_layout(barmode='group', xaxis={'categoryorder':'total descending'})
fig.update_xaxes(type='category')

fig.show()

fig = px.histogram(result, x='Zst_', y='diff', height=600)
fig.update_layout(barmode='group', xaxis={'categoryorder':'total descending'})

fig.update_xaxes(type='category')

fig.show()

import plotly.express as px
result['rel'] = result['diff']/result['avg/h']

fig = px.histogram(result, x='Zst_', y='rel', height=700)

fig.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})
fig.update_xaxes(type='category')

fig.show()

fig = px.line(result, x="Datum_", y="Querschnittsum_sum", color='Zst_', height=700)

fig.update_layout(dict(updatemenus=[
                        dict(
                            type = "buttons",
                            direction = "left",
                            buttons=list([
                                dict(
                                    args=["visible", "legendonly"],
                                    label="Deselect All",
                                    method="restyle"
                                ),
                                dict(
                                    args=["visible", True],
                                    label="Select All",
                                    method="restyle"
                                )
                            ]),
                            pad={"r": 10, "t": 10},
                            showactive=False,
                            x=1,
                            xanchor="right",
                            y=1.1,
                            yanchor="top"
                        ),
                    ]
              ))
fig.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(count=7,
                     label="W",
                     step="day",
                     stepmode="backward"),
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
)

fig.show()

fig = px.line(result, x="Datum_", y="avg/h", color='Zst_', height=700)

fig.update_layout(dict(updatemenus=[
                        dict(
                            type = "buttons",
                            direction = "left",
                            buttons=list([
                                dict(
                                    args=["visible", "legendonly"],
                                    label="Deselect All",
                                    method="restyle"
                                ),
                                dict(
                                    args=["visible", True],
                                    label="Select All",
                                    method="restyle"
                                )
                            ]),
                            pad={"r": 10, "t": 10},
                            showactive=False,
                            x=1,
                            xanchor="right",
                            y=1.1,
                            yanchor="top"
                        ),
                    ]
              ))
fig.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(count=7,
                     label="W",
                     step="day",
                     stepmode="backward"),
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
)

fig.show()

fig = px.histogram(result, x='Zst_', y='Querschnittsum_sum', height=700)

fig.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})
fig.update_xaxes(type='category')

fig.show()