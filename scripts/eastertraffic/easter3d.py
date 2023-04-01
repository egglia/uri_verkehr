import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from os import path
import matplotlib.dates as mdates


from data.dataloader import extract_pickle, extract_from_pdf

pathpdf = path.dirname(path.abspath(__file__))
pathpdf: str = path.abspath(path.join(pathpdf, "..", "..",
                                      "data", "geo.uri", "7403.pdf"))
assert path.isfile(pathpdf)
werkverk = extract_from_pdf("Gotthardstrasse", np.arange(24), pathpdf)

picklef = extract_pickle()
osterdaten = [  # ['2021-03-31', '2021-04-06', 2021],
              ['2022-04-13', '2022-04-22', 2022]]
fig, ax = plt.subplots()
for (richtung, richname, color) in [[1, "Gurtnellen", "blue"],
                                    # [2, "Silenen", "orange"],
                                    ]:
    for (start, end, year) in osterdaten:
        easter = picklef.loc[(picklef['Datumszeit'] >= pd.to_datetime(start))
                             & (picklef['Datumszeit'] <= pd.to_datetime(end))
                             & (picklef["Zst"] == 7403)
                             & (picklef["Richtung"] == richtung)]
        easter.set_index("Datumszeit", inplace=True)
        print(easter["Querschnitt"].head(100))
        time = range(len(easter["Querschnitt"]))
        ax.plot(easter.index, easter["Querschnitt"].values,
                label=f"Ostern {year} nach {richname}",
                color=color)
        ax.plot(easter.index,
                np.resize(werkverk[f"richtung{richtung}"], len(time)),
                label=f"Werksverkehr nach {richname}",
                color=color, linestyle=":")
    # set the x-axis formatter to show only daily ticks
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_locator(mdates.DayLocator())
ax.legend()
ax.set_xlabel("Datum")
ax.set_ylabel("Fahrzeuge pro Stunde")
ax.set_title("ZST 7403 - Gotthardstrasse 36 in Amsteg")

plt.savefig("Gotthardstrasse Amsteg.png")
plt.show()
