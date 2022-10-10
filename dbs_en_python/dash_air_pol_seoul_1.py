#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 15:37:14 2022

@author: frank
"""

from dash import Dash, dcc, html, Input, Output
import mysql.connector as sql
import pandas as pd
import plotly.express as px
import sys

# niet veilig (intern gebruik)
# eventueel gebruiker en paswoord opvragen via input
# cninfo is lijst met database, user, password, host
cninfo=('proto1','usr1','hetcvo.be','127.0.0.1')

# select queries voor dropdown boxen
select_query_type='''select * from measurement_type'''
select_query_station='''select * from station_info'''

# select query voor de grafiek
select_query_values='''select measure_time,avg(average_val) 
    from air_pol_measurement,measurement_type,station_info
    where measurement_type.name='%s' and station_info.name='%s' 
    and measurement_type.id=air_pol_measurement.measure_type_id 
    and station_info.id=air_pol_measurement.station_id 
    group by measure_time'''

try:
    
    # connectie maken met mysql database proto1 als gebruiker usr1
    cn=sql.connect(db=cninfo[0],user=cninfo[1],password=cninfo[2],host=cninfo[3])
    
    # dataframes maken van de select queries voor de dropdown boxen
    df_measurement_type=pd.read_sql(select_query_type,cn)
    print(df_measurement_type.head())
    df_station_info=pd.read_sql(select_query_station,cn)
    print(df_station_info.head())
    cn.disconnect()
    
    # Dash layout :
    # dropdown box measurement_type
    # dropdown box station_info
    # figuur : Yas -> avg(avgerage_val) X-as -> measure_time
    app = Dash(__name__)
    
    app.layout = html.Div([
        html.Div([
            dcc.Dropdown(df_measurement_type.name.to_list(),
                         df_measurement_type.name.to_list()[0],
                         id='type-dropdown'),
            dcc.Dropdown(df_station_info.name.to_list(),
                         df_station_info.name.to_list()[0],
                         id='station-dropdown'),
            ]),
        html.Div([dcc.Graph(id='dd-output-container-graph')])
    ])

    @app.callback(
        Output('dd-output-container-graph', 'figure'),
        Input('type-dropdown', 'value'),
        Input('station-dropdown', 'value')
        )
    
    def update_output(value1,value2):
        fig=None
        types=df_measurement_type.name.to_list()
        stations=df_station_info.name.to_list()
        # beide comboboxen gevuld
        if (value1 in types) and (value2 in stations):
            # connectie met databank opzetten
            cn=sql.connect(db=cninfo[0],user=cninfo[1],password=cninfo[2],host=cninfo[3])
            # dataframe maken met sql query
            df_values=pd.read_sql(select_query_values%(value1,value2),cn)
            # connectie met databank verbreken
            cn.disconnect()
            # figuur maken
            fig = px.line(df_values,x='measure_time',y='avg(average_val)')
        return fig

    if __name__ == '__main__':
        app.run_server(debug=True)

except Exception as E:
    print('problemen met lezen uit databank')
    print(E)
    sys.exit()
