<<<<<<< Updated upstream
# installeer openapi_client pip install threedi-api-client
import os
import datetime
import subprocess
import shutil
import sqlite3
from osgeo import ogr

deelgebieden_fn = "/mnt/workdir/A_Feenstra/X0143 - Stikstof Limburg/deelgebieden.txt"
schematisaties_fn = "/mnt/workdir/A_Feenstra/X0143 - Stikstof Limburg/schematisaties.txt"
local_repo_dir_fn = "/mnt/workdir/A_Feenstra/X0143 - Stikstof Limburg/"

landuse_raster_src_dir = "/mnt/workdir/A_Feenstra/X0143 - Stikstof Limburg/"
dem_raster_src_dir = "/mnt/workdir/A_Feenstra/X0143 - Stikstof Limburg/"
sqlite_src_dir = "/mnt/workdir/"


pg_host = 'utr-gis-db-01'
pg_port = 5432
pg_user = 'postgis'
pg_password = 'postgis'
pg_database = 'x0143_stikstof'

def ogr_connection(host, port, user, password, database, **kwargs):
    ogr_conn = ("PG:host={} port={} user='{}'"
                "password='{}' dbname='{}'").format(host,
                                                    port,
                                                    user,
                                                    password,
                                                    database)
    return ogr.Open(ogr_conn)

def prepare_local_repository(deelgebied):
    
    print('Copying dem...')
    shutil.copyfile(src=os.path.join(dem_raster_src_dir, '{dgb}/schematisation/rasters/dem.tif'.format(dgb=deelgebied)),
                dst=os.path.join(local_repo_dir, 'rasters', 'dem.tif'))

    print('Copying landuse...')
    shutil.copyfile(src=os.path.join(landuse_raster_src_dir, '{dgb}/schematisation/rasters/landuse.tif'.format(dgb=deelgebied)),
                dst=os.path.join(local_repo_dir, 'rasters', 'landuse.tif'))

    print('Copying sqlite...')
    shutil.copyfile(src=os.path.join(sqlite_src_dir, 'w0203_zuid_holland_zh.sqlite'),
                dst=os.path.join(local_repo_dir, '{dgb}.sqlite'.format(dgb=deelgebied)))


    # sqlite
    sqlite_fn = os.path.join(local_repo_dir, '{dgb}.sqlite'.format(dgb=deelgebied))
    conn = sqlite3.connect(sqlite_fn)
    cur = conn.cursor()
    postgis = ogr_connection(host=pg_host, port=pg_port, user=pg_user, password=pg_password, database=pg_database)

    # global settings name
    print('Set global settings name...')
    sql = """UPDATE v2_global_settings SET name = '{dgb}';""".format(dgb=deelgebied)
    cur.execute(sql)
    conn.commit()


    print('Change dem dir...')
    sql = """UPDATE v2_global_settings SET dem_file = 'rasters/dem.tif';"""
    cur.execute(sql)
    conn.commit()

    print('Change friction dir...')
    sql = """UPDATE v2_global_settings SET frict_coef_file = 'rasters/friction.tif';"""
    cur.execute(sql)
    conn.commit()

    print('Change infiltration dir...')
    sql = """UPDATE v2_simple_infiltration SET infiltration_rate_file = 'rasters/infiltration_T25.tif';"""
    cur.execute(sql)
    conn.commit()



with open(deelgebieden_fn, "r") as deelgebieden:
    with open(schematisaties_fn, "r") as schematisaties: 
        for i in deelgebieden:    
            a = i.strip()
            for j in schematisaties:
                b = j.strip()
                c = str(a + ' ' + b)
                d = (local_repo_dir_fn + a +  'T25')
                local_repo_dir = (local_repo_dir_fn + c)
                prepare_local_repository(d)
                print ('Finished with '+ c)
print ('Finished')
=======
# installeer openapi_client pip install threedi-api-client
import os
import datetime
import subprocess
import shutil
import sqlite3
from osgeo import ogr

deelgebieden_fn = "/mnt/workdir/A_Feenstra/X0143 - Stikstof Limburg/deelgebieden.txt"
schematisaties_fn = "/mnt/workdir/A_Feenstra/X0143 - Stikstof Limburg/schematisaties.txt"
local_repo_dir_fn = "/mnt/workdir/A_Feenstra/X0143 - Stikstof Limburg/"

landuse_raster_src_dir = "/mnt/workdir/A_Feenstra/X0143 - Stikstof Limburg/"
dem_raster_src_dir = "/mnt/workdir/A_Feenstra/X0143 - Stikstof Limburg/"
sqlite_src_dir = "/mnt/workdir/"


pg_host = 'utr-gis-db-01'
pg_port = 5432
pg_user = 'postgis'
pg_password = 'postgis'
pg_database = 'x0143_stikstof'

def ogr_connection(host, port, user, password, database, **kwargs):
    ogr_conn = ("PG:host={} port={} user='{}'"
                "password='{}' dbname='{}'").format(host,
                                                    port,
                                                    user,
                                                    password,
                                                    database)
    return ogr.Open(ogr_conn)

def prepare_local_repository(deelgebied):
    
    print('Copying dem...')
    shutil.copyfile(src=os.path.join(dem_raster_src_dir, '{dgb}/schematisation/rasters/dem.tif'.format(dgb=deelgebied)),
                dst=os.path.join(local_repo_dir, 'rasters', 'dem.tif'))

    print('Copying landuse...')
    shutil.copyfile(src=os.path.join(landuse_raster_src_dir, '{dgb}/schematisation/rasters/landuse.tif'.format(dgb=deelgebied)),
                dst=os.path.join(local_repo_dir, 'rasters', 'landuse.tif'))

    print('Copying sqlite...')
    shutil.copyfile(src=os.path.join(sqlite_src_dir, 'w0203_zuid_holland_zh.sqlite'),
                dst=os.path.join(local_repo_dir, '{dgb}.sqlite'.format(dgb=deelgebied)))


    # sqlite
    sqlite_fn = os.path.join(local_repo_dir, '{dgb}.sqlite'.format(dgb=deelgebied))
    conn = sqlite3.connect(sqlite_fn)
    cur = conn.cursor()
    postgis = ogr_connection(host=pg_host, port=pg_port, user=pg_user, password=pg_password, database=pg_database)

    # global settings name
    print('Set global settings name...')
    sql = """UPDATE v2_global_settings SET name = '{dgb}';""".format(dgb=deelgebied)
    cur.execute(sql)
    conn.commit()


    print('Change dem dir...')
    sql = """UPDATE v2_global_settings SET dem_file = 'rasters/dem.tif';"""
    cur.execute(sql)
    conn.commit()

    print('Change friction dir...')
    sql = """UPDATE v2_global_settings SET frict_coef_file = 'rasters/friction.tif';"""
    cur.execute(sql)
    conn.commit()

    print('Change infiltration dir...')
    sql = """UPDATE v2_simple_infiltration SET infiltration_rate_file = 'rasters/infiltration_T25.tif';"""
    cur.execute(sql)
    conn.commit()



with open(deelgebieden_fn, "r") as deelgebieden:
    with open(schematisaties_fn, "r") as schematisaties: 
        for i in deelgebieden:    
            a = i.strip()
            for j in schematisaties:
                b = j.strip()
                c = str(a + ' ' + b)
                d = (local_repo_dir_fn + a +  'T25')
                local_repo_dir = (local_repo_dir_fn + c)
                prepare_local_repository(d)
                print ('Finished with '+ c)
print ('Finished')
>>>>>>> Stashed changes
