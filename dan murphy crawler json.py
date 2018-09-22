from bs4 import BeautifulSoup
from tornado import ioloop, httpclient
from random import randint
import re
import json

i = 0


def get_products():
    #do some crawling and collect all product url's
    #save them all to a file
    return True

def get_info():
    http_client = httpclient.AsyncHTTPClient(force_instance=True,defaults=dict(user_agent="Mozilla/5.0"),max_clients=2)
    for product_id_new in open('product_urls.txt'):
        global i
        i += 1
        url = "https://api.danmurphys.com.au/apis/ui/Product/"+str(product_id_new)
        http_client.fetch(url.strip(),handle_request_index, method='GET',connect_timeout=10000,request_timeout=10000)
    ioloop.IOLoop.instance().start()

def get_cost(html):
    #code
    return True

def get_standard_drinks(html):
    #code
    return True

def save_to_csv(html,url):
    #regexshit = re.sub(r'[\\/*?:"<>|]',"",data[3])
    #print(to_standard_characters(file_name)) #doesn't suppose Non-BMP characters without above code
    # parse the html using beautiful soup and store in variable `soup`
    result = json.loads(html)['Products']
    try:
        per_bottle_cost = result[0]['Prices']['singleprice']['Value'] #fine
    except:
        try:
            per_bottle_cost = result[0]['Prices']['inanysixprice']['Value'] #fine
        except:
            return
    try:
        per_case_of_6 = result[0]['Prices']['caseprice']['Value'] #fine
    except:
        try:
            per_case_of_6 = "None" #fine
        except:
            return
    additional_details = result[0]['AdditionalDetails'] #fine
    category1 = result[0]['Categories'][0]['Name'].replace(" ", "_").lower()
    try:
        category2 = result[0]['Categories'][1]['Name'].replace(" ", "_").lower()
    except:
        category2 = "None"
    for x in additional_details:
        if x['Name'] == "standarddrinks":
            if "x" in x['Value']:
                standard_drinks = x['Value'].replace(" ","")
                standard_drinks = standard_drinks.split("x")
                standard_drinks = float(standard_drinks[0])*float(standard_drinks[1])
                print(standard_drinks,"yeet")
            else:
                standard_drinks = float(x['Value'][:3])
        elif x['Name'] == "webalcoholpercentage":
            if "x" in x['Value']:
                alcohol_percentage = x['Value'].replace(" ","")
                alcohol_percentage = alcohol_percentage.replace("%","")
                alcohol_percentage = alcohol_percentage.split("x")
                alcohol_percentage = float(alcohol_percentage[1])
                print(alcohol_percentage,"yeet")
            else:
                alcohol_percentage = x['Value'][:3]
        elif x['Name'] == "webliquorsize":
            size = x['Value']
    #print(per_bottle_cost,per_case_of_6,size,alcohol_percentage,standard_drinks,category,url)
    try:
        size
    except NameError:
        size = "701mL" #there's no information about the size at all so we will use 701mL
    try:
        standard_drinks
    except NameError:
        if size[-2:-1] == "m":
            new_size = float(size[:-2])/1000
        else:
            new_size = float(size[:-1])
        standard_drinks = new_size * float(alcohol_percentage[:-1]) * float(0.789)
        print("yeet2")
    price_per_standard_drink = str(float(per_bottle_cost)/float(standard_drinks))
    file_name = "data.csv"
    full_path = "data/" + file_name
    data = (str(price_per_standard_drink),str(per_bottle_cost),str(per_case_of_6),size,str(alcohol_percentage),str(standard_drinks),category1,category2,url)
    print(data)
    data_line = ",".join(data)
    with open(full_path, "a", encoding="utf-8") as data_csv:
        data_csv.write(data_line+"\n")

def handle_request_index(response):
    if response.code == 599:
        print(response.effective_url)
        http_client.fetch(response.effective_url.strip(), handle_request, method='GET',connect_timeout=10000,request_timeout=10000)
    else:
        html = response.body.decode('utf-8')
        url = response.effective_url
        time = response.request_time
        print(url,time)
        save_to_csv(html,url)
        global i
        i -= 1
        if i == 0:
            ioloop.IOLoop.instance().stop()

get_info()
