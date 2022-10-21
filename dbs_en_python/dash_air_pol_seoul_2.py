#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 15:37:14 2022

@author: frank
"""

from dash import Dash, dcc, html, Input, Output
from db_actions import actions
import plotly.express as px

#constructor klasse oproepen met aangepaste waarden voor connectie
dba=actions(usr='usr1',pwd='hetcvo.be')

# connecteren met de databank
dba.connect()

# data frame voor dropdown measure type
df_measure_type=dba.read_df_from_dbtable('select * from measure_type',())

# data frame voor dropdown station
df_station_info=dba.read_df_from_dbtable('select * from station_info',())

# database afsluiten
dba.quitdb()


# Dash layout :
# 2 maal naast elkaar om te kunnen vergelijken
# dropdown box measurement_type
# dropdown box station_info
# figuur : Yas -> avg(avgerage_val) X-as -> measure_time
app = Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(list(df_measure_type.name),placeholder='Select type',
                         id='type-dropdown-1'),
            dcc.Dropdown(list(df_station_info.name),placeholder='Select station',
                         id='station-dropdown-1'),
            ]),
        html.Div([dcc.Graph(id='dd-output-container-graph-1')])
        ],style={'width':'50%','display':'inline-block'}),
    html.Div([
        html.Div([
            dcc.Dropdown(list(df_measure_type.name),placeholder='Select type',
                         id='type-dropdown-2'),
            dcc.Dropdown(list(df_station_info.name),placeholder='Select station',
                         id='station-dropdown-2'),
            ]),
        html.Div([dcc.Graph(id='dd-output-container-graph-2')])
        ],style={'width':'50%','display':'inline-block'})
    ],style={'text-align':'center'})
    
@app.callback(
    Output('dd-output-container-graph-1', 'figure'),
    Input('type-dropdown-1', 'value'),
    Input('station-dropdown-1', 'value'),
   )

def update_output_1(sensor1,station1):
    # beide comboboxen gevuld
    if sensor1 != 'Select type' and station1 != 'Select station':
        # connectie met databank opzetten
        dba.connect()
        # select query voor de grafiek
        select_query_values='''select measure_time,avg(average_val) 
            from air_pol_measurement,measure_type,station_info
            where measure_type.name=%s and station_info.name=%s 
            and measure_type.id=air_pol_measurement.measure_type_id 
            and station_info.id=air_pol_measurement.station_id 
            group by measure_time'''
        # dataframe maken met sql query
        df_values=dba.read_df_from_dbtable(select_query_values,(sensor1,station1))
        # connectie met databank verbreken
        dba.quitdb()
        # figuur maken
        fig1=px.line(df_values,x='measure_time',y='avg(average_val)')
        fig1.data[0].line.color='#ff0000'
        return fig1
    else:
        return None

@app.callback(
    Output('dd-output-container-graph-2', 'figure'),
    Input('type-dropdown-2', 'value'),
    Input('station-dropdown-2', 'value'),
   )

def update_output_2(sensor2,station2):
    # beide comboboxen gevuld
    if sensor2 != 'Select type' and station2 != 'Select station':
        # connectie met databank opzetten
        dba.connect()
        # select query voor de grafiek
        select_query_values='''select measure_time,avg(average_val) 
            from air_pol_measurement,measure_type,station_info
            where measure_type.name=%s and station_info.name=%s 
            and measure_type.id=air_pol_measurement.measure_type_id 
            and station_info.id=air_pol_measurement.station_id 
            group by measure_time'''
        # dataframe maken met sql query
        df_values=dba.read_df_from_dbtable(select_query_values,(sensor2,station2))
        # connectie met databank verbreken
        dba.quitdb()
        # figuur maken
        fig2=px.line(df_values,x='measure_time',y='avg(average_val)')
        fig2.data[0].line.color='#0000ff'
        return fig2
    else:
        return None

if __name__ == '__main__':
    app.run_server(debug=True)

