# -*- coding: utf-8 -*-

# Description: retrieves the date (year or century) of items
# Example usage:
#   python get_dates.py ../data/src/pd_items.json ../data/dates.json ../data/item_dates.json year
#   python get_dates.py ../data/src/pd_items.json ../data/centuries.json ../data/item_centuries.json century

from collections import Counter
import json
import math
from pprint import pprint
import re
import sys
from SPARQLWrapper import SPARQLWrapper
import urllib.request

OUTPUT_FILE = "../data/src/pd_items_all.json"

page = 0
d = 10000
flg = True

arr = []

dd = []

while flg:

    print("page="+str(page+1))

    

    query = """                                                                                                                              
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX dc: <http://purl.org/dc/elements/1.1/>
        PREFIX dcterms: <http://purl.org/dc/terms/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX sim: <http://purl.org/ontology/similarity/>
        PREFIX mo: <http://purl.org/ontology/mo/>
        PREFIX ov: <http://open.vocab.org/terms/>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX dcndl: <http://ndl.go.jp/dcndl/terms/>
        PREFIX jps: <https://jpsearch.go.jp/term/property#>
        PREFIX schema: <http://schema.org/>
        select distinct ?s ?image ?type ?label ?t ?c_label where {                                                                                                                                                                
            ?s foaf:thumbnail ?image .
            ?s dcndl:materialType ?type . 
            ?s dcterms:title ?label .
            optional { ?s dcterms:issued ?t . FILTER ( datatype(?t) = dcterms:W3CDTF) } 
            ?s dcterms:isPartOf ?c_label . FILTER ( lang(?c_label) = "ja") 
        } limit """+str(d)+""" offset """+str(page * d)+"""                                                                                                   
    """

    sparql = SPARQLWrapper(
        endpoint='https://sparql.dl.itc.u-tokyo.ac.jp/', returnFormat='json')
    sparql.setQuery(query)


    results = sparql.query().convert()
    results = results["results"]["bindings"]

    if len(results) > 0:

        for i in range(len(results)):
            if i % 20 == 0:
                print("i="+str(i+page * d))

            obj = results[i]
            s = obj["s"]["value"]

            if s not in dd:

                obj2 = {}
                for key in obj:
                    obj2[key] = obj[key]["value"]

                arr.append(obj2)
                dd.append(s)

        # flg = False
    else:
        flg = False

    page += 1

with open(OUTPUT_FILE, 'w') as outfile:
    json.dump(arr, outfile, ensure_ascii=False, indent=4,
              sort_keys=True, separators=(',', ': '))
