# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 12:09:16 2022

@author: ruben.vanderzaag
"""

#dit wordt aangeroepen wanneer landgebruik_aanpassen.sh wordt gerund in superputty
import threedi_raster_edits as tre
import os
import sys

input_raster = sys.argv[1]
output_raster = sys.argv[2]
input_shape = sys.argv[3]

print(input_raster)
print(output_raster)
print(input_shape)

os.rename(output_raster,input_raster)

landgebruik = tre.Raster(input_raster)
shapefile = tre.Vector(input_shape)

#Mask maken obv landgebruik vector
lu = landgebruik.copy()
array = lu.array 
lu.array = array > 0   
shape = tre.Vector(lu.polygonize(quiet=False,mask_value=0))

#Shapefiles veetilt gebieden clippen obv mask
filtered = shapefile.spatial_filter(shape)
clipped = shapefile.clip(shape)

#Raster landgebruik burnen obv shapefile veetilt 
lu2 = landgebruik.copy()
pushed = lu2.push_vector(clipped, value=17)
pushed.replace_nodata()
pushed.write(output_raster)