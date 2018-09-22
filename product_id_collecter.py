categories = ["red-wine","white-wine","champagne-sparkling","whisky","spirits","beer","cider","fortified-wine"]
category_pages = ["","","","","","","",""]
links = []


for i in categories:
    link = "https://www.danmurphys.com.au/"+i+"/all?page="
    links.append(link)

print(links)
