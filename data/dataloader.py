from pandas.core.indexes.datetimes import DatetimeIndex
from os.path import isfile
from pdfreader import SimplePDFViewer
import numpy as np
import pandas as pd
from pandas.core.frame import DataFrame as df
from os import path
import time
from joblib import Parallel, delayed


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


def extract_pickle() -> df:
    datapath = path.dirname(path.abspath(__file__))
    picklef: str = path.abspath(path.join(datapath, "DatenSisag",
                                          "dfipynb.pickle"))
    assert path.isfile(picklef)
    dataf: df = pd.read_pickle(picklef)
    dataf.dropna(inplace=True)
    print(dataf.head(100))

    def anpassung_zeit(df):
        df.HHMM = df.HHMM / 100
        df['HHMM'] = df['HHMM'].replace(24.0, 23.59)
        df['Datum und Zeit'] = df["Datum"].astype(str).str[:10] \
            + ' ' + df.HHMM.astype(str)
        df['Datumszeit'] = pd.to_datetime(df['Datum und Zeit'],
                                          format='%Y-%m-%d %H.%M',
                                          errors="coerce")
        return df

    def delete_rows(df):
        df = df[df['Querschnitt'].notna()]
        df.drop(columns=["Datum", "HHMM", "Datum und Zeit"], inplace=True)
        return df

    dataf = anpassung_zeit(dataf)
    dataf = delete_rows(dataf)
    return dataf

def load_xlsx_to_pickle(path, picklefilename) -> df
    # iterate over files in
    # that directory
    filenames = []
    for filename in os.listdir(path):
        f = os.path.join(path, filename)
        # checking if it is a file
        #if os.path.isfile(f):
        filenames.append(f)

    def loop(file):
        variant=""
        try:
            dfxlsx = pd.read_excel(file, sheet_name=None)
            if len(dfxlsx.items()) == 1:
                dfxlsx=pd.concat(dfxlsx.values(), names=dfxlsx.keys())#
                variant="1:"
                pass
            else:
                dfxlsx=pd.concat(dfxlsx.values(), names=dfxlsx.keys())
                variant="2:"
        except Exception as e:
            print(e)
        print(variant+"file:"+file)
        return dfxlsx


    df = Parallel(n_jobs=-1, verbose=0, prefer="threads")(delayed(loop)(file) for file in filenames)
    df_concat = pd.DataFrame()
    df_concat = pd.concat(df, ignore_index=True)
    df_concat.to_pickle(picklefilename)
    return df_concat


if __name__ == "__main__":
    data: df = extract_pickle()
    print(data.columns)
    print(data.head(100))
