from bs4 import BeautifulSoup
from tornado import ioloop, httpclient
from random import randint
import requests
import xml.etree.ElementTree as ET
import re
import json
import os

# optimise speed and add option to fix invalid data
# create a server running this that constantly keeps track of products and price changes
# store data in a database that the website can query using php or maybe js and API/Widget

file_name = "data.json"
directory = "data/"
i = 0
product_ids = []
threads = 2
first = True
last = False
total = 0
counter = 1

def init():
    global file_name,directory
    try:
        os.stat(directory)
    except:
        os.mkdir(directory)
    try:
        with open(directory+file_name, "r") as file:
            pass
    except:
        with open(directory+file_name, "w") as file:
            file.write("")

def get_product_ids():
    global product_ids,total
    url = "https://www.danmurphys.com.au/robots.txt"
    headers = {"User-Agent":"Mozilla 5.0/"}

    robots_text = requests.get(url, headers=headers).text.strip().split("\n")

    for line in robots_text:
        if "Sitemap:" in line and "Products" in line:
            product_sitemap_url = line.split("Sitemap:")[1].strip()

    print(product_sitemap_url)
    product_sitemap = requests.get(product_sitemap_url, headers=headers).text

    print("SiteMap FileSize:",len(product_sitemap.encode('utf-8')))

    with open("product_sitemap.xml", "w") as file:
        file.write(product_sitemap)

    root = ET.fromstring(product_sitemap)

    product_ids = []

    for child in root:
        if "product" in child[0].text:
            product_id = child[0].text.split("/")[-2]
            product_ids.append(product_id.split("DM_")[-1])

    total = len(product_ids)
    print("Products:",total)

    with open("product_ids.txt", "w") as file:
        file.write("\n".join(product_ids))

def get_info():
    global product_ids,threads
    http_client = httpclient.AsyncHTTPClient(force_instance=True,defaults=dict(user_agent="Mozilla/5.0"),max_clients=threads)
    for product_id_new in product_ids:
        global i
        i += 1
        url = "https://api.danmurphys.com.au/apis/ui/Product/"+str(product_id_new)
        http_client.fetch(url.strip(),handle_request_index, method='GET',connect_timeout=10000,request_timeout=10000)
    ioloop.IOLoop.instance().start()

def save_to_json(html,url):
    global file_name,directory,first,last,counter
    json = "\"Products"+str(counter)+"\":["+html+"]" #converts it to a sub json part of the larger data file
    full_path = directory + file_name
    if i == 0:
        last = True
    with open(full_path, "a", encoding="utf-8") as data_json:
        if first:
            data_json.write("{"+json)
            first = False
        elif last:
            data_json.write(","+json+"}")
        else:
            data_json.write(","+json)
    counter += 1

def handle_request_index(response):
    global total
    if response.code == 599:
        print(response.effective_url)
        http_client.fetch(response.effective_url.strip(), handle_request, method='GET',connect_timeout=10000,request_timeout=10000)
    else:
        global i
        i -= 1
        html = response.body.decode('utf-8')
        url = response.effective_url
        time = response.request_time
        percent = 100 - ((i/total)*100)
        percent_str = '{:.2f}'.format(round(percent, 2))+"%"
        print(percent_str,url,time)
        save_to_json(html,url)
        if i == 0:
            ioloop.IOLoop.instance().stop()

init()
get_product_ids()
get_info()
