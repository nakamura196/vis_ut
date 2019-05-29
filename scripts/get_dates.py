# -*- coding: utf-8 -*-

# Description: retrieves the date (year or century) of items
# Example usage:
#   python get_dates.py ../data/src/pd_items.json ../data/dates.json ../data/item_dates.json year
#   python get_dates.py ../data/src/pd_items.json ../data/centuries.json ../data/item_centuries.json century

from collections import Counter
import json
from pprint import pprint
import re
import sys
import urllib

# input
if len(sys.argv) < 3:
    print("Usage: %s <inputfile items json> <outputfile dates json> <outputfile item dates json>" %
          sys.argv[0])
    sys.exit(1)
INPUT_FILE = sys.argv[1]
OUTPUT_FILE = sys.argv[2]
OUTPUT_ITEMS_FILE = sys.argv[3]

# init
dates = []
item_dates = []


def addDate(g, url):
    global dates
    global item_dates

    date = next(
        iter([_g for _g in dates if _g['value'] == g]), False)

    if date:
        dates[date['index']]['count'] += 1
    else:
        label = 'Unknown'
        # url = ''
        if g:
            label = g.capitalize()
            # url = 'http://digitaldates.nypl.org/search/index?utf8=✓&keywords=&filters%5Brights%5D=pd&filters%5Bdate%5D=' + label
        date = {
            'index': len(dates),
            'value': g,
            'label': label,
            'url': url,
            'count': 1
        }
        dates.append(date)

    item_dates.append(date['index'])


with open(INPUT_FILE, 'r') as f:
    data = json.load(f)

for item in data:

    date = ""
    url = ""

    if "t" in item:
        date = item["t"].split("/")[-1]
        url = item["t"]
    addDate(
        date, url)

# Report on dates
dates = sorted(dates, key=lambda d: d['value'])
pprint(dates)

# Write out data
with open(OUTPUT_FILE, 'w') as outfile:
    json.dump(dates, outfile, ensure_ascii=False, indent=4,
              sort_keys=True, separators=(',', ': '))
print("Wrote " + str(len(dates)) + " dates to " + OUTPUT_FILE)

with open(OUTPUT_ITEMS_FILE, 'w') as outfile:
    json.dump(item_dates, outfile, ensure_ascii=False, indent=4,
              sort_keys=True, separators=(',', ': '))
print("Wrote " + str(len(item_dates)) + " items to " + OUTPUT_ITEMS_FILE)
