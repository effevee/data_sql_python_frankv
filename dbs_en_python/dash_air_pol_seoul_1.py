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
# dropdown box measurement_type
# dropdown box station_info
# figuur : Yas -> avg(avgerage_val) X-as -> measure_time
app = Dash(__name__)

app.layout = html.Div([
    html.Div([
        dcc.Dropdown(list(df_measure_type.name),placeholder='Select type',
                     id='type-dropdown'),
        dcc.Dropdown(list(df_station_info.name),placeholder='Select station',
                     id='station-dropdown'),
        ]),
    html.Div([dcc.Graph(id='dd-output-container-graph')])
])

@app.callback(
    Output('dd-output-container-graph', 'figure'),
    Input('type-dropdown', 'value'),
    Input('station-dropdown', 'value')
    )

def update_output(sensor,station):
    # beide comboboxen gevuld
    if sensor != 'Select type' and station != 'Select station':
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
        df_values=dba.read_df_from_dbtable(select_query_values,(sensor,station))
        # connectie met databank verbreken
        dba.quitdb()
        # figuur maken
        fig=px.line(df_values,x='measure_time',y='avg(average_val)')
        fig.data[0].line.color='#ff0000'
        return fig
    else:
        return None

if __name__ == '__main__':
    app.run_server(debug=True)
