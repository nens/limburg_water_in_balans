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
    echo $(date '+ %H:%M:%S') Begonnen met deelgebied $v1
	
	echo $v1
    ogr2ogr -f "ESRI Shapefile" resultaten/$v1.shp PG:"host=utr-gis-db-01 user=postgis dbname=w0154_hekerbeekdal password=postgis" -sql "SELECT * FROM resultaten.$v1"
  
  echo $(date '+ %H:%M:%S') Klaar met deelgebied $v1
	
done < panden_res.txt

echo $(date '+ %H:%M:%S') "Klaar met batch"