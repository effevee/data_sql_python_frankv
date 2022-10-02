select sensor_state from air_pol_measurement where measure_type_id=1;
select measure_time,average_val,measure_type_id from air_pol_measurement where station_id=105;
select measure_time,average_val from air_pol_measurement where station_id=105 and measure_type_id=1;