input="namen2.txt" #textbestand met de namen van de deelgebieden
######################################
# $IFS removed to allow the trimming # 
#####################################
while read -r line
do
  echo $line
  ogr2ogr -clipsrc $line/T25/Basis/schematisation/bounding_box/bounding_box.shp $line/T25/Basis/schematisation/bounding_box/panden.shp /mnt/workdir/R_vdZaag/Stikstof_limburg/Limburg_panden/Limburg_panden.shp #De panden van Limburg worden geclipt
done < "$input"