--creer nieuwe tabel met de watervlakken, waar de wateroppervlakte aan toe wordt gevoegd
DROP TABLE IF EXISTS tmp.wateroppervlakten;
create table tmp.wateroppervlakten as
select * from watervlakken, st_area(watervlakken.geom) as area;

--creer nieuwe tabel met de panden voor een deelgebied
DROP TABLE IF EXISTS tmp.panden;
create table tmp.panden as
SELECT pt.*
FROM source.panden_input pt,
deelgebied deel
where ST_Intersects(pt.geom, deel.geom);
--Kolom toevoegen of een pand ook een adres is
DROP TABLE IF EXISTS tmp.panden_opgeschoond_adressen;
create table tmp.panden_opgeschoond_adressen AS
SELECT distinct on(a.identifica) a.identifica, a.bouwjaar, a.geom,
case when b.id is not null then 1 else 0 end as adres
from tmp.panden a
left join source.adressen b
on st_intersects(b.geom,a.geom)
group by a.identifica, a.bouwjaar, a.geom, b.id;

CREATE INDEX ON tmp.panden_opgeschoond_adressen USING GIST (geom);

-- Creer een nieuwe tabel, met buffer van 0.5 m om de panden. Neem identifica en bouwjaar mee
DROP TABLE IF EXISTS tmp.panden_backup_buffer;
create table tmp.panden_backup_buffer as
select identifica, bouwjaar, adres, st_buffer(geom,+0.5) as geom from tmp.panden_opgeschoond_adressen;

--combineer wateroppervlakten met panden voor het deelgebied in kwestie
CREATE INDEX ON tmp.panden_backup_buffer USING GIST (geom);
CREATE INDEX ON tmp.wateroppervlakten USING GIST (geom);

DROP TABLE IF EXISTS tmp.buffer_panden_wateroppervlakten;
create table tmp.buffer_panden_wateroppervlakten as
select pa.identifica, pa.bouwjaar, pa.adres, pa.geom, sum(st_area(pb.geom)) as area
from tmp.panden_backup_buffer pa
left join tmp.wateroppervlakten pb
on ST_Intersects(pa.geom, pb.geom) group by pa.identifica, pa.bouwjaar, pa.geom, pa.adres;

-- Creer een nieuwe tabel, met het verschil tussen de gebufferde en niet gebufferde panden. Alleen bij gelijke ID, neem bouwjaar en identifica weer mee
DROP TABLE IF EXISTS tmp.pand_tot;
create table tmp.pand_tot as
select b.identifica, b.bouwjaar, b.adres, b.area,st_difference(st_force2d(b.geom),st_force2d(a.geom)) as geom, a.geom as pand
from tmp.panden_opgeschoond_adressen a, tmp.buffer_panden_wateroppervlakten b 
where a.identifica = b.identifica;
