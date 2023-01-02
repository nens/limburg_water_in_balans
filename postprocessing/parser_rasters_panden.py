#!/usr/bin/env python
# coding: utf-8

# In[1]:


from osgeo import gdal
import glob
import os, fnmatch
import numpy as np
import csv
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import matplotlib.pyplot as plt


# In[2]:


base_path = "I:/Projecten_X_2022/x0143_stikstof/"

scenario = '100p'
bui = 't25'

Scenario = '100p'
Bui = 'T25'

final_path = "Results"
scenario_bui = str(Bui + ' ' + Scenario)
print (scenario_bui)

deelgebieden_fn = r"G:\Projecten X (2022)\X0143 - Modelberekeningen mogelijke effecten Wet Stikstofreductie Waterschap Limburg\Gegevens\Bewerking\Scripts\14 - Waterdiepterasters en kwetsbare panden analyseren\namen.txt" 
deelgebieden_db_fn = r"G:\Projecten X (2022)\X0143 - Modelberekeningen mogelijke effecten Wet Stikstofreductie Waterschap Limburg\Gegevens\Bewerking\Scripts\14 - Waterdiepterasters en kwetsbare panden analyseren\namen_db.txt"
deelgebieden_excel_fn = r"G:\Projecten X (2022)\X0143 - Modelberekeningen mogelijke effecten Wet Stikstofreductie Waterschap Limburg\Gegevens\Bewerking\Scripts\14 - Waterdiepterasters en kwetsbare panden analyseren\namen_excel.txt"
excel_fn = str("I:/Projecten_X_2022/x0143_stikstof/excel_modelresultaten/"+Bui + ".xlsx")

# DEFINE THE DATABASE CREDENTIALS
user = 'postgis'
password = 'postgis'
host = 'utr-gis-db-01.nens.local'
port = 5432
database = 'x0143_stikstof'

# In[3]:


Names=[]
h=-1
with open(deelgebieden_fn, "r") as deelgebieden:
    for i in deelgebieden:
        h += 1
        a = i.strip()
        Names.append(a)


# In[4]:


Statistics = np.zeros((11,4))
f = -1 
Names_1 = []
with open(deelgebieden_fn, "r") as deelgebieden:
    for i in deelgebieden:
        f += 1
        a = i.strip()
        Names_1.append(a)
        b = os.path.join(base_path, a, Bui, Scenario, final_path)
        os.chdir(b)
        c = glob.glob('*max_depth.tif')
        d = os.path.join(b, c[0])
        image = gdal.Open(d)
        image.RasterCount, image.RasterXSize, image.RasterYSize
        img = image.GetRasterBand(1)
        #min, max, mean, standard deviation
        e = img.GetStatistics(True, True)
        Statistics[f, 0] = e[0]
        Statistics[f, 1] = e[1]
        Statistics[f, 2] = e[2]
        Statistics[f, 3] = e[3]


# In[5]:

# PYTHON FUNCTION TO CONNECT TO THE POSTGRESQL DATABASE AND
# RETURN THE SQLACHEMY ENGINE OBJECT
def get_connection():
    return create_engine(
        url="postgresql://{0}:{1}@{2}:{3}/{4}".format(
            user, password, host, port, database
        )
    )
  
engine = get_connection()


# In[6]:


dbConnection    = engine.connect();


# In[7]:


Names_2 = []
Statistics_2 = np.zeros((11,5))
g=-1
with open(deelgebieden_db_fn, "r") as deelgebieden:
    for i in deelgebieden:
        g += 1
        a = i.strip()
        Names_2.append(a)
        sql_querie = str("select * from resultaten.kw_"+ a + "_" + bui + "_"+ scenario)
        dataFrame       = pd.read_sql(sql_querie, dbConnection)
        
        kosten = np.sum(dataFrame['kosten'])
        print ('De totale kosten voor ' + a + ' ' + bui + ' ' + scenario + ' is €', round((kosten/1000000), 0),'miljoen')
        
        kwetsbare_panden_totaal = 0 
        kwetsbare_panden_adres = 0
        kwetsbare_panden_lokaal = 0
        kwetsbare_panden_regionaal = 0
        for index, row in dataFrame.iterrows():
            if row['knelpunt'] == 'lokaal':
                kwetsbare_panden_lokaal += 1 
        for index, row in dataFrame.iterrows():
            if row['knelpunt'] == 'regionaal':
                kwetsbare_panden_regionaal += 1 
        for index, row in dataFrame.iterrows():
            if row['knelpunt'] != 'geen knelpunt' and row['adres'] == 1:
                kwetsbare_panden_adres += 1 
        for index, row in dataFrame.iterrows():
            if row['knelpunt'] != 'geen knelpunt':
                kwetsbare_panden_totaal += 1 
                
        print ('Totaal zijn in ' + a + ' ' + bui + ' ' + scenario , kwetsbare_panden_totaal, 'panden kwetsbaar' )
        
        Statistics_2[g, 0] = kosten
        Statistics_2[g, 1] = kwetsbare_panden_totaal
        Statistics_2[g, 2] = kwetsbare_panden_adres
        Statistics_2[g, 3] = kwetsbare_panden_lokaal
        Statistics_2[g, 4] = kwetsbare_panden_regionaal
        


# In[ ]:


Stats = {'Model': Names, 'min':Statistics[:,0], 'max':Statistics[:,1], 'mean':Statistics[:,2], 'std':Statistics[:,3], 'kwetsbare panden lokaal':Statistics_2[:,3], 'kwetsbare panden regionaal':Statistics_2[:,4], 'kwetsbare panden totaal':Statistics_2[:,1], 'kwetsbare panden waarvan adres':Statistics_2[:,2], 'kosten':Statistics_2[:, 0], 'raster naam':Names_1, 'database naam':Names_2}
Stats_df = pd.DataFrame(data=Stats)


# In[ ]:


Stats_df


# In[ ]:
with pd.ExcelWriter(excel_fn, engine='openpyxl', mode='a') as writer:  
    Stats_df.to_excel(writer, sheet_name=Scenario)
#Stats_df.to_excel(excel_fn, sheet_name=Scenario)
print ('Data has been written to Excel' , Bui, '.xlsx')


# In[ ]:




