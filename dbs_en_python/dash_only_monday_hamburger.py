# -*- coding: utf-8 -*-
"""
Created on Sat Nov 26 21:42:59 2022

@author: gebruiker
"""

from dash import Dash, dcc, html, Input, Output, dash_table
from db_actions_monday_burger import actions_db_monday_burger

dba = actions_db_monday_burger(db='dbonly_monday_burger', host='127.0.0.1')

data_tmp={"Hamburger gezond":"OK","Cola":"OK","Ketchup":"OK"}

def init_table(data):
    vals = list(data.values())
    dash_obj = html.Table([
        html.Tr([html.Th(col) for col in list(data.keys())]),
        html.Tr([html.Td(vals[j],id="+\""+str(j)+"_status\"",style={"background-color":"green","color":"white"}) for j in range(0,len(vals))])]
        )
    return dash_obj

app = Dash(__name__)

app.layout = dcc.Tabs(id='tabs',value='login',children=[
    dcc.Tab(label='login',value='login',id='tab_login',children=[
            dcc.Input(id='in-name',type='text',placeholder='naam'),
            dcc.Input(id='in-pwd',type='password',placeholder='paswoord'),
            html.Button("aanmelden",id='btn-login')]
        ),
     dcc.Tab(label='aantal klanten',disabled=True,value='num_clients',id='num_clients',children=[
         html.Div([
             html.Div([dcc.Graph(id="num_clients_today")],id="left_panel",style={"width":"45%","border":"solid","float":"left"}),
             html.Div([dcc.Graph(id="num_clients_prev_week")],id="right_panel",style={"width":"45%","border":"solid","float":"left"})])
         ])
         ,
    dcc.Tab(label="voorraad",value="stock",id="stock",disabled=True,children=[
        dcc.Graph(id="stock_food"),
        dcc.Graph(id="stock_drinks"),
        dcc.Graph(id="stock_sauces")]),
    dcc.Tab(label="quick view voorraad",value="quickstock",id="quickstock",disabled=True,children=[init_table(data_tmp)])]
    )

@app.callback(
    Output('num_clients','disabled'),
    Output('stock','disabled'),
    Output('quickstock','disabled'),
    Output('btn-login','n_clicks'),
    Input('in-name','value'),
    Input('in-pwd','value'),
    Input('btn-login','n_clicks'))

def login(name,pwd,clicks):
    if clicks > 0:
        try:
            # gebruikersnaam doorgeven
            dba.set_user(name)
            # paswoord doorgeven
            dba.set_password(pwd)
            # connecteren met de databank
            dba.connect()
            if dba.check_connect() == False:
                raise Exception('No Connection')
            # databank sluiten
            dba.quitdb()
            # login ok, tabs dash enabled
            return False, False, False, 0
        except:
            # login nok, tabs dash disabled
            return True, True, True, 0
            
    

if __name__ == '__main__':
    app.run_server(debug=True,host="0.0.0.0")