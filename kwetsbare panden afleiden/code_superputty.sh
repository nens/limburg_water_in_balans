#############################################################
## SHAPEFILES
###############################################################
echo $(date '+ %H:%M:%S') "Ik ben gestart :)"

##PRESET PASSWORD OF DATABASE
echo "utr-gis-db-01:5432:*:postgis:postgis" > ~/.pgpass
chmod 0600 ~/.pgpass

while read p; do
    c=1
    IFS='|' read -ra vars <<< "$p"
    for i in "${vars[@]}"; do eval "v$c=$i"; c=$((c+1)); done
    echo $(date '+ %H:%M:%S') Begonnen met scenario $v1

    gdal_calc.py -A waterdiepterasters/$v1.tif --outfile=result.tif --calc="(A>0.02)*1+(A<0.02)*-9999" --NoDataValue=-9999

    gdal_polygonize.py result.tif $v1"_polygons".shp  -f "ESRI SHAPEFILE" OUTPUT DN
    ogr2ogr -overwrite -f "PostgreSQL" PG:"host=utr-gis-db-01 user=postgis dbname=w0154_hekerbeekdal password=postgis port=5432" -nln watervlakken $v1"_polygons".shp -a_srs EPSG:28992 -lco GEOMETRY_NAME=geom 

    ogr2ogr -overwrite -f "PostgreSQL" PG:"host=utr-gis-db-01 user=postgis dbname=w0154_hekerbeekdal password=postgis port=5432" -nln deelgebied shapefiles_deelgebieden/Plangebied.shp -a_srs EPSG:28992 -lco GEOMETRY_NAME=geom -lco precision=NO
	
    psql -h utr-gis-db-01 -p 5432 -U postgis -d w0154_hekerbeekdal -f combineer_watervlakken_panden.sql
    
    ogr2ogr -f "ESRI Shapefile" panden_buffer_$v1.shp PG:"host=utr-gis-db-01 user=postgis dbname=w0154_hekerbeekdal password=postgis port=5432" "tmp.pand_tot" -lco GEOMETRY_NAME=geom 
    zonal panden_buffer_$v1.shp panden_stats_$v1.shp -r waterdiepterasters/$v1.tif -s max median

    ogr2ogr -overwrite -f "PostgreSQL" PG:"host=utr-gis-db-01 user=postgis dbname=w0154_hekerbeekdal password=postgis port=5432" -nln panden_met_stats -nlt PROMOTE_TO_MULTI panden_stats_$v1.shp -a_srs EPSG:28992 -lco GEOMETRY_NAME=geom 

    # **SQL CODE:opslaan_resultaten**
	
    psql -h utr-gis-db-01 -p 5432 -U postgis -d w0154_hekerbeekdal -c "update panden_met_stats set max=0 where max='Nan';"

    psql -h utr-gis-db-01 -p 5432 -U postgis -d w0154_hekerbeekdal -c "CREATE TABLE resultaten.$v1 AS select pand.identifica,pand.bouwjaar,pand.adres, pand.pand as geom,stats.area,stats.max,stats.median, CASE WHEN stats.max>0.15 and stats.area>200 THEN 'regionaal' WHEN stats.max>0.15 AND stats.area<200 THEN 'lokaal' ELSE 'geen knelpunt' END as knelpunt from tmp.pand_tot pand, panden_met_stats stats where stats.identifica=pand.identifica"
    
    rm *$v1*.{shp,shx,prj,dbf}
    rm result.tif

    echo $(date '+ %H:%M:%S') Klaar met scenario $v1
    
done < deelgebieden.txt

echo $(date '+ %H:%M:%S') "Klaar met batch"