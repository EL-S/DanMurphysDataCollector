import requests
import xml.etree.ElementTree as ET

url = "https://www.danmurphys.com.au/robots.txt"
headers = {"User-Agent":"Mozilla 5.0/"}

robots_text = requests.get(url, headers=headers).text.strip().split("\n")

for line in robots_text:
    if "Sitemap:" in line and "Products" in line:
        product_sitemap_url = line.split("Sitemap:")[1].strip()

product_sitemap = requests.get(product_sitemap_url, headers=headers).text
#print(product_sitemap)

with open("product_sitemap.xml", "w") as file:
    file.write(product_sitemap)

root = ET.fromstring(product_sitemap)

for child in root:
    print(child.tag, child.attrib)
