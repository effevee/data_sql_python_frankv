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
    # 2 maal naast elkaar om te kunnen vergelijken
    # dropdown box measurement_type
    # dropdown box station_info
    # figuur : Yas -> avg(avgerage_val) X-as -> measure_time
    app = Dash(__name__)
    
    app.layout = html.Div(
        [html.Div(
            [html.Div([
                dcc.Dropdown(df_measurement_type.name.to_list(),
                             df_measurement_type.name.to_list()[0],
                             id='type-dropdown-1'),
                dcc.Dropdown(df_station_info.name.to_list(),
                             df_station_info.name.to_list()[0],
                             id='station-dropdown-1'),
                ]),
                html.Div([dcc.Graph(id='dd-output-container-graph-1')])
            ]),
        ],    
        [html.Div(
            [html.Div([
                dcc.Dropdown(df_measurement_type.name.to_list(),
                             df_measurement_type.name.to_list()[0],
                             id='type-dropdown-2'),
                dcc.Dropdown(df_station_info.name.to_list(),
                             df_station_info.name.to_list()[0],
                             id='station-dropdown-2'),
                ]),
                html.Div([dcc.Graph(id='dd-output-container-graph-2')])
            ]),
         ], style={'width':'45%','display':'inline-block'})

    @app.callback(
        Output('dd-output-container-graph-1', 'figure'),
        Output('dd-output-container-graph-2', 'figure'),
        Input('type-dropdown-1', 'value'),
        Input('station-dropdown-1', 'value'),
        Input('type-dropdown-2', 'value'),
        Input('station-dropdown-2', 'value')
        )
    
    def update_output(value1,value2,value3,value4):
        fig1=None
        fig2=None
        types=df_measurement_type.name.to_list()
        stations=df_station_info.name.to_list()
        # beide comboboxen links gevuld
        if (value1 in types) and (value2 in stations):
            # connectie met databank opzetten
            cn=sql.connect(db=cninfo[0],user=cninfo[1],password=cninfo[2],host=cninfo[3])
            # dataframe maken met sql query
            df_values1=pd.read_sql(select_query_values%(value1,value2),cn)
            # connectie met databank verbreken
            cn.disconnect()
            # figuur maken
            fig1 = px.line(df_values1,x='measure_time',y='avg(average_val)')
        '''# beide comboboxen rechts gevuld
        if (value3 in types) and (value4 in stations):
            # connectie met databank opzetten
            cn=sql.connect(db=cninfo[0],user=cninfo[1],password=cninfo[2],host=cninfo[3])
            # dataframe maken met sql query
            df_values2=pd.read_sql(select_query_values%(value3,value4),cn)
            # connectie met databank verbreken
            cn.disconnect()
            # figuur maken
            fig2 = px.line(df_values2,x='measure_time',y='avg(average_val)')'''
        return fig1

    if __name__ == '__main__':
        app.run_server(debug=True)

except Exception as E:
    print(E)
    sys.exit()
