# Väri-Signe
Mastodon bot that colorizes old photos using the DeOldify algorithm.

The bot is running at https://botsin.space/@varisigne and can be followed
using any Mastodon or Fediverse client.

# Bot code

The bot itself is in the file [varisigne-bot.py](varisigne-bot.py)

# Dependencies

The main dependencies are Mastodon.py and Requests. See
[requirements.txt](requirements.txt)

# Data files

The source images were collected via the Finna API using the script
[finna-data/fetch-signebrander-records-from-finna.py](finna-data/fetch-signebrander-records-from-finna.py).
The JSON metadata records for the images are in
[finna-data/finna-records.jsonl](finna-data/finna-records.jsonl).

# Colorization

The images were colorized using the
[DeOldify](https://github.com/jantic/DeOldify) algorithm under Google Colab.
I used the example Colab notebook and modified it to colorize all images
specified in the JSON metadata records and store the colorized images in
Google Drive. Then I downloaded the images to the server running the bot.
