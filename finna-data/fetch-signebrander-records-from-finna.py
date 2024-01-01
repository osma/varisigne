#!/usr/bin/env python

import requests
import json
import logging

logging.basicConfig(level=logging.INFO)


# Finna API search using the following criteria:
# - format: image
# - author: Brander, Signe
# - organization: Helsingin kaupunginmuseo or Museovirasto
SEARCH_URL = 'https://api.finna.fi/v1/search?filter%5B%5D=%7Eformat_ext_str_mv%3A%220%2FImage%2F%22&filter%5B%5D=%7Eauthor_facet%3A%22Brander%2C+Signe%22&filter%5B%5D=%7Ebuilding%3A%220%2FMuseovirasto%2F%22&filter%5B%5D=%7Ebuilding%3A%220%2FHKM%2F%22&type=AllFields&lng=fi'

page = 0
n_records = 0

while True:
    page += 1
    logging.info(f"Fetching page {page}")
    
    url = f"{SEARCH_URL}&page={page}"
    response = requests.get(url)
    data = response.json()
    if 'records' in data:
        records = data['records']
    else:
        logging.info(f"Empty result for page {page}, stopping.")
        break

    for record in records:
        n_records += 1
        print(json.dumps(record))

logging.info(f"Collected {n_records} records.")
