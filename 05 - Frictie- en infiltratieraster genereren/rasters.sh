<<<<<<< Updated upstream

echo $(date '+ %H:%M:%S') "Ik ben gestart :)" $1
if [ -n "$1" ];
then
	echo "rasters worden ook" $1 "doorgerekend"
else 
	echo "rasters worden niet hybride doorgerekend"
fi

echo "FRICTION: gedownload via de citybuilder"
	gdal_calc.py -A "/mnt/workdir/A_Feenstra/X0143 - Stikstof Limburg/Geul Midden T25/schematisation/rasters/landgebruik.tif" --NoDataValue -9999 --outfile=output/frictie/frictie.tif --calc="(A==1)*0.013+(A==2)*0.034+(A==3)*0.020+(A==4)*0.029+(A==5)*0.013+(A==6)*0.020+(A==7)*0.020+(A==8)*0.058+(A==9)*0.058+(A==10)*0.058+(A==11)*0.058+(A==12)*0.058+(A==13)*0.058+(A==14)*0.058+(A==15)*0.034+(A==16)*0.058+(A==17)*0.034+(A==18)*0.058+(A==19)*0.058+(A==20)*0.058+(A==21)*0.058+(A==22)*0.058+(A==23)*0.034+(A==26)*0.058+(A==27)*0.058+(A==28)*0.058+(A==29)*0.026+(A==30)*0.058+(A==254)*0.026+(A==253)*0.058)" --co COMPRESS=DEFLATE 

# echo "TIP! pas eerst de extent van je hellingsklasse aan naar je dem"		
# echo "Start met maken infiltratieraster T25"	
#     gdal_calc.py -A input/hellingsklasse/*.tif -B input/landgebruik/*.tif --NoDataValue -9999 --outfile=output/infiltratie/infiltratie_T25.tif --calc="(A==1)*(B==1)*0+(A==2)*(B==1)*0+(A==3)*(B==1)*0+(A==4)*(B==1)*0+(A==1)*(B==2)*460+(A==2)*(B==2)*400+(A==3)*(B==2)*390+(A==4)*(B==2)*225+(A==1)*(B==3)*74+(A==2)*(B==3)*78+(A==3)*(B==3)*74+(A==4)*(B==3)*60+(A==1)*(B==4)*245+(A==2)*(B==4)*260+(A==3)*(B==4)*248+(A==4)*(B==4)*200+(A==1)*(B==5)*0+(A==2)*(B==5)*0+(A==3)*(B==5)*0+(A==4)*(B==5)*0+(A==1)*(B==6)*74+(A==2)*(B==6)*78+(A==3)*(B==6)*74+(A==4)*(B==6)*60+(A==1)*(B==7)*74+(A==2)*(B==7)*78+(A==3)*(B==7)*74+(A==4)*(B==7)*60+(A==1)*(B==8)*490+(A==2)*(B==8)*520+(A==3)*(B==8)*495+(A==4)*(B==8)*400+(A==1)*(B==9)*490+(A==2)*(B==9)*520+(A==3)*(B==9)*520+(A==4)*(B==9)*440+(A==1)*(B==10)*490+(A==2)*(B==10)*520+(A==3)*(B==10)*495+(A==4)*(B==10)*400+(A==1)*(B==11)*490+(A==2)*(B==11)*520+(A==3)*(B==11)*495+(A==4)*(B==11)*400+(A==1)*(B==12)*490+(A==2)*(B==12)*520+(A==3)*(B==12)*495+(A==4)*(B==12)*400+(A==1)*(B==13)*490+(A==2)*(B==13)*520+(A==3)*(B==13)*520+(A==4)*(B==13)*440+(A==1)*(B==14)*490+(A==2)*(B==14)*520+(A==3)*(B==14)*495+(A==4)*(B==14)*400+(A==1)*(B==15)*460+(A==2)*(B==15)*400+(A==3)*(B==15)*390+(A==4)*(B==15)*225+(A==1)*(B==16)*490+(A==2)*(B==16)*520+(A==3)*(B==16)*495+(A==4)*(B==16)*400+(A==1)*(B==17)*460+(A==2)*(B==17)*400+(A==3)*(B==17)*390+(A==4)*(B==17)*225+(A==1)*(B==18)*490+(A==2)*(B==18)*520+(A==3)*(B==18)*520+(A==4)*(B==18)*440+(A==1)*(B==19)*490+(A==2)*(B==19)*520+(A==3)*(B==19)*520+(A==4)*(B==19)*440+(A==1)*(B==20)*490+(A==2)*(B==20)*520+(A==3)*(B==20)*495+(A==4)*(B==20)*400+(A==1)*(B==21)*490+(A==2)*(B==21)*520+(A==3)*(B==21)*495+(A==4)*(B==21)*400+(A==1)*(B==22)*490+(A==2)*(B==22)*520+(A==3)*(B==22)*520+(A==4)*(B==22)*440+(A==1)*(B==23)*460+(A==2)*(B==23)*400+(A==3)*(B==23)*390+(A==4)*(B==23)*225+(A==1)*(B==26)*490+(A==2)*(B==26)*520+(A==3)*(B==26)*495+(A==4)*(B==26)*400+(A==1)*(B==27)*490+(A==2)*(B==27)*520+(A==3)*(B==27)*495+(A==4)*(B==27)*400+(A==1)*(B==28)*490+(A==2)*(B==28)*520+(A==3)*(B==28)*495+(A==4)*(B==28)*400+(A==1)*(B==29)*0+(A==2)*(B==29)*0+(A==3)*(B==29)*0+(A==4)*(B==29)*0+(A==1)*(B==30)*490+(A==2)*(B==30)*520+(A==3)*(B==30)*495+(A==4)*(B==30)*400+(A==1)*(B==254)*0+(A==2)*(B==254)*0+(A==3)*(B==254)*0+(A==4)*(B==254)*0+(A==1)*(B==253)*490+(A==2)*(B==253)*520+(A==3)*(B==253)*495+(A==4)*(B==253)*400" --co COMPRESS=DEFLATE 
    
	
# echo "Start met maken infiltratieraster T100"	
#     gdal_calc.py -A input/hellingsklasse/*.tif -B input/landgebruik/*.tif --NoDataValue -9999 --outfile=output/infiltratie/infiltratie_T100.tif --calc="(A==1)*(B==1)*0+(A==2)*(B==1)*0+(A==3)*(B==1)*0+(A==4)*(B==1)*0+(A==1)*(B==2)*395+(A==2)*(B==2)*330+(A==3)*(B==2)*320+(A==4)*(B==2)*130+(A==1)*(B==3)*64+(A==2)*(B==3)*65+(A==3)*(B==3)*63+(A==4)*(B==3)*51+(A==1)*(B==4)*213+(A==2)*(B==4)*218+(A==3)*(B==4)*210+(A==4)*(B==4)*170+(A==1)*(B==5)*0+(A==2)*(B==5)*0+(A==3)*(B==5)*0+(A==4)*(B==5)*0+(A==1)*(B==6)*64+(A==2)*(B==6)*65+(A==3)*(B==6)*63+(A==4)*(B==6)*51+(A==1)*(B==7)*64+(A==2)*(B==7)*65+(A==3)*(B==7)*63+(A==4)*(B==7)*51+(A==1)*(B==8)*425+(A==2)*(B==8)*435+(A==3)*(B==8)*420+(A==4)*(B==8)*340+(A==1)*(B==9)*425+(A==2)*(B==9)*435+(A==3)*(B==9)*430+(A==4)*(B==9)*380+(A==1)*(B==10)*425+(A==2)*(B==10)*435+(A==3)*(B==10)*420+(A==4)*(B==10)*340+(A==1)*(B==11)*425+(A==2)*(B==11)*435+(A==3)*(B==11)*420+(A==4)*(B==11)*340+(A==1)*(B==12)*425+(A==2)*(B==12)*435+(A==3)*(B==12)*420+(A==4)*(B==12)*340+(A==1)*(B==13)*425+(A==2)*(B==13)*435+(A==3)*(B==13)*430+(A==4)*(B==13)*380+(A==1)*(B==14)*425+(A==2)*(B==14)*435+(A==3)*(B==14)*420+(A==4)*(B==14)*340+(A==1)*(B==15)*395+(A==2)*(B==15)*330+(A==3)*(B==15)*320+(A==4)*(B==15)*130+(A==1)*(B==16)*425+(A==2)*(B==16)*435+(A==3)*(B==16)*420+(A==4)*(B==16)*340+(A==1)*(B==17)*395+(A==2)*(B==17)*330+(A==3)*(B==17)*320+(A==4)*(B==17)*130+(A==1)*(B==18)*425+(A==2)*(B==18)*435+(A==3)*(B==18)*430+(A==4)*(B==18)*380+(A==1)*(B==19)*425+(A==2)*(B==19)*435+(A==3)*(B==19)*430+(A==4)*(B==19)*380+(A==1)*(B==20)*425+(A==2)*(B==20)*435+(A==3)*(B==20)*420+(A==4)*(B==20)*340+(A==1)*(B==21)*425+(A==2)*(B==21)*435+(A==3)*(B==21)*420+(A==4)*(B==21)*340+(A==1)*(B==22)*425+(A==2)*(B==22)*435+(A==3)*(B==22)*430+(A==4)*(B==22)*380+(A==1)*(B==23)*395+(A==2)*(B==23)*330+(A==3)*(B==23)*320+(A==4)*(B==23)*130+(A==1)*(B==26)*425+(A==2)*(B==26)*435+(A==3)*(B==26)*420+(A==4)*(B==26)*340+(A==1)*(B==27)*425+(A==2)*(B==27)*435+(A==3)*(B==27)*420+(A==4)*(B==27)*340+(A==1)*(B==28)*425+(A==2)*(B==28)*435+(A==3)*(B==28)*420+(A==4)*(B==28)*340+(A==1)*(B==29)*0+(A==2)*(B==29)*0+(A==3)*(B==29)*0+(A==4)*(B==29)*0+(A==1)*(B==30)*425+(A==2)*(B==30)*435+(A==3)*(B==30)*420+(A==4)*(B==30)*340+(A==1)*(B==254)*0+(A==2)*(B==254)*0+(A==3)*(B==254)*0+(A==4)*(B==254)*0+(A==1)*(B==253)*425+(A==2)*(B==253)*435+(A==3)*(B==253)*420+(A==4)*(B==253)*340" --co COMPRESS=DEFLATE

# echo "Start met maken max infiltratie"	
# 	gdal_calc.py -A output/infiltratie/infiltratie_T100.tif --calc="(A>-1)*0.120" --co COMPRESS=DEFLATE --NoDataValue -9999 --outfile=output/infiltratie/max_infiltratie.tif 
# echo "Start met maken van ini waterlevel"
# 	gdal_calc.py -A output/ini_WL/max_infiltration_meerssen_hybride.tif --calc="(A>0)*-10" --co COMPRESS=DEFLATE --NoDataValue -9999 --outfile=output/ini_WL/ini_waterlevel_meerssen_hybride.tif 


# #hybride
# if [ -n "$1" ];
# then
# 	echo "start met hybride rasters maken"
# 	cp input/dem/dem.tif output/dem/dem_hybride.tif
# 	cp output/frictie/friction.tif output/frictie/friction_hybride.tif
# 	cp output/infiltratie/infiltratie_T25.tif output/infiltratie/infiltratie_T25_hybride.tif
# 	cp output/infiltratie/infiltratie_T100.tif output/infiltratie/infiltratie_T100_hybride.tif
# 	cp output/infiltratie/max_infiltratie.tif output/infiltratie/max_infiltratie_hybride.tif
# 	#shapes burnen in achtergrondraster:
# 	gdalwarp -dstnodata -9999 output/dem/dem_hybride.tif output/dem/dem_hybride_nan.tif
	
# 	gdal_rasterize -burn -9999 -l meersen_panden input/panden/meersen_panden.shp output/dem/dem_hybride_nan.tif
# 	gdal_rasterize -burn -9999 -l meersen_panden input/panden/meersen_panden.shp output/frictie/friction_hybride.tif
# 	gdal_rasterize -burn -9999 -l meersen_panden input/panden/meersen_panden.shp output/infiltratie/infiltratie_T25_hybride.tif
# 	gdal_rasterize -burn -9999 -l meersen_panden input/panden/meersen_panden.shp output/infiltratie/infiltratie_T100_hybride.tif
# 	gdal_rasterize -burn -9999 -l meersen_panden input/panden/meersen_panden.shp output/infiltratie/max_infiltratie_hybride.tif 
# 	gdal_rasterize -burn 48 -l watergang input/watergang/watergang.shp output/ini_WL/ini_waterlevel_meerssen_hybride.tif
# 	gdal_rasterize -burn -9999 -l meersen_panden input/panden/meersen_panden.shp output/ini_WL/ini_waterlevel_meerssen_hybride.tif
	
# 	gdal_translate -co 'COMPRESS=DEFLATE' output/dem/dem_hybride_nan.tif output/dem/dem_hybride_nan_co.tif
# 	gdal_translate -co 'COMPRESS=DEFLATE' output/frictie/friction_hybride.tif output/frictie/friction_hybride_co.tif
# 	gdal_translate -co 'COMPRESS=DEFLATE' output/infiltratie/infiltratie_T25_hybride.tif output/infiltratie/infiltratie_T25_hybride_co.tif
# 	gdal_translate -co 'COMPRESS=DEFLATE' output/infiltratie/infiltratie_T100_hybride.tif output/infiltratie/infiltratie_T100_hybride_co.tif
# 	gdal_translate -co 'COMPRESS=DEFLATE' output/infiltratie/max_infiltratie_hybride.tif output/infiltratie/max_infiltratie_hybride_co.tif 
# 	gdal_translate -co 'COMPRESS=DEFLATE' output/ini_WL/ini_waterlevel_meerssen_hybride.tif output/ini_WL/ini_waterlevel_meerssen_hybride_co.tif
	
# 	echo "KLAAR!"
# else
# 	gdal_translate -co 'COMPRESS=DEFLATE' output/dem/dem_nan.tif output/dem/dem_nan_co.tif
# 	gdal_translate -co 'COMPRESS=DEFLATE' output/frictie/friction_hybride.tif output/frictie/friction_co.tif
# 	gdal_translate -co 'COMPRESS=DEFLATE' output/infiltratie/infiltratie_T25_hybride.tif output/infiltratie/infiltratie_T25_co.tif
# 	gdal_translate -co 'COMPRESS=DEFLATE' output/infiltratie/infiltratie_T100_hybride.tif output/infiltratie/infiltratie_T100_co.tif
# 	gdal_translate -co 'COMPRESS=DEFLATE' output/infiltratie/max_infiltratie_hybride.tif output/infiltratie/max_infiltratie_co.tif 
# 	gdal_translate -co 'COMPRESS=DEFLATE' output/ini_WL/ini_waterlevel_meerssen_hybride.tif output/ini_WL/ini_waterlevel_meerssen_co.tif
# 	echo "KLAAR! voor hybride rasters run: bash rasters.sh hybride"
# fi	





=======

echo $(date '+ %H:%M:%S') "Ik ben gestart :)" $1
if [ -n "$1" ];
then
	echo "rasters worden ook" $1 "doorgerekend"
else 
	echo "rasters worden niet hybride doorgerekend"
fi

echo "FRICTION: gedownload via de citybuilder"
	gdal_calc.py -A "/mnt/workdir/A_Feenstra/X0143 - Stikstof Limburg/Geul Midden T25/schematisation/rasters/landgebruik.tif" --NoDataValue -9999 --outfile=output/frictie/frictie.tif --calc="(A==1)*0.013+(A==2)*0.034+(A==3)*0.020+(A==4)*0.029+(A==5)*0.013+(A==6)*0.020+(A==7)*0.020+(A==8)*0.058+(A==9)*0.058+(A==10)*0.058+(A==11)*0.058+(A==12)*0.058+(A==13)*0.058+(A==14)*0.058+(A==15)*0.034+(A==16)*0.058+(A==17)*0.034+(A==18)*0.058+(A==19)*0.058+(A==20)*0.058+(A==21)*0.058+(A==22)*0.058+(A==23)*0.034+(A==26)*0.058+(A==27)*0.058+(A==28)*0.058+(A==29)*0.026+(A==30)*0.058+(A==254)*0.026+(A==253)*0.058)" --co COMPRESS=DEFLATE 

# echo "TIP! pas eerst de extent van je hellingsklasse aan naar je dem"		
# echo "Start met maken infiltratieraster T25"	
#     gdal_calc.py -A input/hellingsklasse/*.tif -B input/landgebruik/*.tif --NoDataValue -9999 --outfile=output/infiltratie/infiltratie_T25.tif --calc="(A==1)*(B==1)*0+(A==2)*(B==1)*0+(A==3)*(B==1)*0+(A==4)*(B==1)*0+(A==1)*(B==2)*460+(A==2)*(B==2)*400+(A==3)*(B==2)*390+(A==4)*(B==2)*225+(A==1)*(B==3)*74+(A==2)*(B==3)*78+(A==3)*(B==3)*74+(A==4)*(B==3)*60+(A==1)*(B==4)*245+(A==2)*(B==4)*260+(A==3)*(B==4)*248+(A==4)*(B==4)*200+(A==1)*(B==5)*0+(A==2)*(B==5)*0+(A==3)*(B==5)*0+(A==4)*(B==5)*0+(A==1)*(B==6)*74+(A==2)*(B==6)*78+(A==3)*(B==6)*74+(A==4)*(B==6)*60+(A==1)*(B==7)*74+(A==2)*(B==7)*78+(A==3)*(B==7)*74+(A==4)*(B==7)*60+(A==1)*(B==8)*490+(A==2)*(B==8)*520+(A==3)*(B==8)*495+(A==4)*(B==8)*400+(A==1)*(B==9)*490+(A==2)*(B==9)*520+(A==3)*(B==9)*520+(A==4)*(B==9)*440+(A==1)*(B==10)*490+(A==2)*(B==10)*520+(A==3)*(B==10)*495+(A==4)*(B==10)*400+(A==1)*(B==11)*490+(A==2)*(B==11)*520+(A==3)*(B==11)*495+(A==4)*(B==11)*400+(A==1)*(B==12)*490+(A==2)*(B==12)*520+(A==3)*(B==12)*495+(A==4)*(B==12)*400+(A==1)*(B==13)*490+(A==2)*(B==13)*520+(A==3)*(B==13)*520+(A==4)*(B==13)*440+(A==1)*(B==14)*490+(A==2)*(B==14)*520+(A==3)*(B==14)*495+(A==4)*(B==14)*400+(A==1)*(B==15)*460+(A==2)*(B==15)*400+(A==3)*(B==15)*390+(A==4)*(B==15)*225+(A==1)*(B==16)*490+(A==2)*(B==16)*520+(A==3)*(B==16)*495+(A==4)*(B==16)*400+(A==1)*(B==17)*460+(A==2)*(B==17)*400+(A==3)*(B==17)*390+(A==4)*(B==17)*225+(A==1)*(B==18)*490+(A==2)*(B==18)*520+(A==3)*(B==18)*520+(A==4)*(B==18)*440+(A==1)*(B==19)*490+(A==2)*(B==19)*520+(A==3)*(B==19)*520+(A==4)*(B==19)*440+(A==1)*(B==20)*490+(A==2)*(B==20)*520+(A==3)*(B==20)*495+(A==4)*(B==20)*400+(A==1)*(B==21)*490+(A==2)*(B==21)*520+(A==3)*(B==21)*495+(A==4)*(B==21)*400+(A==1)*(B==22)*490+(A==2)*(B==22)*520+(A==3)*(B==22)*520+(A==4)*(B==22)*440+(A==1)*(B==23)*460+(A==2)*(B==23)*400+(A==3)*(B==23)*390+(A==4)*(B==23)*225+(A==1)*(B==26)*490+(A==2)*(B==26)*520+(A==3)*(B==26)*495+(A==4)*(B==26)*400+(A==1)*(B==27)*490+(A==2)*(B==27)*520+(A==3)*(B==27)*495+(A==4)*(B==27)*400+(A==1)*(B==28)*490+(A==2)*(B==28)*520+(A==3)*(B==28)*495+(A==4)*(B==28)*400+(A==1)*(B==29)*0+(A==2)*(B==29)*0+(A==3)*(B==29)*0+(A==4)*(B==29)*0+(A==1)*(B==30)*490+(A==2)*(B==30)*520+(A==3)*(B==30)*495+(A==4)*(B==30)*400+(A==1)*(B==254)*0+(A==2)*(B==254)*0+(A==3)*(B==254)*0+(A==4)*(B==254)*0+(A==1)*(B==253)*490+(A==2)*(B==253)*520+(A==3)*(B==253)*495+(A==4)*(B==253)*400" --co COMPRESS=DEFLATE 
    
	
# echo "Start met maken infiltratieraster T100"	
#     gdal_calc.py -A input/hellingsklasse/*.tif -B input/landgebruik/*.tif --NoDataValue -9999 --outfile=output/infiltratie/infiltratie_T100.tif --calc="(A==1)*(B==1)*0+(A==2)*(B==1)*0+(A==3)*(B==1)*0+(A==4)*(B==1)*0+(A==1)*(B==2)*395+(A==2)*(B==2)*330+(A==3)*(B==2)*320+(A==4)*(B==2)*130+(A==1)*(B==3)*64+(A==2)*(B==3)*65+(A==3)*(B==3)*63+(A==4)*(B==3)*51+(A==1)*(B==4)*213+(A==2)*(B==4)*218+(A==3)*(B==4)*210+(A==4)*(B==4)*170+(A==1)*(B==5)*0+(A==2)*(B==5)*0+(A==3)*(B==5)*0+(A==4)*(B==5)*0+(A==1)*(B==6)*64+(A==2)*(B==6)*65+(A==3)*(B==6)*63+(A==4)*(B==6)*51+(A==1)*(B==7)*64+(A==2)*(B==7)*65+(A==3)*(B==7)*63+(A==4)*(B==7)*51+(A==1)*(B==8)*425+(A==2)*(B==8)*435+(A==3)*(B==8)*420+(A==4)*(B==8)*340+(A==1)*(B==9)*425+(A==2)*(B==9)*435+(A==3)*(B==9)*430+(A==4)*(B==9)*380+(A==1)*(B==10)*425+(A==2)*(B==10)*435+(A==3)*(B==10)*420+(A==4)*(B==10)*340+(A==1)*(B==11)*425+(A==2)*(B==11)*435+(A==3)*(B==11)*420+(A==4)*(B==11)*340+(A==1)*(B==12)*425+(A==2)*(B==12)*435+(A==3)*(B==12)*420+(A==4)*(B==12)*340+(A==1)*(B==13)*425+(A==2)*(B==13)*435+(A==3)*(B==13)*430+(A==4)*(B==13)*380+(A==1)*(B==14)*425+(A==2)*(B==14)*435+(A==3)*(B==14)*420+(A==4)*(B==14)*340+(A==1)*(B==15)*395+(A==2)*(B==15)*330+(A==3)*(B==15)*320+(A==4)*(B==15)*130+(A==1)*(B==16)*425+(A==2)*(B==16)*435+(A==3)*(B==16)*420+(A==4)*(B==16)*340+(A==1)*(B==17)*395+(A==2)*(B==17)*330+(A==3)*(B==17)*320+(A==4)*(B==17)*130+(A==1)*(B==18)*425+(A==2)*(B==18)*435+(A==3)*(B==18)*430+(A==4)*(B==18)*380+(A==1)*(B==19)*425+(A==2)*(B==19)*435+(A==3)*(B==19)*430+(A==4)*(B==19)*380+(A==1)*(B==20)*425+(A==2)*(B==20)*435+(A==3)*(B==20)*420+(A==4)*(B==20)*340+(A==1)*(B==21)*425+(A==2)*(B==21)*435+(A==3)*(B==21)*420+(A==4)*(B==21)*340+(A==1)*(B==22)*425+(A==2)*(B==22)*435+(A==3)*(B==22)*430+(A==4)*(B==22)*380+(A==1)*(B==23)*395+(A==2)*(B==23)*330+(A==3)*(B==23)*320+(A==4)*(B==23)*130+(A==1)*(B==26)*425+(A==2)*(B==26)*435+(A==3)*(B==26)*420+(A==4)*(B==26)*340+(A==1)*(B==27)*425+(A==2)*(B==27)*435+(A==3)*(B==27)*420+(A==4)*(B==27)*340+(A==1)*(B==28)*425+(A==2)*(B==28)*435+(A==3)*(B==28)*420+(A==4)*(B==28)*340+(A==1)*(B==29)*0+(A==2)*(B==29)*0+(A==3)*(B==29)*0+(A==4)*(B==29)*0+(A==1)*(B==30)*425+(A==2)*(B==30)*435+(A==3)*(B==30)*420+(A==4)*(B==30)*340+(A==1)*(B==254)*0+(A==2)*(B==254)*0+(A==3)*(B==254)*0+(A==4)*(B==254)*0+(A==1)*(B==253)*425+(A==2)*(B==253)*435+(A==3)*(B==253)*420+(A==4)*(B==253)*340" --co COMPRESS=DEFLATE

# echo "Start met maken max infiltratie"	
# 	gdal_calc.py -A output/infiltratie/infiltratie_T100.tif --calc="(A>-1)*0.120" --co COMPRESS=DEFLATE --NoDataValue -9999 --outfile=output/infiltratie/max_infiltratie.tif 
# echo "Start met maken van ini waterlevel"
# 	gdal_calc.py -A output/ini_WL/max_infiltration_meerssen_hybride.tif --calc="(A>0)*-10" --co COMPRESS=DEFLATE --NoDataValue -9999 --outfile=output/ini_WL/ini_waterlevel_meerssen_hybride.tif 


# #hybride
# if [ -n "$1" ];
# then
# 	echo "start met hybride rasters maken"
# 	cp input/dem/dem.tif output/dem/dem_hybride.tif
# 	cp output/frictie/friction.tif output/frictie/friction_hybride.tif
# 	cp output/infiltratie/infiltratie_T25.tif output/infiltratie/infiltratie_T25_hybride.tif
# 	cp output/infiltratie/infiltratie_T100.tif output/infiltratie/infiltratie_T100_hybride.tif
# 	cp output/infiltratie/max_infiltratie.tif output/infiltratie/max_infiltratie_hybride.tif
# 	#shapes burnen in achtergrondraster:
# 	gdalwarp -dstnodata -9999 output/dem/dem_hybride.tif output/dem/dem_hybride_nan.tif
	
# 	gdal_rasterize -burn -9999 -l meersen_panden input/panden/meersen_panden.shp output/dem/dem_hybride_nan.tif
# 	gdal_rasterize -burn -9999 -l meersen_panden input/panden/meersen_panden.shp output/frictie/friction_hybride.tif
# 	gdal_rasterize -burn -9999 -l meersen_panden input/panden/meersen_panden.shp output/infiltratie/infiltratie_T25_hybride.tif
# 	gdal_rasterize -burn -9999 -l meersen_panden input/panden/meersen_panden.shp output/infiltratie/infiltratie_T100_hybride.tif
# 	gdal_rasterize -burn -9999 -l meersen_panden input/panden/meersen_panden.shp output/infiltratie/max_infiltratie_hybride.tif 
# 	gdal_rasterize -burn 48 -l watergang input/watergang/watergang.shp output/ini_WL/ini_waterlevel_meerssen_hybride.tif
# 	gdal_rasterize -burn -9999 -l meersen_panden input/panden/meersen_panden.shp output/ini_WL/ini_waterlevel_meerssen_hybride.tif
	
# 	gdal_translate -co 'COMPRESS=DEFLATE' output/dem/dem_hybride_nan.tif output/dem/dem_hybride_nan_co.tif
# 	gdal_translate -co 'COMPRESS=DEFLATE' output/frictie/friction_hybride.tif output/frictie/friction_hybride_co.tif
# 	gdal_translate -co 'COMPRESS=DEFLATE' output/infiltratie/infiltratie_T25_hybride.tif output/infiltratie/infiltratie_T25_hybride_co.tif
# 	gdal_translate -co 'COMPRESS=DEFLATE' output/infiltratie/infiltratie_T100_hybride.tif output/infiltratie/infiltratie_T100_hybride_co.tif
# 	gdal_translate -co 'COMPRESS=DEFLATE' output/infiltratie/max_infiltratie_hybride.tif output/infiltratie/max_infiltratie_hybride_co.tif 
# 	gdal_translate -co 'COMPRESS=DEFLATE' output/ini_WL/ini_waterlevel_meerssen_hybride.tif output/ini_WL/ini_waterlevel_meerssen_hybride_co.tif
	
# 	echo "KLAAR!"
# else
# 	gdal_translate -co 'COMPRESS=DEFLATE' output/dem/dem_nan.tif output/dem/dem_nan_co.tif
# 	gdal_translate -co 'COMPRESS=DEFLATE' output/frictie/friction_hybride.tif output/frictie/friction_co.tif
# 	gdal_translate -co 'COMPRESS=DEFLATE' output/infiltratie/infiltratie_T25_hybride.tif output/infiltratie/infiltratie_T25_co.tif
# 	gdal_translate -co 'COMPRESS=DEFLATE' output/infiltratie/infiltratie_T100_hybride.tif output/infiltratie/infiltratie_T100_co.tif
# 	gdal_translate -co 'COMPRESS=DEFLATE' output/infiltratie/max_infiltratie_hybride.tif output/infiltratie/max_infiltratie_co.tif 
# 	gdal_translate -co 'COMPRESS=DEFLATE' output/ini_WL/ini_waterlevel_meerssen_hybride.tif output/ini_WL/ini_waterlevel_meerssen_co.tif
# 	echo "KLAAR! voor hybride rasters run: bash rasters.sh hybride"
# fi	





>>>>>>> Stashed changes
