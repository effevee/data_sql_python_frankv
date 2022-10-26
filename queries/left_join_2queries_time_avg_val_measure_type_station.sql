select time,avg_left,avg_right from
(select measure_time as time,avg(average_val) as avg_left from air_pol_measurement,measure_type,station_info  where 
measure_type.name = 'SO2' and measure_type.id = air_pol_measurement.measure_type_id and
station_info.name = 'Dongjak-gu' and station_info.id = air_pol_measurement.station_id
group by measure_time) as t1
 left join (
select measure_time as time_right,avg(average_val) as avg_right from air_pol_measurement,measure_type,station_info where 
measure_type.name = 'CO' and measure_type.id = air_pol_measurement.measure_type_id and
station_info.name = 'Dongjak-gu' and station_info.id = air_pol_measurement.station_id
group by measure_time) as t2
on t1.time = t2.time_right