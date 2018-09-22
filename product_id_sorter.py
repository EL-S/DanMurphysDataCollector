import os

directory = "images"
for filename in os.listdir(directory):
    if filename.endswith(".png"): 
        print(filename[:-6])
        
        continue
    else:
        continue
