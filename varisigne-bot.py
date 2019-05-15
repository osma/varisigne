#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import twitter
import requests
import PIL
import imagehash
import io
import os.path
import time
import logging

BOT_NAME='varisigne'
SCREEN_NAME='Signe Brander väreissä'

IMAGEDIR='colorized'
CREDENTIALS_FILE='~/.varisignebot_credentials'
# App registered by @OsmaSuominen
# I don't care that these are public, as the real authentication is done using OAuth tokens
CONSUMER_KEY='FfDJIT93T8hoeufDUp2gXa4SB'
CONSUMER_SECRET='bc6eIvBCOWHpAXdTiTHuWZNQZ3oivh96OMRf6ZF3gPqk393pzX'

STATUS_MAXCOUNT=20 # maximum number of status messages to process per cycle

def parse_tweet(tweet, reply=False):
    """parse a single incoming tweet, returning a (text, result) tuple"""
    if tweet['user']['screen_name'] == SCREEN_NAME:
        return None # ignore my own tweets
    logging.info("%s @%s: %s", tweet['created_at'], tweet['user']['screen_name'], tweet['text'])
    logging.info(tweet)
    if 'media' in tweet['entities']:
        text = ' '.join(tweet['text'].split(' ')[:-1])
        image_url = tweet['entities']['media'][0]['media_url_https']
        response = requests.get(image_url + ':large')
        image = PIL.Image.open(io.BytesIO(response.content))
        imghash = str(imagehash.dhash(image))
        logging.info(imghash)
        imgfn = os.path.join(IMAGEDIR, imghash + '.png')
        if os.path.exists(imgfn):
            return {'id': tweet['id_str'], 'text': text, 'imagefile': imgfn}
    return None

def process_tweet(tweet, reply=False):
    response = parse_tweet(tweet, reply)
    if response:
        text = "{}. Alkuperäinen kuva @signebrander, värit #DeOldify".format(response['text'])
        with open(response['imagefile'], 'rb') as imgfile:
            img_id = t_upload.media.upload(media=imgfile.read())['media_id_string']
            t.statuses.update(status=text, media_ids=img_id, in_reply_to_status_id=response['id'])
            #t.statuses.update(status=text, media_ids=img_id)
        already_posted.add(response['id'])
        logging.info("* Tweet successfully sent.")

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')

MY_TWITTER_CREDS = os.path.expanduser(CREDENTIALS_FILE)
if not os.path.exists(MY_TWITTER_CREDS):
    twitter.oauth_dance(BOT_NAME, CONSUMER_KEY, CONSUMER_SECRET,
                MY_TWITTER_CREDS)

oauth_token, oauth_secret = twitter.read_token_file(MY_TWITTER_CREDS)

t = twitter.Twitter(auth=twitter.OAuth(oauth_token, oauth_secret, CONSUMER_KEY, CONSUMER_SECRET))

t_upload = twitter.Twitter(domain='upload.twitter.com',
    auth=twitter.OAuth(oauth_token, oauth_secret, CONSUMER_KEY, CONSUMER_SECRET))

# initialize since_id by looking for our own most recent tweet
since_id = 1
for tweet in t.statuses.user_timeline(screen_name=SCREEN_NAME, count=1):
    since_id = max(since_id, int(tweet['id']))
logging.debug("* Initialized since_id to %d", since_id)

# keep track of already posted record IDs
already_posted = set()

while True:
    logging.info("* Querying for status of followed users since %d", since_id)
    for tweet in t.statuses.home_timeline(since_id=since_id, count=STATUS_MAXCOUNT):
        since_id = max(since_id, int(tweet['id']))
        process_tweet(tweet)
    
    logging.info("* Sleeping...")
    time.sleep(60)
