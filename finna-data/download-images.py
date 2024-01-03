#!/usr/bin/env python

import requests
import json
import logging
import os.path
import sys

logging.basicConfig(level=logging.INFO)

BASE_URL = "https://finna.fi"

if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <records.jsonl> <output-dir>", file=sys.stderr)
    sys.exit(1)


records_file = sys.argv[1]
output_dir = sys.argv[2]

with open(records_file) as jsonl_file:
    for line in jsonl_file:
        record = json.loads(line)
        try:
            image_url = BASE_URL + record['images'][0]
        except IndexError:
            continue
        outfilename = os.path.join(output_dir, f"{record['id']}.jpg")
        logging.info(f"downloading {record['id']} from {image_url} into {outfilename}")
        with requests.get(image_url, stream=True) as r:
            with open(outfilename, "wb") as outfile:
                for chunk in r.iter_content(chunk_size=8192):
                    outfile.write(chunk)
