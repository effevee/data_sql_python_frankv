select measure_time,average_val from air_pol_measurement where station_id=105 and measure_type_id=1;
# per dag de gemiddelde waarde van sensor type 1 en station 105 
select measure_time,avg(average_val) from air_pol_measurement where station_id=105 and measure_type_id=1 group by measure_time;
select measure_time,avg(average_val) from air_pol_measurement where station_id=105 and measure_type_id=1 group by measure_time;