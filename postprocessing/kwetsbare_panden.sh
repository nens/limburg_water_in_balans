#############################################################
## SHAPEFILES
###############################################################
# echo $(date '+ %H:%M:%S') "Ik ben gestart :)"

##PRESET PASSWORD OF DATABASE
echo "utr-gis-db-01:5432:*:postgis:postgis" > ~/.pgpass
chmod 0600 ~/.pgpass

input="namen.txt"
input2="bui.txt"
input3="scenarios.txt"

while read -r line
do
   while read -r line2
   do
	   while read -r line3
	   do
			# **aanhalingstekens aan het begin en eind van een string weghalen (nodig om inputs met getallen en spaties mogelijk te maken)**
			line="${line%\"}"
			line="${line#\"}"
			line2="${line2%\"}"
			line2="${line2#\"}"
			line3="${line3%\"}"
			line3="${line3#\"}"
			echo path_raster="/mnt/workdir/R_vdZaag/Stikstof_limburg/x0143_stikstof/$line/$line2/$line3/Results"
			path_raster="/mnt/results/Projecten_X_2022/x0143_stikstof/$line/$line2/$line3/Results"
			path_gpkg="/mnt/workdir/R_vdZaag/Stikstof_limburg/x0143_stikstof/$line/$line2/$line3"
			echo "$path_raster"
			for input_raster in $path_raster/*max_depth.tif
			do
				naam=${line/-/_}
				naam_db=kw_${naam}_${line2}_${line3}
				
				echo "$input_raster"
				gdal_calc.py -A "$input_raster" --outfile=result.tif --calc="(A>0.02)*1+(A<0.02)*-9999" --NoDataValue=-9999

				gdal_polygonize.py result.tif "$naam_db""_polygons".shp  -f "ESRI SHAPEFILE" OUTPUT DN
				ogr2ogr -overwrite -f "PostgreSQL" PG:"host=utr-gis-db-01 user=postgis dbname=x0143_stikstof password=postgis port=5432" -nln watervlakken "$naam_db""_polygons".shp -a_srs EPSG:28992 -lco GEOMETRY_NAME=geom 
				
				psql -h utr-gis-db-01 -p 5432 -U postgis -d x0143_stikstof -c "DROP TABLE public.deelgebied;"
				psql -h utr-gis-db-01 -p 5432 -U postgis -d x0143_stikstof -c "CREATE TABLE public.deelgebied AS SELECT * FROM deelgebieden.$naam"
				psql -h utr-gis-db-01 -p 5432 -U postgis -d x0143_stikstof -f "kwetsbare panden afleiden/combineer_watervlakken_panden.sql"
				
				ogr2ogr -f "ESRI Shapefile" panden_buffer_"$naam_db".shp PG:"host=utr-gis-db-01 user=postgis dbname=x0143_stikstof password=postgis port=5432" "tmp.pand_tot" -lco GEOMETRY_NAME=geom 
				zonal panden_buffer_"$naam_db".shp panden_stats_"$naam_db".shp -r "$input_raster" -s max median

				ogr2ogr -overwrite -f "PostgreSQL" PG:"host=utr-gis-db-01 user=postgis dbname=x0143_stikstof password=postgis port=5432" -nln panden_met_stats -nlt PROMOTE_TO_MULTI panden_stats_"$naam_db".shp -a_srs EPSG:28992 -lco GEOMETRY_NAME=geom 

				# **SQL CODE:opslaan_resultaten**
				
				psql -h utr-gis-db-01 -p 5432 -U postgis -d x0143_stikstof -c "update panden_met_stats set max=0 where max='Nan';"

				psql -h utr-gis-db-01 -p 5432 -U postgis -d x0143_stikstof -c "CREATE TABLE resultaten.$naam_db AS select pand.identifica,pand.bouwjaar,pand.adres, pand.pand as geom,stats.area,stats.max,stats.median, CASE WHEN stats.max>0.15 and stats.area>200 THEN 'regionaal' WHEN stats.max>0.15 AND stats.area<200 THEN 'lokaal' ELSE 'geen knelpunt' END as knelpunt from tmp.pand_tot pand, panden_met_stats stats where stats.identifica=pand.identifica"
				
				psql -h utr-gis-db-01 -p 5432 -U postgis -d x0143_stikstof -c "ALTER TABLE resultaten.$naam_db ADD COLUMN oppervlakte float"
				psql -h utr-gis-db-01 -p 5432 -U postgis -d x0143_stikstof -c "ALTER TABLE resultaten.$naam_db ADD COLUMN kosten float"
				psql -h utr-gis-db-01 -p 5432 -U postgis -d x0143_stikstof -c "UPDATE resultaten.$naam_db SET oppervlakte = ST_Area(geom) WHERE adres = 1"
				psql -h utr-gis-db-01 -p 5432 -U postgis -d x0143_stikstof -c "UPDATE resultaten.$naam_db SET kosten = 300 * oppervlakte"
				psql -h utr-gis-db-01 -p 5432 -U postgis -d x0143_stikstof -c "UPDATE resultaten.$naam_db SET kosten = NULL WHERE knelpunt = 'geen knelpunt'"
				
				# **Resultaten opslaan in de juiste map**
				rm -f $path_gpkg/$naam_db.gpkg
				ogr2ogr -f GPKG $path_gpkg/$naam_db.gpkg -nln "Risico op wateroverlast per pand" PG:"host=utr-gis-db-01 user=postgis dbname=x0143_stikstof password=postgis" -sql "SELECT * FROM resultaten.$naam_db"
				cp -r $path_gpkg/$naam_db.gpkg $path_raster/$naam_db.gpkg
				rm *.{shp,shx,prj,dbf}
				rm result.tif

				echo $(date '+ %H:%M:%S') Klaar met scenario "$naam_db"
			done
	   done < "$input3"
   done < "$input2"
done < "$input"

echo $(date '+ %H:%M:%S') "Klaar met batch"