#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 15:37:14 2022

@author: frank
"""

from dash import Dash, dcc, html, Input, Output
from db_actions import actions

#constructor klasse oproepen met aangepaste waarden voor connectie
dba=actions(usr='usr1',pwd='hetcvo.be')

# connecteren met de databank
dba.connect()

# data frame voor dropdown measure type
df_measure_type=dba.read_df_from_dbtable('select * from measure_type')

# data frame voor dropdown station
df_station_info=dba.read_df_from_dbtable('select * from station_info')

# database afsluiten
dba.quitdb()

# Dash layout :
# dropdown box measurement_type
# dropdown box station_info
# figuur : Yas -> avg(avgerage_val) X-as -> measure_time
app = Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(df_measure_type.name.to_list(),
                 placeholder='Select type',
                 id='type-dropdown'),
    dcc.Dropdown(df_station_info.name.to_list(),
                 placeholder='Select station',
                 id='station-dropdown'),
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
