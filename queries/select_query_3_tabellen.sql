select measure_time as time,avg(average_val) as average from air_pol_measurement,measurement_type,station_info
where measurement_type.name='SO2' and station_info.name='Dobong-gu'
and measurement_type.id=air_pol_measurement.measure_type_id
and station_info.id=air_pol_measurement.station_id
group by measure_time