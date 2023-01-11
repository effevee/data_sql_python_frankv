# -*- coding: utf-8 -*-
"""
Created on Sat Nov 26 21:42:59 2022

@author: gebruiker
"""

from dash import Dash, dcc, html, Input, Output, dash_table
from db_actions_monday_burger import actions_db_monday_burger
import pandas as pd
import plotly.express as px
import datetime
import time
import math


dba = actions_db_monday_burger(db='dbonly_monday_burger', host='127.0.0.1')

# leeg dataframe met 3 kolommen
df_food = pd.DataFrame(columns=['time','stock','product'])

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
    dcc.Tab(label="quick view voorraad",value="quickstock",id="quickstock",disabled=True,children=[init_table(data_tmp)]),
    dcc.Interval(id='interval_stock',interval=60*1000,n_intervals=0)]
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
            

@app.callback(
    Output('num_clients_today','figure'),
    Output('num_clients_prev_week','figure'),
    Input('tabs','value'))

def update_tab_num_clients(tab):
    if tab == 'num_clients':
        # connectie met database
        dba.connect()
        
        # histogram vandaag
        qry ='''select * from sales_order where sa_timestamp >= %s'''
        # sales orders in dataframe stoppen
        now = datetime.datetime.now()
        today = now.strftime("%y-%m-%d 00:00:00")
        df_now = dba.read_df_from_dbtable(qry, (today,))
        # datum van de tijd verwijderen
        pd.to_datetime(df_now['sa_timestamp']).dt.time
        # uitvoer naar csv test bestand
        # df_now.to_csv('test_orders.csv')
        # aantal klanten per 15 min indelen
        t=time.localtime()
        nbins=math.ceil((int(t.tm_hour)*60 + int(t.tm_min)-18*60)/15)
        fig_now = px.histogram(df_now,x='sa_timestamp',nbins=nbins)
 
        # histogram vorige periode
        qry = '''select * from sales_order where 
            sa_timestamp > now() - interval 3 week and 
            sa_timestamp < now() - interval 2 week'''
        df_prev = dba.read_df_from_dbtable(qry, ())
        # datum van de tijd verwijderen
        pd.to_datetime(df_now['sa_timestamp']).dt.time
        # aantal klanten per 15 min indelen
        nbins=math.ceil((21*60 + 30 -18*60)/15)
        fig_prev = px.histogram(df_prev,x='sa_timestamp',nbins=nbins)
        # database sluiten
        dba.quitdb()

        return fig_now,fig_prev
        
 
@app.callback(
    Output('interval_stock','n_intervals'),
    Input('interval_stock', 'n_intervals'))

def update_stock_status(interval):
    # query food stock
    qry_food = '''select pr_name,po_stock from purchase_order,product 
        where pr_id=po_productid and pr_categoryid=1'''           
    # connectie met database
    dba.connect()
    # dataframe opvullen
    df_stock_food = dba.read_df_from_dbtable(qry_food, ())
    products = df_stock_food['pr_name'].to_list()  # lijst producten
    stocks = df_stock_food['po_stock'].to_list()   # lijst stocks
    # tijd ophalen
    t=time.localtime()
    now = t.tm_hour + ':' + t.tm_min
    # dataframe grafiek opvullen
    for i in range(len(products)):
        # distionary om rij toe te voegen aan dataframe
        row = {'time':now, 'stock':stocks[i], 'product':products[i]}
        # toevoegen aan globale dataframe
        df_food.append(row)
    # test
    df_food.to_csv('test_stock_food.csv')
    dba.quitdb()
    
    return interval

if __name__ == '__main__':
    app.run_server(debug=True,host="0.0.0.0")