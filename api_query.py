#!/usr/bin/env python3

import requests
import sys
import json
import time
import collections

print('api_query.py running')

sys.stdout = open('/home/user/sertroid/pubmed_output.txt','wt') # this script will output to a file for further processing

response = requests.get("http://tripbot.tripsit.me/api/tripsit/getAllDrugNames") #getting druglist from tripsit api

response = response.json() # parsing druglist into python list

response = response['data'] #removing outer list

response = response[0] # removing outer list

data = []

for value in response:      #remove none values
    if value is not None:
        data.append(value) 

big_list = [] # big chonk

for value in data:

    if value is not None:

        # sets entrez url to a drug from the druglist
        entrez_url="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&reldate=1&retmax=1000&retmode=json&term=" + value
        
        entrez_response = requests.get(entrez_url) #returns json data

        parsed_json = entrez_response.json() # parses json data into python list

        key = "esearchresult"

        drugname = value
          
        if key in parsed_json: # sometimes the json doesn't have the key we want for no reason  ¯\_(ツ)_/¯, this checks if it exists

            list_of_pmids = parsed_json["esearchresult"]["idlist"] # retrieves list of pmids from python list
            
            drugdict = collections.OrderedDict()

            for item in list_of_pmids:

                drugdict[item] = drugname 
        
        else:
            pass
        
        big_list.append(drugdict) # joins all pmids into one big list

        

        time.sleep(0.334) # to avoid getting b& from pubmed for spamming them with requests (pubmed allows 3 url requests per second)

        #if len(big_list) == 10:  # limits loop to 10 iterations for quickly testing
        #    break

flat_dictionary = {}

print(flat_dictionary)
    
for dictionary in big_list:  #flattening list
    flat_dictionary.update(dictionary)

for key, item in flat_dictionary.items():

    # This loop is basically the same as the first one except it uses entrez eutils summary instead of eutils search to find info from the PMID,
    # then prints it to the output file

    entrez_summary_url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&retmode=json&id=" + key

    entrez_summary_response = requests.get(entrez_summary_url)

    summary_parsed_json = entrez_summary_response.json()

    pmid = str(key)

    pmid_key = "{}".format(pmid)

    pubmed_url = "https://www.ncbi.nlm.nih.gov/pubmed/" + pmid

    list_key = "result"

    drugname = item

    if list_key in summary_parsed_json:

        title = summary_parsed_json["result"][pmid_key]["title"]

        article_ids = summary_parsed_json["result"][pmid_key]["articleids"]

        matched_article_id = None

        for article_id in article_ids:
    
            if article_id['idtype'] == "doi":

                matched_article_id = article_id

                doi = "https://doi.org/" + matched_article_id['value']


        
        # Prints paper title, PMID and pubmed URL in a human-readable form
        print("[Pubmed] " + "[{}] ".format(drugname) + title + " URL: " + pubmed_url  + " DOI: " + doi)

    else: 
        pass






