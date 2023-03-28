from os import path
import math
import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib import pyplot as plt
import matplotlib.colors

from data.dataloader import extract_from_pdf, TIME_24h

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
