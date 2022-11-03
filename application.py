from flask import Flask
import pandas as pd

import os
import csv 
import json 


app = Flask(__name__)

def removew(d):
    for k, v in d.items():
        if isinstance(v, dict):
            removew(v)
        else:
            d[k]=v.strip()


# Function to convert a CSV to JSON
# Takes the file paths as arguments
def make_json(csvFilePath):
     
    # create a dictionary
    data = {}
     
    # Open a csv reader called DictReader
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
         
        # Convert each row into a dictionary
        # and add it to data
        for rows in csvReader:
            key = rows['tx_date'].strip()
            data[key] = rows
 
    # Open a json writer, and use the json.dumps()
    # function to dump data
    removew(data)
    return json.dumps(data, indent=4)

@app.route('/api/request')
def format():
    dataList = os.listdir('data')
    dataList.sort(reverse=True)
    recentList = dataList[:10]
    recentList = ["~/api/data/" + s for s in recentList]
    recentCSV = pd.DataFrame()
    recentCSV = pd.concat(map(pd.read_csv, recentList))
    recentCSV.to_csv('recent.csv', index=False)
    return make_json('recent.csv')

if __name__ == '__main__':
    app.run()
