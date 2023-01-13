# -*- coding: utf-8 -*-
"""
Created on Sat Nov 26 21:42:59 2022

@author: gebruiker
"""

from dash import Dash, dcc, html, Input, Output
from db_actions_monday_burger import actions_db_monday_burger
import pandas as pd
import plotly.express as px
import datetime
import time
import math


def log(err):
    f = open('log.txt','a')
    t = time.localtime()
    f.write(str(t.tm_hour)+':'+str(t.tm_min)+':'+str(t.tm_sec)+'##'+err+'\n')
    f.close()
    

class localData:
    
    def __init__(self):
        self.df_food = pd.DataFrame(columns=['time','product','stock'])
        self.df_drinks = pd.DataFrame(columns=['time','product','stock'])
        self.df_sauces = pd.DataFrame(columns=['time','product','stock'])
        
lcd = localData()
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

app.layout = html.Div([dcc.Tabs(id='tabs',value='login',children=[
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
    dcc.Tab(label="quick view voorraad",value="quickstock",id="quickstock",disabled=True,children=[init_table(data_tmp)])]),
    dcc.Interval(id='interval_stock',interval=30*1000,n_intervals=0)]
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
        today = now.strftime("%Y-%m-%d 00:00:00")
        df_now = dba.read_df_from_dbtable(qry, (today,))
        # datum van de tijd verwijderen
        pd.to_datetime(df_now['sa_timestamp']).dt.time
        # uitvoer naar csv test bestand
        # df_now.to_csv('test_orders.csv')
        # aantal klanten per 15 min indelen
        t=time.localtime()
        nbins=math.ceil((int(t.tm_hour)*60 + int(t.tm_min)-10*60)/15)
        fig_now = px.histogram(df_now,x='sa_timestamp',nbins=nbins)
 
        # histogram vorige periode
        qry = '''select * from sales_order where 
            sa_timestamp > now() - interval 3 week and 
            sa_timestamp < now() - interval 2 week'''
        df_prev = dba.read_df_from_dbtable(qry, ())
        # datum van de tijd verwijderen
        pd.to_datetime(df_now['sa_timestamp']).dt.time
        # aantal klanten per 15 min indelen
        nbins=math.ceil((21*60 + 30 -10*60)/15)
        fig_prev = px.histogram(df_prev,x='sa_timestamp',nbins=nbins)
        # database sluiten
        dba.quitdb()

        return fig_now,fig_prev
        
 
@app.callback(
    Output('interval_stock','n_intervals'),
    Input('interval_stock', 'n_intervals'))

def update_stock_status(interval):
    # opvullen dataframe zonder aanmelding
    dba.set_user('usr2')
    dba.set_password('hetcvo.be')

    # connectie met database
    res = dba.connect()
    if res == False:
        log('Error connection db')
        return interval

    # dataframe food opvullen
    res = dba.get_product_stock(1)
    log(str(res))
    df = pd.DataFrame(res,columns=['time', 'product', 'stock'])
    lcd.df_food = pd.concat([lcd.df_food,df])
    lcd.df_food.to_csv('test_stock_food.csv')

    # dataframe drinks opvullen
    res = dba.get_product_stock(2)
    log(str(res))
    df = pd.DataFrame(res,columns=['time', 'product', 'stock'])
    lcd.df_drinks = pd.concat([lcd.df_drinks,df])
    lcd.df_drinks.to_csv('test_stock_drinks.csv')

    # dataframe sauces opvullen
    res = dba.get_product_stock(3)
    log(str(res))
    df = pd.DataFrame(res,columns=['time', 'product', 'stock'])
    lcd.df_sauces = pd.concat([lcd.df_sauces,df])
    lcd.df_sauces.to_csv('test_stock_sauces.csv')
    dba.quitdb()
    
    return interval


@app.callback(
    Output('stock_food','figure'),
    Output('stock_drinks','figure'),
    Output('stock_sauces','figure'),
    Input('tabs','value'))

def update_stock_stat(tab):

    # food
    lcd.df_food.to_csv('control_stock.csv')
    fig_food = px.line(lcd.df_food,x='time',y='stock',color='product')
    
    # drinks
    lcd.df_drinks.to_csv('control_stock.csv')
    fig_drinks = px.line(lcd.df_drinks,x='time',y='stock',color='product')

    # sauces
    lcd.df_sauces.to_csv('control_stock.csv')
    fig_sauces = px.line(lcd.df_sauces,x='time',y='stock',color='product')

    return fig_food,fig_drinks,fig_sauces


if __name__ == '__main__':
    app.run_server(debug=True,host="0.0.0.0")