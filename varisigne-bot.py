#!/usr/bin/env python

import json
import os.path
import random

from mastodon import Mastodon


IMAGE_DATA = 'finna-data/finna-records.jsonl'
IMAGE_DIR = 'finna-data/images'

FINNA_BASE_URL = 'https://finna.fi'


def image_filename(record_id):
    return os.path.join(IMAGE_DIR, f"{record_id}.jpg")


# Read the image data
images = []

with open(IMAGE_DATA) as datafile:
    for line in datafile:
        record = json.loads(line)
        # check that we have a corresponding image, otherwise skip record
        if not os.path.exists(image_filename(record['id'])):
            continue
        images.append(record)

# Initialize Mastodon library
mastodon = Mastodon(
    access_token = 'token.secret',
    api_base_url = 'https://botsin.space/'
)

# Pick a random image
record = random.choice(images)

# Prepare a post
title = record['title']
year = record['year']
collection = ', '.join([brec['translated'] for brec in record['buildings']])
link = f"{FINNA_BASE_URL}/Record/{record['id']}"

status_text = f"""
{title}. ({year}, {collection})
Alkuperäinen kuva: {link}
Valokuvaaja Signe Brander, värit #DeOldify
""".strip()

alt_text = f"""
{title}. ({year}, {collection})

Alkuperäisen valokuvan on ottanut Signe Brander. Tämä kuva on keinotekoisesti väritetty DeOldify-algoritmilla.
""".strip()

# Post it!
media = mastodon.media_post(image_filename(record['id']), description=alt_text)
mastodon.status_post(status_text, media_ids=media, language='fi')
