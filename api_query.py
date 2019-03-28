#!/usr/bin/env python3

import requests
import sys
import json
import time

sys.stdout = open('/home/user/sertroid/pubmed_output.txt','wt') # this script will output to a file for further processing

response = requests.get("http://tripbot.tripsit.me/api/tripsit/getAllDrugNames") #getting druglist from tripsit api

response = response.json() # parsing druglist into python list

response = response['data'] 

response = response[0]

data = []

for value in response: 
    if value is not None:
        data.append(value) 

big_list = [] # big chonk

x = 0

for value in data:

    if value is not None:

        # sets entrez url to a drug from the druglist
        entrez_url="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&reldate=1&retmax=1000&retmode=json&term=" + value
    
        
        entrez_response = requests.get(entrez_url) #returns json data

        parsed_json = entrez_response.json() # parses json data into python list

        key = "esearchresult"

        if key in parsed_json: #sometimes the json doesn't have the key we want for no reason  ¯\_(ツ)_/¯, this checks if it exists

            list_of_pmids = parsed_json["esearchresult"]["idlist"] # retrieves list of pmids from python list

        else:
            pass

        big_list.append(list_of_pmids) # joins all pmids into one big list

        time.sleep(0.334) # to avoid getting b& from pubmed for spamming them with requests (pubmed allows 3 url requests per second)

        #x = x + 1
        #print(x)  # counts number of iterations and prints drug name so i know it is working while testing lol
        #print(value)

        #if len(big_list) == 10:  # limits loop to 10 iterations for quickly testing
        #    break

flat_list = []
    
for sublist in big_list:  #flattening list
    for item in sublist:
        flat_list.append(item)

for item in flat_list:

    # This loop is basically the same as the first one except it uses entrez eutils summary instead of eutils search to find info from the PMID,
    # then prints it to the output file

    entrez_summary_url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&retmode=json&id=" + item

    entrez_summary_response = requests.get(entrez_summary_url)

    summary_parsed_json = entrez_summary_response.json()

    pmid = str(item)

    pmid_key = "{}".format(pmid)

    pubmed_url = "https://www.ncbi.nlm.nih.gov/pubmed/" + pmid

    key = "result"

    if key in summary_parsed_json:
        
        # Prints paper title, PMID and pubmed URL in a human-readable form
        print("[Pubmed] " + summary_parsed_json["result"][pmid_key]["title"] + " PMID: " + pmid + " URL: {}".format(pubmed_url))

    else: 
        pass

    




