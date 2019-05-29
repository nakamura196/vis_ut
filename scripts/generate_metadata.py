# Description: generates a json file that contains the data necessary for the UI
# Example usage:
#   python generate_metadata.py ../data/src/pd_items.json ../js/items/ 5

import json
import math
from pprint import pprint
import re
import sys

# input
if len(sys.argv) < 3:
    print("Usage: %s <inputfile items json> <outputfile item captures json> <number of files>" % sys.argv[0])
    sys.exit(1)
INPUT_FILE = sys.argv[1]
OUTPUT_DIR = sys.argv[2]
FILE_COUNT = int(sys.argv[3])

# init
items = []

with open(INPUT_FILE, 'r') as f:
        data = json.load(f)

for item in data:

    captureId = item["s"].split("/")[-1]
    uuid = item["image"]
    title = item["label"]
    items.append([uuid, title, captureId])

# Write out data
groupSize = int(math.ceil(1.0 * len(items) / FILE_COUNT))
start = 0
end = groupSize
for i in range(FILE_COUNT):
    fileName = OUTPUT_DIR + 'items_'+str(i)+'_'+str(FILE_COUNT)+'.json'
    if i >= FILE_COUNT-1:
        group = items[start:]
    else:
        group = items[start:end]
        start = end
        end += groupSize
    with open(fileName, 'w') as outfile:
        data = {
            'page': i,
            'items': group
        }
        json.dump(data, outfile, ensure_ascii=False, indent=4,
                  sort_keys=True, separators=(',', ': '))
    print("Wrote " + str(len(group)) + " lines to " + fileName)
