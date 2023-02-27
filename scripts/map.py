from os import path
import folium
from folium import plugins
import io
import math
import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib import pyplot as plt
import matplotlib.colors
from PIL import Image

from data.dataloader import extract_from_pdf, TIME_24h
from scripts.gif import make_gif

# Constants:
RAD_EARTH = 6371.0  # Earth's radius in kilometers
ALTDORF_KOORD = [46.8800, 8.6433]


def endkoord(startkoord: list,
             degrees: float,
             lenght_km: float) -> tuple:
    # Inputs
    lat1 = math.radians(startkoord[0])
    lon1 = math.radians(startkoord[1])
    brng = math.radians(degrees)  # Bearing in degrees converted to radians

    # Calculate destination coordinates using Vincenty formula
    lat2 = math.asin(math.sin(lat1) * math.cos(lenght_km / RAD_EARTH)
                     + math.cos(lat1) * math.sin(lenght_km / RAD_EARTH)
                     * math.cos(brng))
    lon2 = lon1 + math.atan2(math.sin(brng)
                             * math.sin(lenght_km / RAD_EARTH)
                             * math.cos(lat1),
                             math.cos(lenght_km / RAD_EARTH) - math.sin(lat1)
                             * math.sin(lat2))
    # Convert destination coordinates to degrees
    lat2 = math.degrees(lat2)
    lon2 = math.degrees(lon2)
    return [lat2, lon2]


def distance_km(koord_1: list,
                koord_2: list):
    # Inputs
    lat1 = math.radians(koord_1[0])
    lon1 = math.radians(koord_1[1])
    lat2 = math.radians(koord_2[0])
    lon2 = math.radians(koord_2[1])

    # Calculate differences
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Calculate Haversine formula
    a = math.sin(dlat / 2) ** 2 \
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = RAD_EARTH * c
    return distance  # in km


def color(direction: float):
    # Generate color scripts
    num_colors = 256
    color_array = plt.get_cmap('hsv')(range(num_colors))
    color_map = ListedColormap(color_array)

    # Map data to colors
    color_values = direction / 365.0 * num_colors
    color: tuple = color_map(np.mod(round(color_values), num_colors))
    return matplotlib.colors.to_hex(color)


class VerkehrsMessPunkt:
    def __init__(self,
                 name: str,  # Standortbezeichnung:
                 koord: list,  # z. Bsp. [46.8800, 8.6433]
                 pdf: str,  # z. Bsp. "6011.pdf"
                 r1_deg: float,  # Richtung 1 in °, z. Bsp. 250°
                 ):
        self.name: str = name
        assert distance_km(koord, ALTDORF_KOORD) < 20., "Punkt sehr weit weg?"
        self.koord: tuple = koord

        datapath = path.dirname(path.abspath(__file__))
        datapath = path.abspath(path.join(datapath, "..",
                                          "data", "geo.uri", pdf))
        assert path.isfile(datapath)
        self.pdfpath: str = datapath

        assert 0. <= r1_deg <= 365.
        self.r1_deg: float = r1_deg
        r2_deg = (r1_deg + 180) % 365
        self.r2_deg: float = r2_deg

        # Extract data from pdf
        self.data = extract_from_pdf(self.name, TIME_24h, self.pdfpath)


if __name__ == "__main__":

    standorte: list = [VerkehrsMessPunkt("Lawil AG Haus Nr. 41",
                                         [46.897804, 8.625363],
                                         "5401.pdf",
                                         160),  # nach Altdorf
                       VerkehrsMessPunkt("Östlich Allmendstrasse",
                                         [46.888949, 8.622716],
                                         "6011.pdf",
                                         240),  # Schattdorf
                       VerkehrsMessPunkt("Pumpwerk Weidbach Seedorf",
                                         [46.887104, 8.603902],
                                         "6203.pdf",
                                         135),  # Altdorf
                       VerkehrsMessPunkt("JB Bau",
                                         [46.885623, 8.635232],
                                         "6003.pdf",
                                         135),  # Altdorf
                       VerkehrsMessPunkt("Personalhaus",
                                         [46.882854, 8.636655],
                                         "6009.pdf",
                                         60),  # Flüelerstrasse
                       VerkehrsMessPunkt("EWA",
                                         [46.883092, 8.639164],
                                         "6025.pdf",
                                         120),  # Altdorf
                       VerkehrsMessPunkt("Schulhaus Hagen",
                                         [46.880706, 8.638702],
                                         "6004.pdf",
                                         130),  # Altdorf
                       VerkehrsMessPunkt("Dätwyler Stiftung",
                                         [46.879571, 8.639728],
                                         "6021.pdf",
                                         190),  # Rynächtstrasse
                       VerkehrsMessPunkt("Gisler Druck",
                                         [46.878692, 8.639604],
                                         "6020.pdf",
                                         185),  # Rynächtstrasse
                       VerkehrsMessPunkt("Staatsarchiv",
                                         [46.880602, 8.641298],
                                         "6023.pdf",
                                         300),  # Bahnhofstrasse
                       # 6010.pdf hat ein unbrauchbares pdf format
                       # VerkehrsMessPunkt("Staatsarchiv",  # gleich wie oben!
                       #                   [46.881186, 8.641302],
                       #                   "6010.pdf",
                       #                   60),  # Tellsgasse
                       VerkehrsMessPunkt("St. Karl",
                                         [46.880006, 8.642534],
                                         "6024.pdf",
                                         230),  # Bahnhofstrasse
                       VerkehrsMessPunkt("Amavita Apotheke",
                                         [46.880825, 8.643648],
                                         "6018.pdf",
                                         190),  # Bahnhofstrasse
                       VerkehrsMessPunkt("Turmmattweg",
                                         [46.875895, 8.649334],
                                         "6014.pdf",
                                         140),  # Schattdorf
                       VerkehrsMessPunkt("Bifang/ Milchzentrale",
                                         [46.879292, 8.631181],
                                         "6016.pdf",
                                         175),  # Bahnhof Altdorf
                       # # Messtelle 2022 defekt -> pdf unbrauchbar
                       # VerkehrsMessPunkt("Bauernhof",
                       #                   [],
                       #                   "6022.pdf",
                       #                   ),  #
                       ]
    print("Daten aus PDFs extrahiert")

    for tidx, t in enumerate(TIME_24h):
        # Create a scripts centered on Altdorf
        map_osm = folium.Map(location=ALTDORF_KOORD, zoom_start=14,
                             tiles='Stamen Toner', attr='')  # grayscale

        # TODO put into a function
        for stdort in standorte:
            # # mark the location of the metering station
            # marker = folium.Marker(stdort.koord,
            #                        icon_size=(5, 5))  # A bit smaller icon
            # marker.add_to(map_osm)

            # Erstelle Pfeile für Richtung 1: 1 km pro 1'000 Fahrzeuge
            endpnt = endkoord(stdort.koord,  # Startkoordinate
                              stdort.r1_deg,  # in welche Richtung der Pfeil
                              stdort.data.loc[t, 'richtung1'] / 1000.)
            arrow_coords = [stdort.koord, endpnt]
            # Create an Line that indicates the traffic volume
            pfeil = plugins.AntPath(locations=arrow_coords,
                                    dash_array=[0, 100], weight=10,
                                    color=color(stdort.r1_deg))
            map_osm.add_child(pfeil)

            # Dito für Gegenrichtung:
            endpnt = endkoord(stdort.koord,  # Startkoordinate
                              stdort.r2_deg,  # in welche Richtung der Pfeil
                              stdort.data.loc[t, 'richtung2'] / 1000.)
            arrow_coords = [stdort.koord, endpnt]
            pfeil = plugins.AntPath(locations=arrow_coords,
                                    dash_array=[0, 100], weight=10,
                                    color=color(stdort.r2_deg))
            map_osm.add_child(pfeil)

        print(f"..Starte Extraktion als PNG für t={tidx}")
        # Requires Firefox browser and 'pip install SELENIUM' to work
        img_data = map_osm._to_png(3)  # second rendering time max
        img = Image.open(io.BytesIO(img_data))
        fname = f'arrows_map_{tidx}.png'
        img.save(fname)

    # Generate a .gif out of all pngs
    make_gif('Altdorf_Verkehr.gif')
