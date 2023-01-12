import pandas as pd
import os
import random
import json
import requests
import lxml.html
import sys
import time
import paho.mqtt.publish as publish
import certifi
import ssl


NUM_PERSONS = 2000
DAY = "MA"
p_rain = 0.3
MIN_GEM_DL_BZ = round((1.3371+1.2236)/2,4)
now_gem_dl_bz = 2
URL_1 = "https://geertnaessens.be/"
URL_2 = "https://bestat.statbel.fgov.be/bestat/crosstable.xhtml?view=3a4cfb82-0c67-4f97-94f3-58b2509763ab"
df_customers = None

class hardcoded_data:
    
    def __init__(self):
        self._broker = "3fa295cd989c45948e66687fcc39e5d1.s1.eu.hivemq.cloud"
        self._prefix ="hetcvo_sqldb_python_022"
    
    def set_broker(self,broker):
        self._broker = broker
    
    def set_prefix(self,prefix):
        self._prefix = prefix
    
def send_current_order(order):
    
    topic = hdc._prefix+"/"+order["who"]["firstname"]+"/"+order["who"]["lastname"]
    try:
        tls = { 'ca_certs':certifi.where(),'tls_version': ssl.PROTOCOL_TLSv1_2 }
        auth = {'username':"filip", 'password':"fdes@2022"}
        order.update({"ask_time":time.strftime("%d-%m-%Y#%H%M%S",time.localtime())})
        msg = json.dumps(order)
        publish.single(topic, payload=msg, qos=0, retain=True, hostname=hdc._broker, port=8883, client_id="cvo_order_simulator_"+str(random.randint(1000,22222)), keepalive=60, will=None, auth=auth, tls=tls, transport="tcp")
        print(time.strftime("%d-%m-%Y#%H%M%S",time.localtime())+":MQTT send order from:"+order["who"]["firstname"]+" "+order["who"]["lastname"]+"\n")
    except Exception as e:
        print(time.strftime("%d-%m-%Y#%H%M%S",time.localtime())+":MQTT error:"+str(e)+"\n")

hdc = hardcoded_data()

data_food = None
with open("products.json","r") as f:
    data_food = json.load(f)
#print(data_food)

res = requests.get(URL_1)
page = res.content
if res.status_code != 200:
    print("probleem ophalen website")
    sys.exit()
    
html = lxml.html.fromstring(page)
day = html.xpath("/html/body/div[1]/div[2]/main/div/section/div/div/div[5]/div/div[1]/div/div[1]/h1")
if day[0].text == DAY:
    rain = html.xpath("/html/body/div[1]/div[2]/main/div/section/div/div/div[5]/div/div[1]/div/div[8]/div[2]/div/div[1]/h5")
    rain = float(rain[0].text.replace("%",""))
    p_rain = rain/100
#print(p_rain)

res = requests.get(URL_2)
page = res.content
if res.status_code != 200:
    print("probleem ophalen website")
    sys.exit()
html = lxml.html.fromstring(page)
pbz = html.xpath("/html/body/div[4]/div[3]/div/span/div[2]/div/span[2]/span[1]/form/div/table/tbody/tr[1]/td[8]")
pbz = float(pbz[0].text.replace(",","."))

pdl = html.xpath("/html/body/div[4]/div[3]/div/span/div[2]/div/span[2]/span[1]/form/div/table/tbody/tr[5]/td[8]")
pdl = float(pdl[0].text.replace(",","."))

now_gem_dl_bz = round((pbz+pdl)/2,4)
p_gem_dl_bz = round((now_gem_dl_bz - MIN_GEM_DL_BZ)/MIN_GEM_DL_BZ,4)
print(p_gem_dl_bz)

content = os.listdir()
#print(content)

if "customers.csv" in content:#customer file already in folder
    df_customers=pd.read_csv("customers.csv",encoding='utf-8')
else:
    #open files with firstname
    df_girls = pd.read_excel("Namen\\Voornamen_meisjes_1995-.xlsx",encoding='utf-8')
    df_boys = pd.read_excel("Namen\\Voornamen_Jongens_1995-.xlsx",encoding="utf-8")
    df_last = pd.read_excel("Namen\\Familienamen_2022.xlsx",encoding="utf-8")
    
    print("girls names:")
    #print(df_girls.head())
    l_girls = list(df_girls["Unnamed: 1"])
    #print(l_girls)
    
    print("boys names:")
    #print(df_boys.head())
    l_boys = list(df_boys["Unnamed: 1"])
    #print(l_boys)
    
    print("Last names:")
    #print(df_last.head())
    l_last = list(df_last["Unnamed: 1"])
    #print(l_last)
    
    max_choice = min(len(l_girls),len(l_boys),len(l_last))
    
    #cities and streets
    city_files = os.listdir("Straten")
    d_cities_streets = {}
    for cf in city_files:
        city = cf[cf.index("_")+1:cf.index(".")]
        streets = []
        with open("Straten\\"+cf,"r") as f:
            for l in f:
               l=" ".join(l.split())
               parts = l.split()
               if len(parts)<2:
                   continue
               if len(parts[0]) > 3:
                   streets.append(parts[0])
        d_cities_streets.update({city:streets})
    print(d_cities_streets)
        
    
    df_customers = pd.DataFrame([["Jules","Kabas","jules.kabas@gmail.com","12-12-1946","Deinze","Karrewegstraat 22"]],columns=['firstname','lastname','email','birthdate','city','address'])
    n=0
    while n<=NUM_PERSONS:
        n+=1
        fname = ""
        lname = ""
        i = random.randint(1,max_choice)-1
        if n%2 == 0:
            fname = l_girls[i]
        else:
            fname = l_boys[i]
        
        i = random.randint(1,max_choice)-1
        lname = l_last[i]
        providers = ("hotmail.com","telenet.be","proximus.be","orange.be","yahoo.fr","google.com","vrt.be","hetcvo.be","oudenaarde.be")
        email_part = providers[random.randint(1,len(providers))-1]
        email = fname.replace(" ","_")+"."+lname.replace(" ","_")+"@"+email_part
        year = range(1940,2008)
        year = year[random.randint(1,len(year))-1]
        birthday = str(random.randint(1,28))+"-"+str(random.randint(1,12))+"-"+str(year)
        res = df_customers[(df_customers["firstname"] == fname) & (df_customers["lastname"] == lname)]
        if len(res) > 0:#is already present
            n-=1
            continue
        
        all_cities = list(d_cities_streets.keys())
        city = all_cities[random.randint(1,len(all_cities))-1]
        street = d_cities_streets[city][random.randint(1,len(d_cities_streets[city]))-1]+" "+str(random.randint(1,140))
        df_tmp = pd.DataFrame([[fname,lname,email,birthday,city,street]],columns = ['firstname','lastname','email','birthdate','city','address'])
        df_customers = pd.concat([df_customers,df_tmp])
    print(df_customers)
    df_customers.to_csv("customers.csv")

print(df_customers.head())

#select list --> emails
l_emails = list(df_customers["email"])
while True:
    order = {}
    #random customer
    cus_email = l_emails[random.randint(0,len(l_emails)-1)]
    cus = df_customers[df_customers["email"] == cus_email]
    cus_detail = {"firstname":cus.iloc[0]["firstname"],"lastname":cus.iloc[0]["lastname"],"email":cus_email,"birth":cus.iloc[0]["birthdate"],"town":cus.iloc[0]["city"],"street":cus.iloc[0]["address"]}
    order.update({"who":cus_detail})
    #random order
    #food, number of hamburgers and choice
    num_hamburgers = random.randint(1,8)
    #divide by 2, whole part one type of hamburger, modulus other type hamburger
    num_type1 = num_hamburgers - num_hamburgers%2
    num_type2 = num_hamburgers%2
    choice = random.randint(1,100)
    products = {}
    if num_type1 > 0 and choice > 50:
        products.update({data_food["food"][1]:num_type1})
    elif num_type1 > 0 and choice <= 50:
        products.update({data_food["food"][0]:num_type1})
    
    if num_type2 > 0 and choice > 50:
        products.update({data_food["food"][0]:num_type2})
    elif num_type2 > 0 and choice <= 50:
        products.update({data_food["food"][1]:num_type2})
    
    #number of drinks and choice
    num_drinks = random.randint(1,10)
    drinks_dist = [0]*len(data_food["drinks"])
    for i in range(num_drinks):
        drink_id = random.randint(0,len(data_food["drinks"])-1)
        drinks_dist[drink_id]+=1
    j=0
    for d in data_food["drinks"]:
        if drinks_dist[j] != 0:
            products.update({d:drinks_dist[j]})
        j+=1
    
    #number of sauces and choice
    num_sauces = num_hamburgers - random.randint(1,4)
    if num_sauces < 0:
        num_sauces = num_hamburgers
    sauces_dist = [0]*len(data_food["sauces"])
    for i in range(num_sauces):
        sauce_id = random.randint(0,len(data_food["sauces"])-1)
        sauces_dist[sauce_id]+=1
    j=0
    for s in data_food["sauces"]:
        if sauces_dist[j] != 0:
            products.update({s:sauces_dist[j]})
        j+=1
    
    #Orders update and send
    order.update({"products":products})
    #status: PAID, NOT_PAID
    p_paid = random.randint(0,100)
    if p_paid <= 95:
        order.update({"status":"PAID"})
    else:
        order.update({"status":"NOT_PAID"})
    print(order)
    send_current_order(order)
    pause = 20 - 7*p_rain + 6.5*p_gem_dl_bz + random.uniform(-1.8,1.8)
    print("the pause:",pause)
    time.sleep(pause)
    
        
        
        
    
    
                                                                                                                                                
    
    


        
            
        
    
    
