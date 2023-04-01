import uuid
import plotly.graph_objs as go
from data_formatting import Data

device_id = str(uuid.getnode())
if device_id == "101707883750031":  # Julian
    local_path = 'C://Users//taseehol//PycharmProjects//uri_verkehr//data//DatenSisag//Verkehrsdaten//Rohdaten Auswertungfiles xls//2022'
else:  # somebody else
    local_path = 'C://Users//enriq//Desktop//uri_verkehr//data//DatenSisag//Verkehrsdaten//Rohdaten Auswertungfiles xls//2022'

csvs = ['5401_2022.xlsx', '6002_2022.xlsx', '6004_2022.xlsx', '6009_2022.xlsx', '6011_2022.xlsx',
            '6013_2022.xlsx', '6015_2022.xlsx', '6016_2022.xlsx', '6019_2022.xlsx', '6020_2022.xlsx', '6023_2022.xlsx',
            '6024_2022.xlsx', '6025_2022.xlsx', '6026_2022.xlsx', '6202_2022.xlsx', '6203_2022.xlsx', '6701_2022.xlsx',
            '6703_2022.xlsx', '6704_2022.xlsx', '6705_2022.xlsx', '6706_2022.xlsx', '6707_2022.xlsx', '6708_2022.xlsx',
            '7201_2022.xlsx', '7202_2022.xlsx', '7208_2022.xlsx', '7403_2022.xlsx', '7408_2022.xlsx', '7701_2022.xlsx',
            '8401_2022.xlsx', '8404_2022.xlsx', '8702_2022.xlsx', '9005_2022.xlsx']

plot_data = Data(csvs, local_path)
fig = go.Figure()

for i, csv in enumerate(csvs):
    fig.add_trace(go.Scatter(x=plot_data.dataframes[i]['Datumszeit'],
                             y=plot_data.dataframes[i]['Querschnitt'],
                             name=csv,
                             mode='lines',
                             line=dict(width=1),
                             marker=dict(size=3)))

fig.show()

