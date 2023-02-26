from pandas.core.indexes.datetimes import DatetimeIndex
from pandas.core.frame import DataFrame as df
from os.path import isfile
from pdfreader import SimplePDFViewer
import numpy as np
import pandas as pd
from os import path

# Constants
start_time = pd.Timestamp('2022-11-25 00:30:00')  # Random Friday
TIME_24h = pd.date_range(start=start_time, periods=24, freq='H')


def extract_from_pdf(name: str,
                     time: DatetimeIndex,
                     path_pdf: str,
                     ) -> df:
    """
    Von den pdfs von https://geo.ur.ch/ werden die 24 Werte der
     Tagesganglinien des Werktagverkehrs Mo - Fr in beide Richtungen
     extrahiert
    :param name:
    :param time:
    :param path_pdf:
    :return:
    """
    assert isfile(path_pdf)
    assert len(time) == 24

    # Open the PDF file and create the PDF viewer object
    with open(path_pdf, 'rb') as f:
        viewer = SimplePDFViewer(f)
        # Load the first page of the PDF file
        viewer.navigate(1)
        # Extract the text content of the first page
        viewer.render()
        # Get the text content of the first page
        page_text: list = viewer.canvas.strings
        assert name in "".join(page_text), f"Maybe worng pdf specified? " \
                                           f"Did not find {name} in {path_pdf}"

        text: list = list()
        strings: str = ""
        for chars in page_text:
            if not chars.isdigit():
                strings += chars
            else:
                if len(strings) > 0:
                    text.append(strings)
                    strings: str = ""
                text.append(chars)

        # if name == "Staatsarchiv":
        #     print(text)

        # Die letzten 50 Einträge sind jeweils die
        # 'Tagesganglinien des Werktagverkehrs Mo - Fr'
        assert text[-50].endswith('Richtung 1'), f"{name} {path_pdf}"
        richtung1 = np.array(text[-49:-25], dtype=float)
        assert text[-25].endswith('Richtung 2')
        richtung2 = np.array(text[-24:], dtype=float)

        # Create DataFrame
        out = df({'time': TIME_24h,
                  'richtung1': richtung1,
                  'richtung2': richtung2})
        out.set_index('time', inplace=True)
        return out


if __name__ == "__main__":
    datapath = path.dirname(path.abspath(__file__))
    datapath = path.abspath(path.join(datapath, "..",
                                      "data", "geo.uri", "6025.pdf"))
    print(extract_from_pdf("EWA", TIME_24h, datapath))
