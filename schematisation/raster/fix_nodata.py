# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 14:16:25 2022

@author: abe.feenstra
"""


import pathlib
import threedi_raster_edits as tre
import os

path = (r"I:\Projecten_X_2022\x0143_stikstof\Geul_Midden\T100\75p\schematisation\Geul_Midden T100.sqlite")
out_path = (r"I:\Projecten_X_2022\x0143_stikstof\Geul_Midden\T100\75p\schematisation\rasters\new")
os.makedirs(out_path)
print (path)
model = tre.ThreediEdits(str(path))
rasters = model.rasters
rasters.correct()
rasters.write(str(out_path))

print(rasters.properties)  