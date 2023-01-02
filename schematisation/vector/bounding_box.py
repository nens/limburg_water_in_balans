# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 11:04:36 2022

@author: ruben.vanderzaag
"""
#script werkt in superputty
import os
import pandas as pd
from osgeo import ogr
import geopandas as gpd

path_schematisaties = "namen.txt"
schematisaties = pd.read_csv(path_schematisaties)

for index, row in schematisaties.iterrows():
    schem = row['namen']
    file_out = "/mnt/workdir/A_Feenstra/X0143 - Stikstof Limburg/deelgebieden/" + schem + "/T25/Basis/schematisation/bounding_box/bounding_box.shp"
    path_DEM = "/mnt/workdir/A_Feenstra/X0143 - Stikstof Limburg/deelgebieden/" + schem + "/T25/Basis/schematisation/rasters/dem.tif"
    os.system(f"gdaltindex {file_out} {path_DEM}")
    gdf = gpd.read_file(file_out)
    gdf["rasters"]= "rasters"
    gdf.to_file(file_out)



