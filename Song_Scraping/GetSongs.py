import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sqlite3
import config

input_file = ''

conn = sqlite3.connect("Spotify.db")
cur = conn.cursor()
sql = "select uri from artist where id not in (select artist_id from album) ORDER BY uri;"

cur.execute(sql)

artist_uris = cur.fetchall()

artist_uris = [row[0] for row in artist_uris]

client_credentials_manager = SpotifyClientCredentials(client_id=config.client_id,
                                                      client_secret=config.client_secret)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

for artist_uri in artist_uris:
    print(artist_uri)
    albums = sp.artist_albums(artist_uri)

    # If nothing is returned from search, skip
    if len(albums['items']) == 0:
        print('break')
        continue

    albums = [(album['id'], album['name']) for album in albums['items']][:10]
    print(albums)
    for album in albums:
        print(artist_uri)
        artist_id = artist_uri.split(':')[-1]
        album_id = album[0]
        album_name = album[1]

        album = [album_id, artist_id, album_name, 'spotify:album:'+album_id]

        sql = f''' INSERT INTO album(album_id,artist_id,album_name,album_uri)
                  SELECT ?,?,?,? 
                  WHERE NOT EXISTS(SELECT 1 FROM album WHERE album_id = '{album_id}');'''
        cur = conn.cursor()
        cur.execute(sql, album)
        conn.commit()

        album_tracks = sp.album_tracks(album_id)

        # If nothing is returned from search, skip
        if len(album_tracks['items']) == 0:
            print('break')
            continue

        print(album_tracks)
        for track in album_tracks['items']:

            song_uri = track['uri']
            song_id = track['id']
            song_name = track['name']
            audio_feature = sp.audio_features(song_id)[0]
            print(audio_feature)
            # If nothing is returned from search, skip
            if not audio_feature:
                print('break')
                continue

            danceability = audio_feature['danceability']
            key = audio_feature['key']
            energy = audio_feature['energy']
            loudness = audio_feature['loudness']
            mode = audio_feature['mode']
            speechiness = audio_feature['speechiness']
            acousticness = audio_feature['acousticness']
            instrumentalness = audio_feature['instrumentalness']
            liveness = audio_feature['liveness']
            valence = audio_feature['valence']
            tempo = audio_feature['tempo']

            song =  [
                        song_id, artist_id, album_id,
                        danceability, energy, key,
                        loudness, mode, speechiness,
                        acousticness, instrumentalness, liveness,
                        valence, tempo
                    ]

            sql = f''' INSERT INTO song(song_id, artist_id, album_id, danceability, energy,
                                        key, loudness, mode, speechiness, acousticness, 
                                        instrumentalness, liveness, valence, tempo)
                      SELECT ?,?,?,?,?,?,?,?,?,?,?,?,?,?
                      WHERE NOT EXISTS(SELECT 1 FROM song WHERE song_id = '{song_id}');'''
            cur = conn.cursor()
            cur.execute(sql, song)
            conn.commit()
