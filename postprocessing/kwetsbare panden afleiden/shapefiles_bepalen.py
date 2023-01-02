# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 11:55:26 2022

@author: ruben.vanderzaag
"""
import os
from osgeo import gdal

path_DEM = r'K:\R_vdZaag\Stikstof_limburg\Schematisations\Geul_midden\dem_geul_midden.tif'
path_output = r'K:\R_vdZaag\Stikstof_limburg\Schematisations\Geul_midden\geul_midden.shp'
os.system(f"gdal_polygonize.py {path_DEM} {path_output}")


from osgeo import gdal, ogr, osr

in_path = r'K:\R_vdZaag\Stikstof_limburg\Schematisations\Geul_midden\dem_geul_midden.tif'

out_path = r'K:\R_vdZaag\Stikstof_limburg\Schematisations\Geul_midden\geul_midden.shp'

#  get raster datasource
src_ds = gdal.Open( in_path )
#
srcband = src_ds.GetRasterBand(1)
dst_layername = 'oilpalm_HarvestedAreaHectares'
drv = ogr.GetDriverByName("ESRI Shapefile")
dst_ds = drv.CreateDataSource( out_path )

sp_ref = osr.SpatialReference()
sp_ref.SetFromUserInput('EPSG:4326')

dst_layer = dst_ds.CreateLayer(dst_layername, srs = sp_ref )

fld = ogr.FieldDefn("HA", ogr.OFTInteger)
dst_layer.CreateField(fld)
dst_field = dst_layer.GetLayerDefn().GetFieldIndex("HA")

gdal.Polygonize( srcband, None, dst_layer, dst_field, [], callback=None )

del src_ds
del dst_ds