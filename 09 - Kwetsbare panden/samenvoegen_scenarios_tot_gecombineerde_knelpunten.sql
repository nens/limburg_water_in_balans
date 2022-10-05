DROP TABLE IF EXISTS resultaten.verwacht_t100;
create table resultaten.verwacht_t100 as
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
from resultaten.verwacht_t25_landelijk_v2_t100 lan
left join resultaten.verwacht_t25_stedelijk_v2_t100 ste
on ste.identifica = lan.identifica 
left join resultaten.verwacht_t25_gebiedsbreed_v2_t100 geb 
on lan.identifica = geb.identifica;
