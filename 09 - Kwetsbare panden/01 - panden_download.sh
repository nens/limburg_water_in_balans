## Alle panden voor Limburg extracten:
gdalsrsinfo epsg:28992 -o wkt > /mnt/workdir/R_vdZaag/Stikstof_limburg/Limburg_shape.prj
vselect -a "gid" -u landuse_ro -s utr-landuse-db-01.nens.local bag_2022 bagactueel.pandactueelbestaand /mnt/workdir/R_vdZaag/Stikstof_limburg/Limburg_shape.shp /mnt/workdir/R_vdZaag/Stikstof_limburg/Limburg_panden
## Password = IzGxyGqpUGNR2OWnrz6N