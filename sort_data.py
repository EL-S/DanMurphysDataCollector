import sys
import csv
full_path = "data/data.csv"
full_path_new = "data/data1.csv"
reader = csv.reader(open(full_path), delimiter=",")

sortedlist = sorted(reader, key=lambda row: row[0], reverse=True)

with open(full_path_new, "a", encoding="utf-8") as data_csv:
    for x in sortedlist:
        data = ",".join(x)
        data_csv.write(data+"\n")
