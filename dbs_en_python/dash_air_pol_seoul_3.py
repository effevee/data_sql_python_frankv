#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 16 09:33:13 2022

@author: frank
"""

from dash import Dash, dcc, html, Input, Output
from db_actions import actions
from store_data import store_df  # om dataframes in het geheugen te houden
import pandas as pd
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

# instance aanmaken voor het bijhouden van 2 dataframes
sdfs=store_df(2)

# Dash layout :
# 2 maal naast elkaar om te kunnen vergelijken
# dropdown box measurement_type
# dropdown box station_info
# figuur : Yas -> avg(avgerage_val) X-as -> measure_time
# daaronder knop om correlatie grafiek af te beelden
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
        ],style={'width':'50%','display':'inline-block'}),
    html.Div([
        html.Button('Correlatie', id='corr-btn', n_clicks=0),
        dcc.Graph(id='corr-graph'),
        html.Div(id='container-data')
        ])
    ],style={'text-align':'center'})
    
@app.callback(
    Output('dd-output-container-graph-1', 'figure'),
    Input('type-dropdown-1', 'value'),
    Input('station-dropdown-1', 'value'),
   )

def update_output_1(sensor,station):
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
        # dataframe bewaren voor correlatie grafiek
        sdfs.set_df(0, df_values)
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

def update_output_2(sensor,station):
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
        # dataframe bewaren voor correlatie grafiek
        sdfs.set_df(1, df_values)
        # connectie met databank verbreken
        dba.quitdb()
        # figuur maken
        fig2=px.line(df_values,x='measure_time',y='avg(average_val)')
        fig2.data[0].line.color='#0000ff'
        return fig2
    else:
        return None

@app.callback(
    Output('corr-graph', 'figure'),
    Output('container-data', 'children'),
    Input('corr-btn', 'n_clicks'),
    )

def update_corr(n_clicks):
    # is er geklikt op de button en zitten beide dataframes in het object sdfs
    if n_clicks>0 and sdfs.get_notnone_dfs()==2:
        # ophalen dataframes uit object
        df1=sdfs.get_df(0)
        df2=sdfs.get_df(1)
        # kolommen hernoemen
        df1.rename(columns={'avg(average_val)':'left avg'}, inplace=True)
        df2.rename(columns={'avg(average_val)':'right avg'}, inplace=True)
        # dataframes mergen voor de correlatie
        df=pd.merge(df1,df2,how='left')
        # figuur maken
        fig=px.scatter(df,x='left avg',y='right avg')
        # correlatie factor
        corr_fact=0
        return fig,corr_fact
    else:
        return None,0

if __name__ == '__main__':
    app.run_server(debug=True)

