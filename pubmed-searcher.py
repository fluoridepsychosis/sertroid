#!/usr/bin/env python3

import requests
import sys
import json
import time
import collections

names_json = open('names.json')

sys.stdout = open('pubmed_output.txt','wt') # this script will output to a file for further processing

names = json.load(names_json) # converting from json to python list

big_list = [] # big chonk

for name in names:

    if name is not None:

        if len(big_list) == 100:

            break

        # Creates entrez url from name
        entrez_url="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&reldate=1&retmax=1000&retmode=json&term=" + name

        entrez_response = requests.get(entrez_url) #returns json data

        parsed_json = entrez_response.json() 

        key = "esearchresult"

        drugname = name

        drugdict = {}

        if key in parsed_json: # sometimes the json doesn't have the key we want for no reason  ¯\_(ツ)_/¯, this checks if it exists

            list_of_pmids = parsed_json["esearchresult"]["idlist"] # retrieves list of pmids from python list

            for item in list_of_pmids:

                drugdict[item] = drugname

        else:

            pass

        big_list.append(drugdict)

        time.sleep(0.334) # to avoid getting b& for flood

flat_dictionary = {}

for dictionary in big_list:  #flattening list
    flat_dictionary.update(dictionary)

data_json = []

for key, item in flat_dictionary.items():

    # This loop is basically the same as the first one except it uses entrez eutils summary instead of eutils search to find info from the PMID,
    # then prints it to the output file

    entrez_summary_url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&retmode=json&id=" + key

    entrez_summary_response = requests.get(entrez_summary_url)

    summary_parsed_json = entrez_summary_response.json()

    pmid = str(key)

    pmid_key = "{}".format(pmid)

    pubmed_url = "https://www.ncbi.nlm.nih.gov/labs/pubmed/" + pmid

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

        datadict = {

            'alias':drugname,
            'title':title,
            'url':pubmed_url,
            'doi':doi

        }

        data_json.append(datadict)

    else:
         pass


data_json = json.dumps(data_json)

with open("pubmed_data.json", "w") as write_file:

    write_file.write(data_json)

names_json.close()
