import matplotlib.pyplot as plt
import datetime as dt
from datetime import datetime
import pandas as pd
import numpy as np

start_datetime_dataset = dt.datetime(2011, 1, 1, 0, 0, 0)
print('Start-time of data: ' + start_datetime_dataset.strftime('%y/%m/%d %H:%M:%S'))
end_datetime_dataset = dt.datetime(2023, 2, 13, 0, 0, 0)
print('End-time of data: ' + end_datetime_dataset.strftime('%y/%m/%d %H:%M:%S'))
start_datetime = datetime.strptime(input('Start-time of plot (%y/%m/%d %H:%M:%S): '), '%y/%m/%d %H:%M:%S')
end_datetime = datetime.strptime(input('End-time of plot (%y/%m/%d %H:%M:%S): '), '%y/%m/%d %H:%M:%S')
num_datapoints = end_datetime-start_datetime
first_row_dt = start_datetime-start_datetime_dataset
last_row_dt = end_datetime-start_datetime_dataset
first_row = int(first_row_dt/pd.Timedelta(hours=24))
last_row = int(last_row_dt/pd.Timedelta(hours=24))
list_rows = []

for i in range(first_row, last_row+1):
    list_rows.append(i)

def get_datetime_range(start_datetime, end_datetime, step=dt.timedelta(days=1)):
    current_datetime = start_datetime
    while current_datetime < end_datetime:
        yield current_datetime
        current_datetime += step

list_datetime = list(get_datetime_range(start_datetime, end_datetime))

def read_csv_files(list_datasets_names):
    data = []
    for i, name in enumerate(list_datasets_names):
        df_data = pd.read_csv(name, skiprows=lambda x: x not in list_rows, sep=';')
        data.append(df_data)
        list_datasets = np.squeeze(data)
    return list_datasets

list_datasets_names = ['Data_gasspeicherfuellstaende_AU.csv', 'Data_gasspeicherfuellstaende_EU.csv', 'Data_gasspeicherfuellstaende_FR.csv', 'Data_gasspeicherfuellstaende_GER.csv', 'Data_gasspeicherfuellstaende_IT.csv']
list_datasets = read_csv_files(list_datasets_names)
list_labels = ['AU', 'EU', 'FR', 'GER', 'IT']
comparison_data_index = 1
colors = ['g', 'b', 'm', 'c', 'y', 'k']

fig, ax = plt.subplots(1, 1, figsize=(16, 9), dpi=80)
for i in range(0, len(list_datasets_names)):
    if i == comparison_data_index:
        ax.plot(list_datetime, list_datasets[i], color='r')
    else:
        ax.plot(list_datetime, list_datasets[i], linestyle='solid', color=colors[i], alpha=0.2)

ax.set_title('Prozentuale Gasspeicherfüllstände', fontsize=18)
ax.legend(list_labels)
leg = ax.get_legend()

for i in range(0, len(list_datasets_names)):
    if i == comparison_data_index:
        leg.legend_handles[i].set_color('r')
        leg.legend_handles[i].set_alpha(1)
    else:
        leg.legend_handles[i].set_color(colors[i])

plt.xlabel('Datum')
plt.ylabel('Prozentualer Füllstand der Gasspeicher')
plt.gca().spines["top"].set_alpha(0)
plt.gca().spines["bottom"].set_alpha(.3)
plt.gca().spines["right"].set_alpha(0)
plt.gca().spines["left"].set_alpha(.3)

plt.show()
