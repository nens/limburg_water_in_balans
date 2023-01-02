# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 12:09:16 2022

@author: ruben.vanderzaag
"""
import threedi_raster_edits as tre

#Padverwijzingen
input_raster =  r"K:/R_vdZaag/Stikstof_limburg/schem/Banholt-Mheer/T25/25p/schematisation/rasters/landgebruik.tif"
input_shape = r"G:\Projecten X (2022)\X0143 - Modelberekeningen mogelijke effecten Wet Stikstofreductie Waterschap Limburg\Gegevens\Bewerking\Grasland_polygonen\25p.shp"
clipped_shape = r"K:/R_vdZaag/Stikstof_limburg/schem/Banholt-Mheer/T25/25p/schematisation/rasters/clipped.shp"
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
clipped.write(clipped_shape)

#Raster landgebruik burnen obv shapefile veetilt 
lu2 = landgebruik.copy()
pushed = lu2.push_vector(clipped, value=17)
pushed.replace_nodata()
pushed.write(input_raster)
