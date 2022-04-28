# Water in Balans (Waterschap Limburg)
Scripts en tooling voor het modelaanpassingen, simulaties en naverwerking voor de Water in Balans projecten voor Waterschap Limburg 


## 1. Simulaties draaien
Voor het draaien van simulaties dient de constants.py script aangepast te worden. Hierin is een dictionary SCHEMATISATIONS waarin de schematisaties kunnen worden opgenomen waar de simulaties voor gedraaid moeten worden. In dit bestand zijn ook de buien T10, T25 en T100 opgenomen wat gehanteerd wordt bij Waterschap Limburg. 

Om de simulaties aan te slingeren kan de limburg.py gedraaid worden.
In het mapje zit ook een login.py. Deze wordt ingeladen in de limburg.py en hoeft dus niet geopend te worden verder. Wel moet in de login_details.ini de juiste credentials opgegeven worden. 

## 2. Resultaten downloaden
Als de simulaties zijn afgerond kunnen de ruwe resultaten en de geinterpoleerde snelheid en max waterdiepte rasters worden gedownload. Dit wordt gedaan met de download functie in limburg.py Deze functie maakt een map met de naam van de simulatie en downloadt hier alle resultaten voor de desbretreffende simulatie. 

## 3. Afleiden kwetsbare panden

Voor het afleiden van de kwetsbare panden doorloop de volgende stappen.

### Stap 1: Maak postgis database
Om de kwetsbare panden af te leiden dient als eerst een postgis database gemaakt te worden op de utr-gis-db-01.nens.local server. Deze moet de volgende Schemas te hebben:

- public
- resultaten
- source  
- tmp

### Stap 2: Laad de source bestanden in postgis
In de source schema moeten de volgende twee tabellen worden ingeladen. 
1. panden_input: (dit zijn de panden die in het gebied liggen op basis van de BAG)
2. adressen: Deze tabel bevat punt geometrien van de panden waar een adres voor is. Dit zijn dus panden waar mensen wonen of werken en niet bijvoorbeeld de schuurtjes. 

### Stap 3: Richt je workdir in
De scripts voor het afleiden van panden kunnen het beste via superputty gedraaid worden aangezien het bash bestanden zijn. Dus maak een map in je workdir en zet hier de inhoud van "afleiden kwetsbare panden" in. Vul de volgende mappen 

1. waterdiepterasters: Zet in deze map de maximale waterdiepterasters voor alle simulaties waaarvoor de kwetsbare panden moeten worden afgeleid. 
2. shapefiles_deelgebieden

Geef in de deelgebieden.txt aan voor welke simulaties het script gedraaid moet worden.

Tip: Gebruik voor zowel de waterdiepterasters als shapefiles dezelfde namen.

### Stap 4: Draai code_superputty.sh
Dit script voert de volgende stappen uit:
1. Waterdieptes kleiner dan 0.02 worden uit het raster gehaald. Dit duidt namelijk niet op wateroverlast.
2. De nieuwe waterdiepteraster waar de verwaarloosbare waterdieptes uit zijn gehaald wordt omgezet naar een vector. 
3. De vector wordt in postgis ingeladen in het schma public met de naam watervlakken
4. De shapefile van het desbetreffende gebied wordt in postgis ingeladen in het schema public met de naam deelgebied
5. Het script combineer_watervlakken_panden.sql wordt gedraaid. Dit script knipt voor het deelgebied de panden en de adressen uit de source tabllen. Vervolgens wordt gekeken naar welke panden een adres hebben. Dit wordt in de panden tabel aangegeven in een extra kolom. Vervolgens wordt een buffer om de panden gemaakt van een 0.5m. Voor deze gebufferde panden wordt gekeken of deze intersect met de watervlakken die in stap 3 zijn gemaakt. Als er een watervlak tegen een pand aanligt wordt de oppervlakte van het watervlak overgenomen
6. De gebufferde panden tabel wordt opgeslagen als shapefile
7. Voor elk van de panden wordt de maximale en mediaan van de waterdiepteraster bepaald (zonal)
8. De shapefile met de statistieken wordt ingeladen in postgis met de naam panden_met_stats
9. De max waardes worden op 0 gezet als deze Nan zijn. 
10. In het schema resultaten wordt voor het deelgebied een tabel weggeschreven waar de oorsprong van het knelpunt is aangegeven. Knelpunten ontstaan pas bij 15 cm of hoger (de gekozen drempelwaarde). Deze worden op basis van de volgende criteria bepaald. 
    - oppervlakte watervlak > 200 m2 & maximale waarde waterdiepte > 0.15m: regioneel knelpunt
    - oppervlakte watervlak < 200 m2 & maximale waarde waterdiepte > 0.15m: lokaal knelpunt
    - Anders: geen knelpunt

### Stap 4: Combineer resultaten met samenvoegen_scenarios_tot_gecombineerde_knelpunten.sql
Dit script combineert de verschillende neerslag types (stedelijk, landelijk en gebiedsbreed) tot 1 gecombineerde knelpunten tabel. De namen van de tabellen die gebruikt moeten worden voor de afleiding moeten nog handmatig aangepast worden. Het script moet vervolgens in pgadmin gedraaid worden. (Dit kan eenvoudig toegevoegd worden aan de vorige stap.


### Stap 5: Voer checks uit.
Controleer of de scripts goed hebben gedraaid. 
- Check of het aantal knelpunten per categorie logisch is met het type neerslag
- Check of het totaal aantal panden overeenkomt met de som van alle knelpunt categorien.
- Check of het afgeleid watervlak tegen de panden ongeveer klopt met de lineaal functie in qgis (Dit kan steekproefgewjis)


### Stap 6: Download postgis tabellen als shapefiles.
Geef in de panden_rest.txt aan welke tabellen je wilt gaan downloaden. Vervolgens kan met het script downloaden.sh alle tabellen als shapefiles worden gedownload voor opleveringen. 
