#!/usr/bin/env python3

import requests
import sys
import json
import time
import collections
import pubchempy as pcp 
import re

sys.stdout = open('names.json','wt') # this script will output to a file for further processing

response = requests.get("http://tripbot.tripsit.me/api/tripsit/getAllDrugNames") #getting druglist from tripsit api

response = response.json() # parsing druglist into python list

response = response['data'] #removing outer list

response = response[0] # removing outer list

names = []

for value in response:      #remove none values
    if value is not None:
        names.append(value)

synonyms = []

count = 0

for name in names:

    # This block of code 

    #if count == 15: 

    #   break

    result = pcp.get_compounds(name, 'name')

    cid = re.sub("[^0-9]", "", str(result))


    url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/" + cid + "/JSON?heading=mesh+entry+terms"

    synonyms_json = requests.get(url)

    synonyms_list = synonyms_json.json()

    
    try: synonyms_list = synonyms_list['Record']['Section'][0]['Section'][0]['Section'][0]['Information'][0]['Value']['StringWithMarkup']
    
    except KeyError:

        pass

    for synonym in synonyms_list:

        if type(synonym) is str:

            synonyms.append(synonym)

        else:

            for key, value in synonym.items():

                synonyms.append(value)

    count = count + 1

    #print (count)

fault = 'Fault'

while fault in synonyms:

    synonyms.remove(fault)


mt45 = 'MT 45'

while mt45 in synonyms:

    synonyms.remove(mt45)


for name in synonyms:
    
    if len(name) < 4:

        synonyms.remove(name)

synonyms = json.dumps(synonyms) #converting python list to json

print(synonyms)

