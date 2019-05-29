# -*- coding: utf-8 -*-

# Description: retrieves the collection of items; attempts to normalize collection text
# Example usage:
#   python get_collections.py ../data/src/pd_items.json ../data/collections.json ../data/item_collections.json

from collections import Counter
import json
from pprint import pprint
import re
import sys
import urllib

# input
if len(sys.argv) < 3:
    print("Usage: %s <inputfile items json> <outputfile collections json> <outputfile item collections json>" %
          sys.argv[0])
    sys.exit(1)
INPUT_FILE = sys.argv[1]
OUTPUT_FILE = sys.argv[2]
OUTPUT_ITEMS_FILE = sys.argv[3]

# init
collections = []
item_collections = []


def addCollection(g, url):
    global collections
    global item_collections

    collection = next(
        iter([_g for _g in collections if _g['value'] == g]), False)

    if collection:
        collections[collection['index']]['count'] += 1
    else:
        label = 'Unknown'
        # url = ''
        if g:
            label = g.capitalize()
            # url = 'http://digitalcollections.nypl.org/search/index?utf8=✓&keywords=&filters%5Brights%5D=pd&filters%5Bcollection%5D=' + label
        collection = {
            'index': len(collections),
            'value': g,
            'label': label,
            'url': url,
            'count': 1
        }
        collections.append(collection)

    item_collections.append(collection['index'])


with open(INPUT_FILE, 'r') as f:
    data = json.load(f)

for item in data:

    collection = item["c_label"]
    url = ""
    if "c_url" in item:
        url = item["c_url"]
    addCollection(collection, url)

# Report on collections
collections = sorted(collections, key=lambda d: d['count'], reverse=True)
pprint(collections)

# Write out data
with open(OUTPUT_FILE, 'w') as outfile:
    json.dump(collections, outfile, ensure_ascii=False, indent=4,
              sort_keys=True, separators=(',', ': '))
print("Wrote " + str(len(collections)) + " collections to " + OUTPUT_FILE)

with open(OUTPUT_ITEMS_FILE, 'w') as outfile:
    json.dump(item_collections, outfile, ensure_ascii=False, indent=4,
              sort_keys=True, separators=(',', ': '))
print("Wrote " + str(len(item_collections)) + " items to " + OUTPUT_ITEMS_FILE)
