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
			#aanhalingstekens verwijderderen aan begin en eind van string (spaties en getallen hierdoor mogelijk)
			line="${line%\"}"
			line="${line#\"}"
			line2="${line2%\"}"
			line2="${line2#\"}"
			line3="${line3%\"}"
			line3="${line3#\"}"
			
			#Kopieer orginele raster en verander de naam. Pas vervolgens van het orginele raster de extent aan (infiltration.tif)
			path_raster="/mnt/results/Projecten_X_2022/x0143_stikstof/$line/$line2/$line3/schematisation/rasters"
			infiltration_raster=$path_raster/infiltration.tif
			echo $infiltration_raster
			mv $infiltration_raster $path_raster/infiltration_old.tif
			bash Extent_aanpassen/extent_aanpassen.sh $path_raster/dem.tif $path_raster/infiltration_old.tif 0 $path_raster/infiltration.tif
	   done < "$input3"
   done < "$input2"
done < "$input"

echo $(date '+ %H:%M:%S') "Klaar met batch"