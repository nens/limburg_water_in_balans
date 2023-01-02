input="namen.txt"
input2="bui.txt"
input3="scenarios.txt"
######################################
# $IFS removed to allow the trimming # 
#####################################
while read -r line
do
   echo $line
   while read -r line2
   do
	   while read -r line3
	   do
		  #aanhalingstekens aan het begin en eind van de strings verwijderen (maakt getallen en spaties mogelijk)
		  line="${line%\"}"
          line="${line#\"}"
		  line2="${line2%\"}"
          line2="${line2#\"}"
		  line3="${line3%\"}"
          line3="${line3#\"}"
		  
		  #Padverwijzingen
          input_raster="/mnt/results/Projecten_X_2022/x0143_stikstof/$line/$line2/$line3/schematisation/rasters/landgebruik_origineel.tif"
          input_shape="/mnt/workdir/R_vdZaag/Stikstof_limburg/Grasland_polygonen/$line3.shp"
          output_raster="/mnt/results/Projecten_X_2022/x0143_stikstof/$line/$line2/$line3/schematisation/rasters/landgebruik.tif"
		  
		  #python script aanroepen
          python3 achtergrond_script_landgebruik_aanpassen.py $input_raster $output_raster $input_shape
          echo "done with $line $line2 $line3"  
	   done < "$input3"
   done < "$input2"
done < "$input"

echo "
Script uitgevoerd.
Script gemaakt door Ruben van der Zaag, Nelen & Schuurmans, oktober 2022"