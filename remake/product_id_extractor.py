import requests
import xml.etree.ElementTree as ET

url = "https://www.danmurphys.com.au/robots.txt"
headers = {"User-Agent":"Mozilla 5.0/"}

robots_text = requests.get(url, headers=headers).text.strip().split("\n")

for line in robots_text:
    if "Sitemap:" in line and "Products" in line:
        product_sitemap_url = line.split("Sitemap:")[1].strip()

print(product_sitemap_url)
product_sitemap = requests.get(product_sitemap_url, headers=headers).text
#print(product_sitemap)
print(len('你'.encode('utf-8')))
print(len(product_sitemap.encode('utf-8')))

with open("product_sitemap.xml", "w") as file:
    file.write(product_sitemap)

root = ET.fromstring(product_sitemap)

product_ids = []

for child in root:
    if "product" in child[0].text:
        product_id = child[0].text.split("/")[-2]
        product_ids.append(product_id)

print(product_ids, len(product_ids))
