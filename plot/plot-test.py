# import required module
import os
import pandas as pd

# assign directory
directory = '../data/DatenSisag/Verkehrsdaten/Rohdaten Auswertungfiles xls/test'
dflist = {}
messstelle = ""
con = None

# iterate over files in
# that directory
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        print(f)
        if filename.startswith("ok_") :
            messstelle =  filename[3:7]
        else:
            messstelle = filename[0:4]
        # if dataframe exists then append data to dataframe
        tmp_df = pd.read_excel(f, sheet_name=None)
        if messstelle in dflist:
            old = dflist[messstelle]
            frames = [old, tmp_df]
            con = pd.concat(frames)
            con.to_excel("merge.xlsx")
        else:
            dflist[messstelle] = tmp_df

print(len(dflist[messstelle]))