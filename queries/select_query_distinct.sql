select distinct station_id from air_pol_measurement;
select distinct measure_type_id from air_pol_measurement;
select distinct station_id,measure_type_id from air_pol_measurement;
# tellen (count) van het aantal unieke (distinct) waarden in 2 kolommen (station_id, measure_type_id)
# group by is groeperen per station_id
select station_id, count(distinct station_id,measure_type_id) from air_pol_measurement group by station_id;