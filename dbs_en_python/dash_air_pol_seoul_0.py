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
df_measure_type=dba.read_df_from_dbtable('select * from measure_type',())

# data frame voor dropdown station
df_station_info=dba.read_df_from_dbtable('select * from station_info',())

# database afsluiten
dba.quitdb()

# Dash layout :
# dropdown box measurement_type
# dropdown box station_info
# figuur : Yas -> avg(avgerage_val) X-as -> measure_time
app = Dash(__name__) # maken dash object

app.layout = html.Div([
    dcc.Dropdown(list(df_measure_type.name),placeholder='Select type',
                 id='type-dropdown'),
    dcc.Dropdown(list(df_station_info.name),placeholder='Select station',
                 id='station-dropdown'),
    html.Div(id='dd-output-container')
])  # layout van de app, is een html pagina met een div met daarin 2
    # dropdown boxen en een div met tekst van de geselecteerde opties

@app.callback(
    Output('dd-output-container', 'children'),
    Input('type-dropdown', 'value'),
    Input('station-dropdown', 'value')
    )

def update_output(value1, value2):
    return f'You selected {value1} and {value2}'

# het callback blok (@ is een python decorator)
# wordt actief als de dropdown boxen wijzigen (Input)
# met update_output wordt er iets gedaan met de waarden van de dropdowns
# de geretourneerde waarde wordt doorgegeven aan Output (dd-output-container)

if __name__ == '__main__':
    app.run_server(debug=True)  # opstarten van de webapp server
    
# je kan het resultaat raadplegen in een browser op url http://localhost:8050
    
