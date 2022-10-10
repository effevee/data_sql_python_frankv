#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 15:37:14 2022

@author: frank
"""

from dash import Dash, dcc, html, Input, Output
import mysql.connector as sql
import pandas as pd
import sys

# niet veilig (intern gebruik)
# eventueel gebruiker en paswoord opvragen via input
# cninfo is lijst met database, user, password, host
cninfo=('proto1','usr1','hetcvo.be','127.0.0.1')

# select queries voor dropdown boxen
select_query_type='''select * from measurement_type'''
select_query_station='''select * from station_info'''

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
        dcc.Dropdown(df_measurement_type.name.to_list(),placeholder='Select type',id='type-dropdown'),
        dcc.Dropdown(df_station_info.name.to_list(),placeholder='Select station',id='station-dropdown'),
        html.Div(id='dd-output-container')
    ])

    @app.callback(
        Output('dd-output-container', 'children'),
        Input('type-dropdown', 'value'),
        Input('station-dropdown', 'value')
        )
    
    def update_output(value1, value2):
        return f'You selected {value1} and {value2}'

    if __name__ == '__main__':
        app.run_server(debug=True)

except Exception as E:
    print('problemen met lezen uit databank')
    print(E)
    sys.exit()
