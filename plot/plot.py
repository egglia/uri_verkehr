import matplotlib.pyplot as plt
from data_formatting import Data
import uuid

device_id = str(uuid.getnode())
if device_id == "101707883750031":  # Julian
    local_path = 'C://Users//taseehol//PycharmProjects//uri_verkehr//data//DatenSisag//Verkehrsdaten//Rohdaten Auswertungfiles xls//2022'
else:
    ''

csvs = ['6004_2022.xlsx']

fig, ax = plt.subplots()

plot_data = Data(csvs, local_path)
ax.plot(plot_data.datetimes[0], plot_data.dataframes[0]['Querschnitt'], label='6004_2022')
