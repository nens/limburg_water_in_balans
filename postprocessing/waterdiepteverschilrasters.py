#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np 
import glob
import subprocess


# In[2]:


deelgebieden_fn = "deelgebieden.txt"
results_fn = 'I:/Projecten_X_2022/x0143_stikstof/Waterdiepteverschilrasters/T100/'


# In[3]:


# %load waterdepthdiff.py
#!/usr/bin/env python
""" Calculate difference between two overlapping water depth tiffs. Result is raster2 - raster1."""

import argparse
import sys
import numpy as np
import os
from osgeo import gdal, osr
gdal.UseExceptions()

STYLESTRING = """<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis maxScale="0" version="3.4.12-Madeira" hasScaleBasedVisibilityFlag="0" styleCategories="AllStyleCategories" minScale="1e+08">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <customproperties>
    <property value="false" key="WMSBackgroundLayer"/>
    <property value="false" key="WMSPublishDataSourceUrl"/>
    <property value="0" key="embeddedWidgets/count"/>
    <property value="Value" key="identify/format"/>
  </customproperties>
  <pipe>
    <rasterrenderer alphaBand="-1" band="1" classificationMax="0.5" type="singlebandpseudocolor" opacity="1" classificationMin="-0.5">
      <rasterTransparency>
        <singleValuePixelList>
          <pixelListEntry max="0.01" min="-0.01" percentTransparent="100"/>
        </singleValuePixelList>
      </rasterTransparency>
      <minMaxOrigin>
        <limits>None</limits>
        <extent>WholeRaster</extent>
        <statAccuracy>Estimated</statAccuracy>
        <cumulativeCutLower>0.02</cumulativeCutLower>
        <cumulativeCutUpper>0.98</cumulativeCutUpper>
        <stdDevFactor>2</stdDevFactor>
      </minMaxOrigin>
      <rastershader>
        <colorrampshader clip="0" classificationMode="1" colorRampType="INTERPOLATED">
          <colorramp name="[source]" type="gradient">
            <prop v="77,172,38,255" k="color1"/>
            <prop v="208,28,139,255" k="color2"/>
            <prop v="0" k="discrete"/>
            <prop v="gradient" k="rampType"/>
            <prop v="0.25;184,225,134,255:0.5;247,247,247,255:0.75;241,182,218,255" k="stops"/>
          </colorramp>
          <item alpha="255" color="#4dac26" label="-0.5" value="-0.5"/>
          <item alpha="255" color="#b8e186" label="-0.25" value="-0.25"/>
          <item alpha="255" color="#f7f7f7" label="0" value="0"/>
          <item alpha="255" color="#f1b6da" label="0.25" value="0.25"/>
          <item alpha="255" color="#d01c8b" label="0.5" value="0.5"/>
        </colorrampshader>
      </rastershader>
    </rasterrenderer>
    <brightnesscontrast contrast="0" brightness="0"/>
    <huesaturation saturation="0" colorizeBlue="128" colorizeOn="0" colorizeRed="255" grayscaleMode="0" colorizeStrength="100" colorizeGreen="128"/>
    <rasterresampler maxOversampling="2"/>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
"""

def getExtent(raster):
    gt=raster.GetGeoTransform()
    ulx=gt[0]
    uly=gt[3]
    lrx=gt[0] + (raster.RasterXSize*gt[1])
    lry=gt[3] + (raster.RasterYSize*gt[5]) # '+' because gt[5] is negative
    return [ulx, uly, lrx, lry]

def getSharedExtent(extent1, extent2):
    ulx = max(extent1[0], extent2[0])
    uly = min(extent1[1], extent2[1])
    lrx = min(extent1[2], extent2[2])
    lry = max(extent1[3], extent2[3])
    
    return [ulx, uly, lrx, lry] 

def WaterDepthDiff(raster1_fn, raster2_fn, outputraster):
    # 1. Lees beide rasters in 
    raster1 = gdal.Open(raster1_fn)
    raster2 = gdal.Open(raster2_fn)
    
    # raise error if pixel sizes differ
    assert raster1.GetGeoTransform()[1] == raster2.GetGeoTransform()[1]
    assert raster1.GetGeoTransform()[5] == raster2.GetGeoTransform()[5]
    
    # raise error if pixel skews differ
    assert raster1.GetGeoTransform()[2] == raster2.GetGeoTransform()[2]
    assert raster1.GetGeoTransform()[4] == raster2.GetGeoTransform()[4]
    
    # raise error if projections differ
    ## assert raster1.GetProjection() == raster2.GetProjection()
        
    # Als extents verschillen: 
        # 2. Bepaal gemeenschappelijke extent 
        # 3. Knip de rasters op die gemeenschappelijke extent met gdal.Translate 
    # 4 Lees het resultaat van beiden in als array
    
        
    raster1extent = getExtent(raster1)
    raster2extent = getExtent(raster2)
    
    if raster1extent == raster2extent:
        raster1Array = raster1.ReadAsArray()
        raster2Array = raster2.ReadAsArray()
        gt = raster1.GetGeoTransform()
    
    else:
        sharedExtent = getSharedExtent(raster1extent, raster2extent)
        
        raster1SharedExt = gdal.Translate('', raster1, format='MEM', projWin=sharedExtent)
        raster1Array = raster1SharedExt.ReadAsArray()
        raster1SharedExt = None
        
        raster2SharedExt = gdal.Translate('', raster2, format='MEM', projWin=sharedExtent)
        raster2Array = raster2SharedExt.ReadAsArray()
        raster2SharedExt = None
        
        gt = list(raster1.GetGeoTransform()) #(upper_left_x, x_resolution, x_skew, upper_left_y, y_skew, y_resolution)
        gt[0] = sharedExtent[0]
        gt[3] = sharedExtent[1] 
        gt = tuple(gt)
    
    # 5 Vervang alle nodatavalues door 0
    ndv1 = raster1.GetRasterBand(1).GetNoDataValue()
    raster1Array[np.where(raster1Array==ndv1)] = 0
    ndv2 = raster2.GetRasterBand(1).GetNoDataValue()
    raster2Array[np.where(raster2Array==ndv2)] = 0
    
    # 6 Bereken verschilarray
    result = np.subtract(raster2Array, raster1Array)
    
    # 7 Schrijf weg naar raster met 0 als nodatavalue
    height = result.shape[0] # dit nog aanpassen als stap 2 & 3 worden geimplementeerd
    width = result.shape[1] # dit nog aanpassen als stap 2 & 3 worden geimplementeerd
    
    wkt = raster1.GetProjection()
    
    if os.path.exists(outputraster):
        os.remove(outputraster)
    
    drv = gdal.GetDriverByName('Mem')
    ds = drv.Create('', xsize=width, ysize=height, bands=1, eType=gdal.GDT_Float32)
    ds.SetGeoTransform(gt)
    ds.SetProjection(wkt)
    ds.GetRasterBand(1).SetNoDataValue(0)
    ds.GetRasterBand(1).WriteArray(result)
    
    dst_drv = gdal.GetDriverByName('GTiff')
    dst_ds = dst_drv.CreateCopy(outputraster, ds, options=["TILED=YES", "COMPRESS=DEFLATE"])
    dst_ds = None
    ds = None
    
    ext_len = len(os.path.basename(outputraster).split('.')[-1])
    qml_fn = outputraster[:-1*ext_len-1] + '.qml'
    
    with open(qml_fn, "w") as qml:
        qml.write(STYLESTRING)

def get_parser():
    """ Return argument parser. """
    parser = argparse.ArgumentParser(
        description=__doc__
    )
    parser.add_argument('raster1_fn')
    parser.add_argument('raster2_fn')
    parser.add_argument('outputraster')
    return parser


# In[ ]:


with open(deelgebieden_fn) as deelgebieden: 
    for i in deelgebieden:
        a = i.strip()
        for j in ['25p', '50p', '75p', '100p']:
            input1 = glob.glob('I:/Projecten_X_2022/x0143_stikstof/' + a + '/T100/Basis/Results/*max_depth.tif')
            print ("raster1:", input1[0])
            input2 = glob.glob('I:/Projecten_X_2022/x0143_stikstof/' + a + '/T100/' + j + '/Results/*max_depth.tif')
            print ("raster2:", input2[0])
            output = results_fn + a + '_scenario_' + j + '_Basis.tif'
            print ("output:", output)
            WaterDepthDiff(input1[0], input2[0], output)
            print ('Waterdiepteraster is klaar')

