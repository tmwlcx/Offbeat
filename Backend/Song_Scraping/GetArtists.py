import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sqlite3
import time
import config
import csv

input_file = open(r'C:\Users\jeffr\Desktop\Spotify\artists.csv', encoding='utf-8')
artists = [item[0] for item in list(csv.reader(input_file))]
artists = sorted(list(set(artists)))

conn = sqlite3.connect("Spotify.db")
cur = conn.cursor()

client_credentials_manager = SpotifyClientCredentials(client_id=config.client_id,
                                                      client_secret=config.client_secret)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

for artist in artists:
    print(artist)
    res = sp.search(q="artist:"+artist, type="artist", limit=1)

    # If nothing is returned from search, skip
    if len(res['artists']['items']) == 0:
        print('break')
        continue

    # return data from json
    spotify_id = res['artists']['items'][0]['id']
    uri = res['artists']['items'][0]['uri']
    name = res['artists']['items'][0]['name']
    followers = res['artists']['items'][0]['followers']['total']

    artist = [spotify_id, uri, name, followers]

    sql = f''' INSERT INTO artist(id,uri,name,followers)
              SELECT ?,?,?,? 
              WHERE NOT EXISTS(SELECT 1 FROM artist WHERE id = '{spotify_id}');'''
    cur = conn.cursor()
    cur.execute(sql, artist)
    conn.commit()
    # pause between requests
    time.sleep(.25)
    print(cur.lastrowid)

