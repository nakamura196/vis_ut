# -*- coding: utf-8 -*-

# Description: retrieves the genre of items; attempts to normalize genre text
# Example usage:
#   python get_genres.py ../data/src/pd_items.json ../data/genres.json ../data/item_genres.json

from collections import Counter
import json
from pprint import pprint
import re
import sys
import urllib

# input
if len(sys.argv) < 3:
    print("Usage: %s <inputfile items json> <outputfile genres json> <outputfile item genres json>" %
          sys.argv[0])
    sys.exit(1)
INPUT_FILE = sys.argv[1]
OUTPUT_FILE = sys.argv[2]
OUTPUT_ITEMS_FILE = sys.argv[3]

# init
genres = []
item_genres = []


def addGenre(g, url):
    global genres
    global item_genres

    genre = next(iter([_g for _g in genres if _g['value'] == g]), False)

    if genre:
        genres[genre['index']]['count'] += 1
    else:
        label = 'Unknown'
        # url = ''
        if g:
            label = g.capitalize()
            # url = 'http://digitalcollections.nypl.org/search/index?utf8=✓&keywords=&filters%5Brights%5D=pd&filters%5Bgenre%5D=' + label
        genre = {
            'index': len(genres),
            'value': g,
            'label': label,
            'url': url,
            'count': 1
        }
        genres.append(genre)

    item_genres.append(genre['index'])


with open(INPUT_FILE, 'r') as f:
    data = json.load(f)

for item in data:

    genre = ""
    if "type" in item:
        genre = item["type"].split("/")[-1]
        url = item["type"]
    addGenre(genre, url)


# Report on collections
genres = sorted(genres, key=lambda d: d['count'], reverse=True)
pprint(genres)

# Write out data
with open(OUTPUT_FILE, 'w') as outfile:
    json.dump(genres, outfile, ensure_ascii=False, indent=4,
              sort_keys=True, separators=(',', ': '))
print("Wrote " + str(len(genres)) + " genres to " + OUTPUT_FILE)

with open(OUTPUT_ITEMS_FILE, 'w') as outfile:
    json.dump(item_genres, outfile, ensure_ascii=False, indent=4,
              sort_keys=True, separators=(',', ': '))
print("Wrote " + str(len(item_genres)) + " items to " + OUTPUT_ITEMS_FILE)
