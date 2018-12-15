import json

flag = False

try:
    with open("data/data.json", "r", encoding="utf-8") as file:
        raw_data = file.read()
    continue_flag = True
except:
    print("Run the downloader first.")
    continue_flag = False

def sanitize_percent(percent):
    if "%" in percent:
        if ("," in percent): #this killed me
            percent = percent.replace("and",",")
            parts = percent.split(",")
            avg = 0
            amount = 0
            for part in parts:
                if "x" in part:
                    part = part.split("x")
                    amount += float(part[0].strip())
                    avg += float(part[0].replace("%","").strip())*float(part[1].replace("%","").strip())
                else:
                    avg += float(part.replace("%","").strip())
                    amount += 1
            percent = round(float(avg)/float(amount),3)
        elif ("-" in percent):
            parts = percent.split("-")
            avg = 0
            for part in parts:
                part = part.replace("%","")
                avg += float(part.strip())
            percent = round(float(avg)/len(parts),1)
        elif "(" in percent:
            percent = percent.split("(")[0].replace("%","").split()[0]
        elif "<" in percent:
            percent = percent.replace("<","").replace("%","").split()[0]
        else:
            percent = percent.replace("%","").split()[0] #before rounding
        try:
            if float(percent) > 100: #divide by 100 to get the percentage
                percent = float(percent)/100
            else:
                if len(str(percent)) > 5: #round the floating point errors
                    percent = round(float(percent),1)
                else:
                    pass #all good
        except: #garbage
            try:
                percent_old = percent.split("x")
                percent = percent_old
                for part in percent_old:
                    if "." in part:
                        percent = part
            except:
                percent = "Unknown"
            if percent == percent_old:
                percent = "Unknown"
    else:
        try:
            if float(percent) > 100: #garbage 42857~ number that seems to be a issue with dm transfering dm_er data
                percent = "Unknown"
            else: #all good
                pass
        except:
            if r"\t" in percent:
                percent = percent.replace(r"\t","")
            else: #garbage
                percent = "Unknown"
    try:
        if percent != "Unknown":
            if float(percent) < 0.3:
                percent = float(percent)*100
            percent = str(float(percent))+"%"
    except:
        percent = "Unknown"
    return percent

def sanitize_size(size):
    try:
        size = int(size)
    except:
        pass
    try:
        size = size.lower() #so the pure numbers are kept
    except:
        pass
    if isinstance(size, int):
        if size <= 15: #litres
            size = size*1000
        size = str(size)+"mL"
    else:
        if "ml" in size:
            #print(size)
            if "x" in size:
                size = str(int(size.split("x")[0])*int(size.split("x")[1][:-2]))+"mL" #evaluates the total volume of the case
            elif " " in size:
                if "," in size: #converts the annoying csv sizes to a total mL
                    size = str(int(size.replace(" ","").split(",")[1].split("x")[1][:-2])*int(size.replace(" ","").split(",")[1].split("x")[0])+int(size.replace(" ","").split(",")[0].split("x")[0])*int(size.replace(" ","").split(",")[0].split("x")[1][:-2]))+"mL"
                else:
                    if "g" in size:
                        size = size.split()[0] #mass and a volume, so ignore the mass
                    elif ("&" in size) or ("/" in size) or ("and" in size): #add the random sums
                        parts = size.split()
                        size = 0
                        for part in parts:
                            if part[-2:] == "ml":
                                size += int(part[:-2])
                        size = str(size)+"mL"
                    else:
                        size = size.replace(" ","").replace("l","L")
            else:
                size = size.replace("l","L")
                #all is good
        elif "l" in size:
            if "n" in size: #"nl" instead of "ml" typo
                size = size.replace("n","m")
            elif "b" in size:
                size = str(int(size.replace(" ","").split("b")[0])*750)+"mL" #converts bottles to estimasted mL (750ml a bottle)
            elif "x" in size:
                size = str(int(float(size.split(" ")[-1].replace(" ","").split("l")[0])*1000))+"mL"
            elif "-" in size:
                size = str(int(float(size.replace(" ","").split("-")[0].split("l")[0])*1000))+"mL"
            else:
                size = str(int(float(size.replace(" ","").split("l")[0])*1000))+"mL"
        elif "g" in size:
            if "k" in size:
                size = str(int(float(size.split("kg")[0])*1000))+"g" #mass in g
            else:
                if " " in size: #garbage
                    size = "Unknown"
                else:
                    pass #mass in g
        else: #nonsense
            size = "Unknown"
    return size

def sanitize_standarddrinks(standarddrinks):
    standarddrinks = standarddrinks.lower()
    if "(" in standarddrinks:
        if "%" in standarddrinks: #probably garbage but will treat as standard drinks
            standarddrinks = standarddrinks.split()[0].replace("%","")
        elif "x" in standarddrinks:
            standarddrinks = float(standarddrinks.split("(")[0].strip().split("x")[0])*float(standarddrinks.split("(")[0].strip().split("x")[1])
        else:
            standarddrinks = standarddrinks.split("(")[0].strip()
    elif "a" in standarddrinks:
        parts = standarddrinks.split()
        total = 0
        for part in parts:
            try:
                total += float(part)
            except:
                pass
        if total > 0:
            standarddrinks = total
        else:
            standarddrinks = "Unknown"
    elif "b" in standarddrinks:
        standarddrinks = "Unknown"
    elif "d" in standarddrinks:
        standarddrinks = "Unknown"
    elif "x" in standarddrinks:
        #print(standarddrinks)
        #flag = True
        if "," in standarddrinks:
            parts = standarddrinks.split(",")
            total = 0
            for part in parts:
                if "x" in part:
                    part = part.split("x")
                    total += float(part[0])*float(part[1])
                else:
                    total += float(part.strip())
            standarddrinks = total
        elif "&" in standarddrinks:
            parts = standarddrinks.split("&")
            total = 0
            for part in parts:
                if "x" in part:
                    part = part.split("x")
                    total += float(part[0])*float(part[1])
                else:
                    total += float(part.strip())
            standarddrinks = total
        if " x " in standarddrinks:
            standarddrinks = round(float(standarddrinks.split(" x ")[0])*float(standarddrinks.split(" x ")[1]),1)
        else:
            parts = standarddrinks.split()
            total = 0
            for part in parts:
                if "x" in part:
                    part = part.split("x")
                    total += float(part[0])*float(part[1])
            standarddrinks = total
                
    elif "/" in standarddrinks:
        parts = standarddrinks.split("/")
        total = 0
        for part in parts:
            total += float(part.strip())
        standarddrinks = total
    elif "&" in standarddrinks:
        parts = standarddrinks.split("&")
        total = 0
        for part in parts:
            total += float(part.strip())
        standarddrinks = round(total,1)
    elif "%" in standarddrinks: #probably really alcohol percent lmao
        standarddrinks = standarddrinks.replace("%","")
    elif "-" in standarddrinks:
        parts = standarddrinks.split(" - ")
        avg = 0
        for part in parts:
            avg += float(part.strip())
        avg = round(avg/len(parts),1)
        standarddrinks = avg
    elif "<" in standarddrinks:
        standarddrinks = standarddrinks.replace("<","").replace(" ","")
    elif "," in standarddrinks:
        parts = standarddrinks.split(",")
        total = 0
        for part in parts:
            total += float(part.strip())
        standarddrinks = total
    elif ".." in standarddrinks:
        standarddrinks = standarddrinks.replace("..",".")
    else:
        pass #all numbers now
    return standarddrinks

def get_price(pricedetails):
    try:
        price = pricedetails['singleprice']['Value']
    except:
        try:
            case_amount = pricedetails['message'].split(" ")[-1]
            case_price = int(pricedetails['caseprice']['Value'])
            price = str(case_price/int(case_amount))
        except:
            try:
                price = pricedetails['inanysixprice']['Value']
            except:
                price = "Unknown"
    if str(price) == "0":
        price = "Unknown"
    return price

def get_price_per_standard_drink(price,standarddrinks):
    global flag
    if (standarddrinks != "Unknown") and (price != "Unknown"):
        try:
            price_per_standard_drink = round(float(price)/float(standarddrinks),5)
            flag = True
        except:
            price_per_standard_drink = "Unknown"
    else:
        price_per_standard_drink = "Unknown"
    return price_per_standard_drink

def get_url(dm_stockcode):
    try:
        url = "https://www.danmurphys.com.au/product/"+str(dm_stockcode)
    except:
        url = "Unknown"
    return url

if continue_flag == True:
    json_data = json.loads(raw_data)
    
    #main loop for saving data below

    for product_name in json_data:
        for product in json_data[product_name]:
            try:
                dm_stockcode = "DM_"+product["PackDefaultStockCode"]
                additionaldetails = product["Products"][0]['AdditionalDetails']
                pricedetails = product["Products"][0]['Prices']
                price = get_price(pricedetails)
                #print("-------------------------------------------------")
                standarddrinks = "Unknown"
                size = "Unknown"
                percent = "Unknown"
                alcohol_type = "Unknown"
                name = "Unknown"
                alcohol_type2 = "Unknown"
                alcohol_type3 = "Unknown"
                alcohol_type4 = "Unknown"
                reviews_amount = "0"
                flag = False
                for detail in additionaldetails: #details are not always in order
                    if detail['Name'] == "dm_stockcode":
                        dm_stockcode = detail['Value']
                    if detail['Name'] == "standarddrinks":
                        standarddrinks = detail['Value']
                        standarddrinks = sanitize_standarddrinks(standarddrinks)
                    if detail['Name'] == "webliquorsize":
                        size = detail['Value']
                        size = sanitize_size(size)
                    if detail['Name'] == "producttitle":
                        name = detail['Value']
                    if detail['Name'] == "webalcoholpercentage":
                        percent = detail['Value']
                        percent = sanitize_percent(percent)
                    if detail['Name'] == "webproducttype":
                        alcohol_type = detail['Value']
                    if detail['Name'] == "webmaincategory":
                        alcohol_type2 = detail['Value']
                    if detail['Name'] == "liquorstyle":
                        alcohol_type3 = detail['Value']
                    if detail['Name'] == "varietal":
                        alcohol_type4 = detail['Value']
                    if detail['Name'] == "webtotalreviewcount":
                        reviews_amount = detail['Value']
                        try:
                            int(reviews_amount)
                        except:
                            print(reviews_amount)
                price_per_standard_drink = get_price_per_standard_drink(price,standarddrinks)
                url = get_url(dm_stockcode)
    ##            if alcohol_type.lower() == "spirit":
    ##                flag = True
    ##            if alcohol_type.lower() == "beer":
    ##                flag = True
    ##            if alcohol_type.lower() == "wine":
    ##                flag = True
                if flag == True:
                    try:
                        size = str(size[:-2]) #remove "mL" for google drive sorting
                        #switch the data set below for a clean csv with review amounts
                        data = [str(price_per_standard_drink),str(price),str(standarddrinks),str(size),str(percent),str(reviews_amount),str(alcohol_type),str(name),str(alcohol_type2),str(alcohol_type3),str(alcohol_type4),str(dm_stockcode),str(url)]
                        #data = [str(reviews_amount),str(alcohol_type),str(alcohol_type2),str(url)]
                        counter = 0
                        for part in data: #remove all false commas
                            if "," in part:
                                data[counter] = part.replace(",","")
                            counter += 1
                        data_str = ",".join(data)+"\n"
                        #print(price_per_standard_drink,price,standarddrinks,size,percent,alcohol_type,name,alcohol_type2,alcohol_type3,alcohol_type4,dm_stockcode,url)
                        with open("data\\data.csv", "a") as file:
                            file.write(data_str)
                    except Exception as e:
                        print("error",e)
            except Exception as e:
                pass
