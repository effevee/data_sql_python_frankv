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

# select query voor de grafiek
select_query_values='''select measure_time,avg(average_val) 
    from air_pol_measurement,measure_type,station_info
    where measure_type.name='%s' and station_info.name='%s' 
    and measure_type.id=air_pol_measurement.measure_type_id 
    and station_info.id=air_pol_measurement.station_id 
    group by measure_time'''

# Dash layout :
# 2 maal naast elkaar om te kunnen vergelijken
# dropdown box measurement_type
# dropdown box station_info
# figuur : Yas -> avg(avgerage_val) X-as -> measure_time
app = Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(df_measure_type.name.to_list(),
                         df_measure_type.name.to_list()[0],
                         id='type-dropdown-1'),
            dcc.Dropdown(df_station_info.name.to_list(),
                         df_station_info.name.to_list()[0],
                         id='station-dropdown-1'),
            ]),
        html.Div([dcc.Graph(id='dd-output-container-graph-1')])
        ],style={'width':'45%','display':'inline-block'}),
    html.Div([
        html.Div([
            dcc.Dropdown(df_measure_type.name.to_list(),
                         df_measure_type.name.to_list()[0],
                         id='type-dropdown-2'),
            dcc.Dropdown(df_station_info.name.to_list(),
                         df_station_info.name.to_list()[0],
                         id='station-dropdown-2'),
            ]),
        html.Div([dcc.Graph(id='dd-output-container-graph-2')])
        ],style={'width':'45%','display':'inline-block'})
    ])
    
@app.callback(
    Output('dd-output-container-graph-1', 'figure'),
    Output('dd-output-container-graph-2', 'figure'),
    Input('type-dropdown-1', 'value'),
    Input('station-dropdown-1', 'value'),
    Input('type-dropdown-2', 'value'),
    Input('station-dropdown-2', 'value'),
   )

def update_output(value1,value2,value3,value4):
    fig1=None
    fig2=None
    types=df_measure_type.name.to_list()
    stations=df_station_info.name.to_list()
    # beide comboboxen links gevuld
    if (value1 in types) and (value2 in stations):
        # connectie met databank opzetten
        dba.connect()
        # dataframe maken met sql query
        df_values=dba.read_df_from_dbtable(select_query_values%(value1,value2),())
        # connectie met databank verbreken
        dba.quitdb()
        # figuur maken
        fig1=px.line(df_values,x='measure_time',y='avg(average_val)')
    # beide comboboxen links gevuld
    if (value3 in types) and (value4 in stations):
        # connectie met databank opzetten
        dba.connect()
        # dataframe maken met sql query
        df_values=dba.read_df_from_dbtable(select_query_values%(value3,value4),())
        # connectie met databank verbreken
        dba.quitdb()
        # figuur maken
        fig2=px.line(df_values,x='measure_time',y='avg(average_val)')
    return fig1,fig2

if __name__ == '__main__':
    app.run_server(debug=True)

