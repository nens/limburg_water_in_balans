#############################################################
## SHAPEFILES
###############################################################
# echo $(date '+ %H:%M:%S') "Ik ben gestart :)"
# dit script is te gebruiken voor een enkel deelgebied. Voor meerdere deelgebieden, gebruik code_superputty_meerdere_dgbn
# run met "bash code_superputty_een_dgb.sh"

##PRESET PASSWORD OF DATABASE
echo "utr-gis-db-01:5432:*:postgis:postgis" > ~/.pgpass
chmod 0600 ~/.pgpass

for max_wd in waterdiepterasters/*.tif; 
do
	v1="$(basename "$max_wd")"
	v1=$(basename "${max_wd%.*}")
	echo $v1
    echo $(date '+ %H:%M:%S') Begonnen met scenario $v1
	echo $max_wd
    gdal_calc.py -A "$max_wd" --outfile=result.tif --calc="(A>0.02)*1+(A<0.02)*-9999" --NoDataValue=-9999

    gdal_polygonize.py result.tif "$v1""_polygons".shp  -f "ESRI SHAPEFILE" OUTPUT DN
    ogr2ogr -overwrite -f "PostgreSQL" PG:"host=utr-gis-db-01 user=postgis dbname=x0143_stikstof password=postgis port=5432" -nln watervlakken "$v1""_polygons".shp -a_srs EPSG:28992 -lco GEOMETRY_NAME=geom 
	
    psql -h utr-gis-db-01 -p 5432 -U postgis -d x0143_stikstof -f "kwetsbare panden afleiden/combineer_watervlakken_panden.sql"
    
    ogr2ogr -f "ESRI Shapefile" panden_buffer_"$v1".shp PG:"host=utr-gis-db-01 user=postgis dbname=x0143_stikstof password=postgis port=5432" "tmp.pand_tot" -lco GEOMETRY_NAME=geom 
    zonal panden_buffer_"$v1".shp panden_stats_"$v1".shp -r "$max_wd" -s max median

    ogr2ogr -overwrite -f "PostgreSQL" PG:"host=utr-gis-db-01 user=postgis dbname=x0143_stikstof password=postgis port=5432" -nln panden_met_stats -nlt PROMOTE_TO_MULTI panden_stats_"$v1".shp -a_srs EPSG:28992 -lco GEOMETRY_NAME=geom 

    # **SQL CODE:opslaan_resultaten**
	
    psql -h utr-gis-db-01 -p 5432 -U postgis -d x0143_stikstof -c "update panden_met_stats set max=0 where max='Nan';"

    psql -h utr-gis-db-01 -p 5432 -U postgis -d x0143_stikstof -c "CREATE TABLE resultaten.$v1 AS select pand.identifica,pand.bouwjaar,pand.adres, pand.pand as geom,stats.area,stats.max,stats.median, CASE WHEN stats.max>0.15 and stats.area>200 THEN 'regionaal' WHEN stats.max>0.15 AND stats.area<200 THEN 'lokaal' ELSE 'geen knelpunt' END as knelpunt from tmp.pand_tot pand, panden_met_stats stats where stats.identifica=pand.identifica"
    
    rm *"$v1"*.{shp,shx,prj,dbf}
    rm result.tif

    echo $(date '+ %H:%M:%S') Klaar met scenario "$v1"
done

echo $(date '+ %H:%M:%S') "Klaar met berekeningen"