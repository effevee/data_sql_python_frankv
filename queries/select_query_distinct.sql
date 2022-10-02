select distinct measure_type_id from air_pol_measurement;
select distinct station_id,measure_type_id from air_pol_measurement;
select station_id, count(distinct station_id,measure_type_id) from air_pol_measurement group by station_id;