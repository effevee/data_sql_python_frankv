# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 17:01:58 2022

@author: gebruiker
"""

#
# Copyright 2021 HiveMQ GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import time
import paho.mqtt.client as paho
from paho import mqtt
import threading
import json
from db_actions_monday_burger import actions_db_monday_burger
import random


dba = None      # variable database
client = None   # variable client

def store_order(msg,dba,client):
    dba.connect()
    # fetch data from mqtt structure
    fname = msg['who']['firstname']
    lname = msg['who']['lastname']
    email = msg['who']['email']
    address = msg['who']['street']+' '+msg['who']['town']
    date_parts = msg['who']['birth'].split('-') # EUR date format
    birth = date_parts[2]+'-'+date_parts[1]+'-'+date_parts[0]
    # insert customer
    customer_id = dba.insert_customer(fname,lname,birth,email,address)
    # insert sales_order
    sales_order_id = dba.insert_sales_order(customer_id,msg['status'])
    # insert product_order
    dba.insert_product_order(msg['products'],sales_order_id)
    # time to prepare order
    time.sleep(random.randint(2, 5))
    # publish status via mqtt
    if sales_order_id > 0:
        dba.update_order_status(sales_order_id,'READY')
        client.publish('hetcvo_sqldb_python_022_respons/frankvg_16',payload=str(sales_order_id))
    dba.quitdb()
    
# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))

# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    # order message
    if 'hetcvo_sqldb_python_022/' in msg.topic:
        # convert message to json object
        msg = json.loads(str(msg.payload.decode()))
        # create thread (subprocess)
        th = threading.Thread(target=store_order,args=(msg,dba,client,))
        # start thread
        th.start()
    # status message
    elif msg.topic == 'hetcvo_sqldb_python_022_delivered/frankvg_16':
        dba.connect()
        sales_order_id = int(str(msg.payload.decode()))
        dba.update_order_status(sales_order_id, 'DELIVERED')
        dba.quitdb()

# create database object
dba = actions_db_monday_burger(db='dbonly_monday_burger',
                               host='127.0.0.1',
                               usr='dev2',
                               pwd='hetcvo_2022.be')
# using MQTT version 5 here, for 3.1.1: MQTTv311, 3.1: MQTTv31
# userdata is user defined data of any type, updated by user_data_set()
# client_id is the given name of the client
client = paho.Client(client_id="frankvg_16", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect

# enable TLS for secure connection
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# set username and password
client.username_pw_set("filip", "fdes@2022")
# connect to HiveMQ Cloud on port 8883 (default for MQTT)
client.connect("3fa295cd989c45948e66687fcc39e5d1.s1.eu.hivemq.cloud", 8883)

# setting callbacks, use separate functions like above for better visibility
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish

# subscribe to all topics of encyclopedia by using the wildcard "#"
client.subscribe("hetcvo_sqldb_python_022/#", qos=1)
client.subscribe('hetcvo_sqldb_python_022_delivered/frankvg_16', qos=1)
# a single publish, this can also be done in loops, etc.
#client.publish("encyclopedia/temperature", payload="hot", qos=1)

# loop_forever for simplicity, here you need to stop the loop manually
# you can also use loop_start and loop_stop
#client.loop_forever()
client.loop_start()
try:
    while True:
        # hier kunnen we eventueel algemene code in plaatsen
        time.sleep(0.005)
except:
    pass
finally:
    client.loop_stop()
    