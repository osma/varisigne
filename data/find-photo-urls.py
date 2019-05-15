#!/usr/bin/env python3

import csv
import sys
import requests
from bs4 import BeautifulSoup

def tweet_photo_url(tweet_url):
    req = requests.get(tweet_url)
    req.raise_for_status()
    soup = BeautifulSoup(req.content, features='html.parser')
    img = soup.find('meta', property='og:image')
    return img['content']

reader = csv.reader(sys.stdin)
writer = csv.writer(sys.stdout)

for idx,row in enumerate(reader):
    if idx == 0:
        continue
    id = int(row[0])
    tweet_type = row[9]
    if tweet_type != 'Tweet':
        continue
    media_type = row[10]
    if media_type != 'Photo':
        continue
    text = ' '.join(row[1].split(' ')[:-1])
    if not text.endswith(')'):
        continue
    if '#signebrander' in text:
        continue
    url = row[1].split(' ')[-1]
    photo_url = tweet_photo_url(url)
    writer.writerow([id, text, url, photo_url])
