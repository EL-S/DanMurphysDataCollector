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
    http_client = httpclient.AsyncHTTPClient(force_instance=True,defaults=dict(user_agent="Mozilla/5.0"),max_clients=150)
    for url in open('product_urls.txt'):
        global i
        i += 1
        http_client.fetch(url.strip(), handle_request_index, method='GET',connect_timeout=20,request_timeout=20)
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
    per_bottle_cost = result[0]['Prices']['singleprice']['Value']
    per_case_of_6 = result[0]['Prices']['caseprice']['Value']
    additional_details = result[0]['AdditionalDetails'] # result is now a dict
    size = additional_details[5]['Value']
    alcohol_percentage = additional_details[6]['Value']
    standard_drinks = additional_details[9]['Value']
    category = additional_details[11]['Value']
    
    print(per_bottle_cost,per_case_of_6,size,alcohol_percentage,standard_drinks,category,url)
    price_per_standard_drink = str(int(per_bottle_cost)/int(standard_drinks))
    file_name = "data.csv"
    full_path = "data/" + file_name
    data = (str(per_bottle_cost),str(per_case_of_6),str(price_per_standard_drink),size,alcohol_percentage,standard_drinks,category,url)
    print(data)
    data_line = ",".join(data)
    with open(full_path, "w", encoding="utf-8") as data_csv:
        data_csv.write(data_line+"\n")

def handle_request_index(response):
    if response.code == 599:
        print(response.effective_url)
        http_client.fetch(response.effective_url.strip(), handle_request, method='GET',connect_timeout=3,request_timeout=3)
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
