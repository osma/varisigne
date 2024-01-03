# Väri-Signe & Väri-Timiri

This repository contains code for Mastodon bots that publish historical photographs colorized using the DeOldify algorithm.

This code is currently used to publish two bots that can be followed using any Mastodon or Fediverse client:

1. Väri-Signe ("Color Signe") at https://botsin.space/@varisigne using photographs taken by Signe Brander
2. Väri-Timiri ("Color Timiri") at https://botsin.space/@varitimiri using photographs taken by Ivan Timiriasew

# Bot code

The bots are in two separate files with almost identical code:

* [varisigne-bot.py](varisigne-bot.py)
* [varitimiri-bot.py](varisigne-bot.py)

These scripts are intended to be triggered using cron.

# Dependencies

The main dependencies are Mastodon.py and Requests. See
[requirements.txt](requirements.txt)

# Data files

The source images were collected via the Finna API using the scripts:

* [finna-data/fetch-signe-records-from-finna.py](finna-data/fetch-signe-records-from-finna.py).
* [finna-data/fetch-timiri-records-from-finna.py](finna-data/fetch-timiri-records-from-finna.py).

The JSON metadata records for the images are in [finna-data/finna-records-signe.jsonl](finna-data/finna-records-signe.jsonl) and [finna-data/finna-records-timiri.jsonl](finna-data/finna-records-timiri.jsonl).

# Colorization

The images were colorized using the [DeOldify](https://github.com/jantic/DeOldify) algorithm under Google Colab.

I used the example Colab notebook and modified it to colorize all images specified in the JSON metadata records and store the colorized images in Google Drive. The notebook can be found at [finna-data/Varisigne_ImageColorizerColab.ipynb](finna-data/Varisigne_ImageColorizerColab.ipynb).

Then I downloaded the colorized images from Google Drive to the server running the bot.
