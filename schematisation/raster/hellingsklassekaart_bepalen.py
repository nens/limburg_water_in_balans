# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 16:32:53 2022

@author: ruben.vanderzaag
"""

from osgeo import gdal
import numpy as np
import os

def bereken_hellingsklasse(dem_path, output_path, res_dem):
    dem_ds = gdal.Open(dem_path)
    dem_resampled_ds = gdal.Warp("mem", dem_ds, xRes = 5, yRes = 5) #evt. 5*res_dem
    
    #Helling berekenen
    opt = gdal.DEMProcessingOptions(
        format="Mem",
        slopeFormat="percent",
    )
    slope_ds = gdal.DEMProcessing("", dem_resampled_ds, "slope", options=opt)
    
    #Hellingsklasse berekenen
    hellingsklasse = slope_ds.GetRasterBand(1).ReadAsArray()
    
    hellingsklasse[np.logical_and(hellingsklasse>-9999, hellingsklasse<4)] = 1
    hellingsklasse[np.logical_and(hellingsklasse>=4, hellingsklasse<7)] = 2
    hellingsklasse[np.logical_and(hellingsklasse>=7, hellingsklasse<12)] = 3
    hellingsklasse[hellingsklasse>=12] = 4
    
    # Schrijf weg naar raster met 0 als nodatavalue
    height = hellingsklasse.shape[0]
    width = hellingsklasse.shape[1] 
    
    proj_wkt = dem_resampled_ds.GetProjection()
    gt = dem_resampled_ds.GetGeoTransform()
    
    if os.path.exists(output_path):
        os.remove(output_path)
    
    drv = gdal.GetDriverByName('Mem')
    helling_ds = drv.Create('', xsize=width, ysize=height, bands=1, eType=gdal.GDT_Float32)
    helling_ds.SetGeoTransform(gt)
    helling_ds.SetProjection(proj_wkt)
    helling_ds.GetRasterBand(1).SetNoDataValue(-9999)
    helling_ds.GetRasterBand(1).WriteArray(hellingsklasse)
    
    #resultaat opslaan
    gdal.Warp(output_path, helling_ds, xRes = res_dem, yRes = res_dem)

#Hier loop omheen bouwen:
resolutie = 1 #dit importeren uit txt per model    
#Padverwijzingen
path_DEM = r"K:\R_vdZaag\Stikstof_limburg\Schematisations\Geul_midden\dem_geul_midden_copy.tif"
path_hellingsklasse = r"K:\R_vdZaag\Stikstof_limburg\Schematisations\Geul_midden\hellingsklasse_geul_midden.tif"
#aanroepen functie
bereken_hellingsklasse(path_DEM,path_hellingsklasse,resolutie)
