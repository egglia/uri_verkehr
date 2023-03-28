import folium
from folium import plugins
from folium.features import DivIcon
import io
from PIL import Image

from map.gif import make_gif
from map.map import VerkehrsMessPunkt, TIME_24h, ALTDORF_KOORD, endkoord, color


standorte: list = [VerkehrsMessPunkt("Dorfeinfahrt Galabau AG Hess",
                                     [46.882652, 8.618019],
                                     "6202.pdf",
                                     60),  # Richtung 1: Altdorf
                   VerkehrsMessPunkt("Pumpstation ARA Altdorf",
                                     [46.883908, 8.626009],
                                     "6015.pdf",
                                     120),  # Altdorf
                   VerkehrsMessPunkt("Steinmatt/Gewerbezentrum",
                                     [46.872906, 8.632481],
                                     "6013.pdf",
                                     170),  # Schattdorf
                   VerkehrsMessPunkt("Attinghauserstrasse",
                                     [46.867579, 8.635087],
                                     "6019.pdf",
                                     200),  # Rynächtstrasse
                   VerkehrsMessPunkt("Nördlich Schlosserei Trögli",
                                     [46.881264, 8.623339],
                                     "6002.pdf",
                                     160),  # Attinghausen
                   VerkehrsMessPunkt("Kollegium",
                                     [46.873726, 8.650481],
                                     "6026.pdf",
                                     175),  # Schattdorf
                   # 6017.pdf Nur Rohdaten Totalwerte :(
                   # VerkehrsMessPunkt("Kant. Verwaltung",
                   #                   [46.874779, 8.652993],
                   #                   "6017.pdf",
                   #                   115),  # Glarus
                   VerkehrsMessPunkt("Lawil AG Haus Nr. 41",
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

    # Add legend: Arrow of 1 km corresponds to 1000 cars per hour
    legend_corner = [46.866227, 8.596747]
    endk = endkoord(legend_corner, 0, 1.)  # 1 km nach 0° Nord
    pfeil = plugins.AntPath(locations=[legend_corner, endk],
                            dash_array=[0, 100], weight=10,
                            color=color(0))
    map_osm.add_child(pfeil)
    text: str = " 1000 Fz/h"
    folium.map.Marker(
        endk,
        icon=DivIcon(
            icon_size=(150, 36),
            icon_anchor=(0, 0),
            html='<div style="font-size: 24pt">%s</div>' % text,
        )
    ).add_to(map_osm)

    print(f"..Starte Extraktion als PNG für t={tidx}")
    # Requires Firefox browser and 'pip install SELENIUM' to work
    img_data = map_osm._to_png(3)  # second rendering time max
    img = Image.open(io.BytesIO(img_data))
    fname = f'arrows_map_{tidx}.png'
    img.save(fname)

# Generate a .gif out of all pngs
make_gif('Altdorf_Verkehr.gif')
