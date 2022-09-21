import urllib3

UPLOAD_TIMEOUT = urllib3.Timeout(connect=60, read=600)

THREEDI_API_HOST = "https://api.3di.live"
ORGANISATION_UUID = "7a1c4292ac0f44a6b788a1155bb23043"  #Waterschap Limburg
# ORGANISATION_UUID = '61f5a464c35044c19bc7d4b42d7f58cb' # Nelen & Schuurmans Consultancy
RADAR_ID = "d6c2347d-7bd1-4d9d-a1f6-b342c865516f"
SCHEMATISATIONS = [


#	 "Hekerbeek zonder drempel",
   #  "Hekerbeek drempel 5 cm",
     "Hekerbeek drempel 10 cm",
   #  "Hekerbeek drempel 30 cm",
    # "Hekerbeek drempel 20 cm",
   # 'Hekerbeek drempel 40 cm'
]


BUIEN = {
 'T10': [ #s,m/s
[0,5.612/(1000*24*60)],
[24*60,6.064/(1000*24*60)],
[48*60,14.168/(1000*24*60)],
[72*60,7.932/(1000*24*60)],
[96*60,4.224/(1000*24*60)],
[120*60,0]
],   

'T25': [ #s,m/s
[0,7.09896/(1000*24*60)],
[24*60,7.6224/(1000*24*60)],
[48*60,17.00328/(1000*24*60)],
[72*60,9.78264/(1000*24*60)],
[96*60,5.49288/(1000*24*60)],
[120*60,0]
],
    
'T100': [ #s,m/s
[0,9.219/(1000*24*60)],
[24*60,9.897/(1000*24*60)],
[48*60,22.050/(1000*24*60)],
[72*60,12.696/(1000*24*60)],
[96*60,7.138/(1000*24*60)],
[120*60,0]
]

}
