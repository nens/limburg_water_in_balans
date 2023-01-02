DROP TABLE IF EXISTS resultaten.hekerbeekdal_t25;
create table resultaten.hekerbeekdal_t25 as
select lan.identifica, lan.bouwjaar, lan.adres, lan.geom, greatest(lan.area, ste.area, geb.area) as area, greatest(lan.max, ste.max, geb.max) as max, greatest(lan.median, ste.median, geb.median) as median,
case when lan.knelpunt = 'regionaal' and ste.knelpunt = 'regionaal' and geb.knelpunt = 'regionaal' then 'stedelijk en regionaal knelpunt'
when lan.knelpunt = 'regionaal' and ste.knelpunt = 'regionaal' and geb.knelpunt = 'lokaal' then 'stedelijk en regionaal knelpunt'
when lan.knelpunt = 'regionaal' and ste.knelpunt = 'regionaal' and geb.knelpunt = 'geen knelpunt' then 'stedelijk en regionaal knelpunt'
when lan.knelpunt = 'regionaal' and ste.knelpunt = 'lokaal' and geb.knelpunt = 'regionaal' then 'landelijk regionaal knelpunt'
when lan.knelpunt = 'regionaal' and ste.knelpunt = 'lokaal' and geb.knelpunt = 'lokaal' then 'landelijk regionaal knelpunt'
when lan.knelpunt = 'regionaal' and ste.knelpunt = 'lokaal' and geb.knelpunt = 'geen knelpunt' then 'landelijk regionaal knelpunt'
when lan.knelpunt = 'regionaal' and ste.knelpunt = 'geen knelpunt' and geb.knelpunt = 'regionaal' then 'landelijk regionaal knelpunt'
when lan.knelpunt = 'regionaal' and ste.knelpunt = 'geen knelpunt' and geb.knelpunt = 'lokaal' then 'landelijk regionaal knelpunt'
when lan.knelpunt = 'regionaal' and ste.knelpunt = 'geen knelpunt' and geb.knelpunt = 'geen knelpunt' then 'landelijk regionaal knelpunt'
when lan.knelpunt = 'lokaal' and ste.knelpunt = 'regionaal' and geb.knelpunt = 'regionaal' then 'stedelijk regionaal knelpunt'
when lan.knelpunt = 'lokaal' and ste.knelpunt = 'regionaal' and geb.knelpunt = 'lokaal' then 'stedelijk regionaal knelpunt'
when lan.knelpunt = 'lokaal' and ste.knelpunt = 'regionaal' and geb.knelpunt = 'geen knelpunt' then 'stedelijk regionaal knelpunt'
when lan.knelpunt = 'lokaal' and ste.knelpunt = 'lokaal' and geb.knelpunt = 'regionaal' then 'gebiedsbreed regionaal knelpunt'
when lan.knelpunt = 'lokaal' and ste.knelpunt = 'lokaal' and geb.knelpunt = 'lokaal' then 'lokaal knelpunt'
when lan.knelpunt = 'lokaal' and ste.knelpunt = 'lokaal' and geb.knelpunt = 'geen knelpunt' then 'lokaal knelpunt'
when lan.knelpunt = 'lokaal' and ste.knelpunt = 'geen knelpunt' and geb.knelpunt = 'regionaal' then 'gebiedsbreed regionaal knelpunt'
when lan.knelpunt = 'lokaal' and ste.knelpunt = 'geen knelpunt' and geb.knelpunt = 'lokaal' then 'lokaal knelpunt'
when lan.knelpunt = 'lokaal' and ste.knelpunt = 'geen knelpunt' and geb.knelpunt = 'geen knelpunt' then 'lokaal knelpunt'
when lan.knelpunt = 'geen knelpunt' and ste.knelpunt = 'regionaal' and geb.knelpunt = 'regionaal' then 'stedelijk regionaal knelpunt'
when lan.knelpunt = 'geen knelpunt' and ste.knelpunt = 'regionaal' and geb.knelpunt = 'lokaal' then 'stedelijk regionaal knelpunt'
when lan.knelpunt = 'geen knelpunt' and ste.knelpunt = 'regionaal' and geb.knelpunt = 'geen knelpunt' then 'stedelijk regionaal knelpunt'
when lan.knelpunt = 'geen knelpunt' and ste.knelpunt = 'lokaal' and geb.knelpunt = 'regionaal' then 'gebiedsbreed regionaal knelpunt'
when lan.knelpunt = 'geen knelpunt' and ste.knelpunt = 'lokaal' and geb.knelpunt = 'lokaal' then 'lokaal knelpunt'
when lan.knelpunt = 'geen knelpunt' and ste.knelpunt = 'lokaal' and geb.knelpunt = 'geen knelpunt' then 'lokaal knelpunt'
when lan.knelpunt = 'geen knelpunt' and ste.knelpunt = 'geen knelpunt' and geb.knelpunt = 'regionaal' then 'gebiedsbreed regionaal knelpunt'
when lan.knelpunt = 'geen knelpunt' and ste.knelpunt = 'geen knelpunt' and geb.knelpunt = 'lokaal' then 'lokaal knelpunt'
else 'geen knelpunt'
end as knelpunt
from resultaten.hekerbeekdal_t25_landelijk lan
left join resultaten.hekerbeekdal_t25_stedelijk ste
on ste.identifica = lan.identifica 
left join resultaten.hekerbeekdal_t25_gebiedsbreed geb 
on lan.identifica = geb.identifica;
