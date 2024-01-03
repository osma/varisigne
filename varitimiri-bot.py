#!/usr/bin/env python

import json
import os.path
import random
import re

from mastodon import Mastodon


IMAGE_DATA = 'finna-data/finna-records-timiri.jsonl'
ORIG_IMAGE_DIR = 'finna-data/original/timiri'
COLOR_IMAGE_DIR = 'finna-data/colorized/timiri'
FINNA_BASE_URL = 'https://finna.fi'
TOKEN_FILE = 'timiri.secret'


def orig_image_filename(record_id):
    return os.path.join(ORIG_IMAGE_DIR, f"{record_id}.jpg")


def color_image_filename(record_id):
    return os.path.join(COLOR_IMAGE_DIR, f"{record_id}.jpg")


# Read the image data
images = []

with open(IMAGE_DATA) as datafile:
    for line in datafile:
        record = json.loads(line)
        # check that we have a corresponding image, otherwise skip record
        if not os.path.exists(orig_image_filename(record['id'])) or \
           not os.path.exists(color_image_filename(record['id'])):
            continue
        images.append(record)

# Pick a random image
record = random.choice(images)

# Prepare a post
title = record['title']
try:
  year = record['year']
except KeyError:
  year = 'tuntematon vuosi'
collection = ', '.join([brec['translated'] for brec in record['buildings']])
link = f"{FINNA_BASE_URL}/Record/{record['id']}"

status_text = f"""
{title}. ({year}, {collection})
Alkuperäisen kuvan lähde: {link}
Valokuvaaja Ivan Timiriasew, värit #DeOldify
""".strip()

color_alt_text = f"""
{title}. ({year}, {collection})

Alkuperäisen valokuvan on ottanut Ivan Timiriasew. Tämä kuva on keinotekoisesti väritetty DeOldify-algoritmilla.
""".strip()


orig_alt_text = f"""
{title}. ({year}, {collection})

Alkuperäinen mustavalkoinen valokuva, jonka on ottanut Ivan Timiriasew.
""".strip()


# Initialize Mastodon library
mastodon = Mastodon(
    access_token = TOKEN_FILE,
    api_base_url = 'https://botsin.space/'
)

# Post it!
media_color = mastodon.media_post(color_image_filename(record['id']), description=color_alt_text)
media_orig = mastodon.media_post(orig_image_filename(record['id']), description=orig_alt_text)
mastodon.status_post(status_text, media_ids=[media_color, media_orig], language='fi')
