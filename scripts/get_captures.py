# -*- coding: utf-8 -*-

# Description: retrieves the capture ids of items
# Example usage:
#   python get_captures.py ../data/src/pd_items.json ../data/captures.json

import json
from pprint import pprint
import re
import sys

# input
if len(sys.argv) < 2:
    print("Usage: %s <inputfile items json> <outputfile item captures json>" % sys.argv[0])
    sys.exit(1)
INPUT_FILE = sys.argv[1]
OUTPUT_FILE = sys.argv[2]

# init
captureIds = []

# Captures
noCaptureCount = 0
invalidCaptureCount = 0

with open(INPUT_FILE, 'r') as f:
        data = json.load(f)

for item in data:

    captureId = item["s"].split("/")[-1]
    captureIds.append(captureId)
              

# Report on captures
print(str(noCaptureCount) + " items with no captures")
print(str(invalidCaptureCount) + " items with invalid captures")

# Write out data
with open(OUTPUT_FILE, 'w') as outfile:
    json.dump(captureIds, outfile, ensure_ascii=False,
              indent=4, sort_keys=True, separators=(',', ': '))
print("Wrote " + str(len(captureIds)) + " lines to " + OUTPUT_FILE)
