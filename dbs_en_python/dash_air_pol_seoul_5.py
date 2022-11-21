#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 20:32:45 2022

@author: frank
"""

from dash import Dash, dcc, html, Input, Output
from db_actions import actions
from store_data import store_df  # om dataframes in het geheugen te houden
import pandas as pd
import plotly.express as px


def replace_outliers(df,col):
    mean=df[col].mean()   # gemiddelde
    stdev=df[col].std()   # standaard deviatie
    min_limit=mean-3*stdev  # ondergrens
    max_limit=mean+3*stdev  # bovengrens
    # door de kolomwaarden van het dataframe lopen
    clean=[]
    for v in df[col].to_list():  # van de kolom een lijst maken
        if v>min_limit and v<max_limit:  # waarde ligt in interval
            clean.append(v)                  # behoud waardd
        else:                            # waarde buiten interval
            clean.append(mean)               # vervangen door gemiddelde
    df[col]=clean   # kolom vervangen door opgekuiste data
    return df
            

#constructor klasse oproepen met aangepaste waarden voor connectie
dba=actions()

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
    html.Div([dcc.Input(id='in-name',type='text',placeholder='naam'),
              dcc.Input(id='in-pwd',type='password',placeholder='paswoord'),
              html.Button("aanmelden",id='btn-login',n_clicks=0)],
             style={'padding':'20px','text-align':'right'}),
    html.Div([
        html.Div([
            dcc.Dropdown([],placeholder='Select type',id='type-dropdown-1'),
            dcc.Dropdown([],placeholder='Select station',id='station-dropdown-1'),
            ]),
        html.Div([dcc.Graph(id='dd-output-container-graph-1')])
        ],style={'width':'50%','display':'inline-block'}),
    html.Div([
        html.Div([
            dcc.Dropdown([],placeholder='Select type',id='type-dropdown-2'),
            dcc.Dropdown([],placeholder='Select station',id='station-dropdown-2'),
            ]),
        html.Div([dcc.Graph(id='dd-output-container-graph-2')])
        ],style={'width':'50%','display':'inline-block'}),
    html.Div([
        html.Button('Correlatie', id='corr-btn', n_clicks=0,disabled=True, 
                    style={'width':'80%','height':'60px','font-size':'22px'}),
        dcc.Graph(id='corr-graph'),
        html.Div(id='corr-data')
        ])
    ],style={'text-align':'center'})
    
@app.callback(
    Output('dd-output-container-graph-1', 'figure'),
    Input('type-dropdown-1', 'value'),
    Input('station-dropdown-1', 'value')
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
        # outliers verwijderen
        df_values=replace_outliers(df_values,'avg(average_val)')
        # dataframe bewaren voor correlatie grafiek
        sdfs.set_df(0, df_values)
        # connectie met databank verbreken
        dba.quitdb()
        # figuur maken
        fig1=px.line(df_values,x='measure_time',y='avg(average_val)')
        fig1.data[0].line.color='#ff0000'
        return fig1
    return None

@app.callback(
    Output('dd-output-container-graph-2', 'figure'),
    Input('type-dropdown-2', 'value'),
    Input('station-dropdown-2', 'value')
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
        # outliers verwijderen
        df_values=replace_outliers(df_values,'avg(average_val)')
        # dataframe bewaren voor correlatie grafiek
        sdfs.set_df(1, df_values)
        # connectie met databank verbreken
        dba.quitdb()
        # figuur maken
        fig2=px.line(df_values,x='measure_time',y='avg(average_val)')
        fig2.data[0].line.color='#0000ff'
        return fig2
    return None

@app.callback(
    Output('corr-graph', 'figure'),
    Output('corr-data', 'children'),
    Output('corr-btn', 'n_clicks'),
    Input('corr-btn', 'n_clicks')
    )

def update_corr(num_clicks):
    # zitten beide dataframes in het object sdfs en is er op de knop gedrukt
    if sdfs.get_notnone_dfs()==2 and num_clicks==1:
        # ophalen dataframes uit object
        df1=sdfs.get_df(0)  # linker dataframe
        df2=sdfs.get_df(1)  # rechter dataframe
        # kolommen in dataframes hernoemen
        df1.rename(columns={'avg(average_val)':'left_avg'}, inplace=True)
        df2.rename(columns={'avg(average_val)':'right_avg'}, inplace=True)
        # dataframes mergen voor de correlatie 
        # left join met als referentie measure_time kolom van het linker dataframe (df1)
        df=pd.merge(df1,df2,how='left')
        # scatter plot is uitzetten van punten
        scatter=px.scatter(df,x='left_avg',y='right_avg')
        # correlatie factor is een getal tussen -1 en +1, hoe dichter bij de
        # uitersten hoe beter het verband, rond 0 geen verband
        cr=df['left_avg'].corr(df['right_avg'])
        # 1ste elem : figuur, 2de elem : correlatie berekening, 3de elem : clicks op 0
        return scatter,'correlatie:'+str(cr),0
    
    # dataframes niet volledig of knop niet ingedrukt
    return None

@app.callback(
    Output('type-dropdown-1','options'),
    Output('station-dropdown-1','options'),
    Output('type-dropdown-2','options'),
    Output('station-dropdown-2','options'),
    Output('corr-btn','disabled'),
    Output('btn-login','n_clicks'),
    Input('btn-login','n_clicks'),
    Input('in-name','value'),
    Input('in-pwd','value')
    )

def login_action(clicks,name,pwd):
    if clicks > 0:
        try:
            # gebruikersnaam doorgeven
            dba.set_user(name)
            # paswoord doorgeven
            dba.set_password(pwd)
            # connecteren met de databank
            dba.connect()
            # data frame voor dropdown measure type
            df_measure_type=dba.read_df_from_dbtable('select * from measure_type',())
            # data frame voor dropdown station
            df_station_info=dba.read_df_from_dbtable('select * from station_info',())
            # database afsluiten
            dba.quitdb()
            types=list(df_measure_type['name'])
            stations=list(df_station_info['name'])
            return types,stations,types,stations,False,0
        except Exception as e:
            return [],[],[],[],True,0
    return [],[],[],[],True,0
            
            
        
    
    
    
if __name__ == '__main__':
    app.run_server(debug=True)

