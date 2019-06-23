#!/usr/bin/env python3

import requests
import sys
import json
import time
import collections
import pubchempy as pcp 
import re

sys.stdout = open('/home/user/sertroid/names.json','wt') # this script will output to a file for further processing
response = requests.get("http://tripbot.tripsit.me/api/tripsit/getAllDrugNames") #getting druglist from tripsit api
response = response.json() # parsing druglist into python list
response = response['data'] #removing outer list
response = response[0] # removing outer list

names = []
badlist = ['alcohol','carisoprodol','dramamine','moclobemide','diethyl-ether','aspirin','apap']
for value in response:      #remove none values
    if value is not None:
        if value in badlist:
            pass
        else:
            names.append(value)

synonyms = []
count = 0
for name in names:
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
            pass
        else:
            for key, value in synonym.items():
                namedict = {name : value}
                synonyms.append(namedict)
    #count = count + 1


def problemalias(alias):
    while alias in synonyms:
        synonyms.remove(alias)
problemalias('MT 45')
problemalias('Luminal')
problemalias('Grain Alcohol')
problemalias('Ethyl Ether')

for name in synonyms:
    if len(name) < 4:
        synonyms.remove(name)

synonyms = json.dumps(synonyms) #converting python list to json
print(synonyms)

