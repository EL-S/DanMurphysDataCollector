from bs4 import BeautifulSoup
from tornado import ioloop, httpclient
from random import randint
import re
from selenium import webdriver
from requests_html import HTMLSession


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
    print(html)
    #regexshit = re.sub(r'[\\/*?:"<>|]',"",data[3])
    #print(to_standard_characters(file_name)) #doesn't suppose Non-BMP characters without above code

    # parse the html using beautiful soup and store in variable `soup`
    
    soup = BeautifulSoup(html, 'html.parser')
    try:
        drink_data = soup.findAll("li", { "class" : "list--details_item ng-star-inserted" })
        if drink_data:
            #print(drink_data)
            for x in drink_data:
                y = x.find("span",recursive=False)
                print(y.text, y.next_sibling.text)
            
    except:
        print("Couldn't find data",url)
    
    standard_drinks = str(randint(1,40))
    cost = str(randint(3,100))
    price_per_standard_drink = str(int(cost)/int(standard_drinks))
    file_name = "data.csv"
    full_path = "data/" + file_name
    data = (standard_drinks,cost,price_per_standard_drink,url,"\n")
    data_line = ",".join(data)
    with open(full_path, "w", encoding="utf-8") as data_csv:
        data_csv.write(data_line)

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
        #process into fetch list
        #insitiate all with content handler (max client 10?)

get_info()
